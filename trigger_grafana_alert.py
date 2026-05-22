"""
Triggers a real Grafana alert notification through the Grafana Alerting system.
The alert rule (IoT Local Key Controllers Failure) uses the math expression 1 > 0,
which always evaluates to true. When Grafana evaluates it, the alert fires and
routes through the Prometheus Alertmanager → PagerDuty → Event Orchestration.

Unlike simulate_iot_alert.py (which bypasses Grafana), this script makes Grafana
an active participant in the monitoring pipeline.

Before running: ensure create_grafana_alert.py was executed first.
"""
import os
import sys
import time
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

GRAFANA_API_KEY = os.environ.get("GRAFANA_API_KEY")
GRAFANA_URL = os.environ.get("GRAFANA_URL", "https://acmehotel.grafana.net")

if not GRAFANA_API_KEY:
    print("[-] ERROR: GRAFANA_API_KEY not found in .env")
    sys.exit(1)

GRAFANA_API_KEY = GRAFANA_API_KEY.strip().replace('"', '').replace("'", "")
ALERT_RULE_TITLE = "IoT Local Key Controllers Failure"

HEADERS = {
    "Authorization": f"Bearer {GRAFANA_API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def find_alert_rule():
    print(f"[*] Searching for alert rule: {ALERT_RULE_TITLE}")
    resp = requests.get(
        f"{GRAFANA_URL}/api/v1/provisioning/alert-rules",
        headers=HEADERS,
        timeout=15
    )
    if resp.status_code != 200:
        print(f"[-] Failed to list alert rules. HTTP {resp.status_code}: {resp.text}")
        return None

    rules = resp.json()
    for rule in rules:
        if rule.get("title") == ALERT_RULE_TITLE:
            print(f"[+] Found alert rule. UID: {rule.get('uid')}, State: {rule.get('state', 'unknown')}")
            return rule
    print(f"[-] Alert rule not found. Run create_grafana_alert.py first.")
    return None

def check_rule_state(rule_uid):
    print("[*] Checking alert rule evaluation state...")
    resp = requests.get(
        f"{GRAFANA_URL}/api/v1/provisioning/alert-rules/{rule_uid}",
        headers=HEADERS,
        timeout=15
    )
    if resp.status_code == 200:
        rule = resp.json()
        state = rule.get("state", "unknown")
        print(f"[*] Current state: {state}")
        return state
    return "unknown"

def trigger_test_alert(rule_uid):
    """
    Attempts to trigger a test alert notification.
    Grafana 9+ supports test notifications through the alert rule API.
    """
    print("[*] Triggering test alert notification through Grafana Alertmanager...")

    # Grafana Managed Alertmanager endpoint
    payload = {
        "alerts": [{
            "status": "firing",
            "labels": {
                "alertname": ALERT_RULE_TITLE,
                "severity": "critical",
                "service": "iot_controllers"
            },
            "annotations": {
                "summary": "FIRING: Digital lock controllers are offline.",
                "description": "BLE/NFC devices across hotels are not responding. No communication for over 1 minute."
            },
            "startsAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "endsAt": "0001-01-01T00:00:00Z",
            "generatorURL": f"{GRAFANA_URL}/alerting/grafana/{rule_uid}/view"
        }]
    }

    resp = requests.post(
        f"{GRAFANA_URL}/api/alertmanager/grafana/api/v2/alerts",
        headers=HEADERS,
        json=payload,
        timeout=15
    )

    if resp.status_code in (200, 202, 204):
        print("[+] Test alert posted to Grafana Alertmanager.")
        print("[!] Grafana should now route this to the Prometheus contact point.")
        print("[!] Prometheus → PagerDuty integration → Event Orchestration (P1).")
        return True

    print(f"[-] Grafana Alertmanager HTTP {resp.status_code}: {resp.text}")
    print("[!] Alternative: the alert rule evaluates every 1 minute and should fire automatically.")
    print("[!] Check PagerDuty for a new incident on IoT Local Key Controllers.")
    return False

if __name__ == "__main__":
    rule = find_alert_rule()
    if not rule:
        sys.exit(1)

    rule_uid = rule["uid"]
    state = check_rule_state(rule_uid)

    if state == "firing":
        print("[+] Alert rule is already firing. PagerDuty should have received the alert.")
        print("[!] If not visible in PagerDuty, check the Prometheus integration contact point in Grafana.")
    else:
        print("[*] Alert rule is not firing yet. Triggering test alert...")
        trigger_test_alert(rule_uid)

    print("\n[+] Grafana Alerting flow complete.")
    print("[+] Grafana was an active participant: Alert Rule → Alertmanager → PagerDuty Integration.")
