"""
Triggers a real Datadog Synthetic Test run.
The test targets httpstat.us/500 (always returns 500) with an assertion expecting 200,
so it always fails → Datadog generates an alert → PagerDuty receives it via the integration
→ Event Orchestration classifies the incident.

Unlike simulate_datadog_alert.py (which bypasses Datadog), this script makes Datadog
an active participant in the monitoring pipeline.
"""
import os
import sys
import time
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

DD_API_KEY = os.environ.get("DATADOG_API_KEY")
DD_APP_KEY = os.environ.get("DATADOG_APP_KEY")
DD_SITE = os.environ.get("DATADOG_SITE", "us5.datadoghq.com")

if not DD_API_KEY or not DD_APP_KEY:
    print("[-] ERROR: DATADOG_API_KEY or DATADOG_APP_KEY not found in .env")
    sys.exit(1)

DD_API_KEY = DD_API_KEY.strip().replace('"', '').replace("'", "")
DD_APP_KEY = DD_APP_KEY.strip().replace('"', '').replace("'", "")
BASE = f"https://api.{DD_SITE}"

HEADERS = {
    "DD-API-KEY": DD_API_KEY,
    "DD-APPLICATION-KEY": DD_APP_KEY,
    "Content-Type": "application/json"
}

TEST_NAME = "Acme Hotel - Cloud Reservation API Health Check"

def find_test():
    print(f"[*] Searching for synthetic test: {TEST_NAME}")
    resp = requests.get(f"{BASE}/api/v1/synthetics/tests", headers=HEADERS, timeout=30)
    if resp.status_code != 200:
        print(f"[-] Failed to list tests. HTTP {resp.status_code}: {resp.text}")
        return None
    for test in resp.json().get("tests", []):
        if test.get("name") == TEST_NAME:
            return test
    print(f"[-] Test not found. Run create_datadog_test.py first.")
    return None

def unpause_test(public_id):
    print("[*] Unpausing test (status: live)...")
    resp = requests.put(
        f"{BASE}/api/v1/synthetics/tests/{public_id}",
        headers=HEADERS,
        json={"status": "live"},
        timeout=30
    )
    if resp.status_code == 200:
        print("[+] Test is now live and will run every 60 seconds.")
        return True
    print(f"[-] Failed to unpause. HTTP {resp.status_code}: {resp.text}")
    return False

def trigger_test_run(public_id):
    print("[*] Triggering immediate test run...")
    resp = requests.post(
        f"{BASE}/api/v1/synthetics/tests/trigger/{public_id}",
        headers=HEADERS,
        json={"tests": [{"public_id": public_id}]},
        timeout=30
    )
    if resp.status_code == 200:
        data = resp.json()
        result_id = data.get("results", [{}])[0].get("result_id")
        print(f"[+] Test run triggered. result_id: {result_id}")
        return result_id
    print(f"[-] Failed to trigger. HTTP {resp.status_code}: {resp.text}")
    return None

def wait_for_result(result_id, public_id, timeout=120):
    print(f"[*] Waiting for test result (up to {timeout}s)...")
    start = time.time()
    while time.time() - start < timeout:
        resp = requests.get(
            f"{BASE}/api/v1/synthetics/tests/{public_id}/results/{result_id}",
            headers=HEADERS,
            timeout=30
        )
        if resp.status_code == 200:
            data = resp.json()
            status = data.get("status", 99)
            if status != 99:
                passed = status == 0
                print(f"[{'PASS' if passed else 'FAIL'}] Test completed. Status code: {status}")
                print(f"[!] {'This should NOT have passed — check the assertion.' if passed else 'Test failed as expected.'}")
                print(f"[!] Datadog alert should now be routing to PagerDuty via the integration.")
                print(f"[!] Check PagerDuty for a new incident on Cloud Reservation API.")
                if not passed:
                    print("[!] Event Orchestration will classify based on the alert content.")
                return True
        time.sleep(3)
    print("[-] Timed out waiting for test result.")
    return False

if __name__ == "__main__":
    test = find_test()
    if not test:
        sys.exit(1)

    public_id = test["public_id"]
    current_status = test.get("status", "live")

    if current_status == "paused":
        if not unpause_test(public_id):
            sys.exit(1)
        time.sleep(2)

    result_id = trigger_test_run(public_id)
    if result_id:
        wait_for_result(result_id, public_id)

    print("\n[+] Datadog Synthetic Test flow complete.")
    print("[+] Datadog was an active participant: Synthetic Test → Alert → PagerDuty Integration.")
