import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

GRAFANA_API_KEY = os.environ.get("GRAFANA_API_KEY")
GRAFANA_URL = os.environ.get("GRAFANA_URL", "https://acmehotel.grafana.net")

if not GRAFANA_API_KEY:
    print("[-] ERROR: GRAFANA_API_KEY not found in .env")
    sys.exit(1)

GRAFANA_API_KEY = GRAFANA_API_KEY.strip().replace('"', '').replace("'", "")

headers = {
    "Authorization": f"Bearer {GRAFANA_API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

payload = {
    "title": "IoT Local Key Controllers Failure",
    "condition": "C",
    "data": [
        {
            "refId": "A",
            "relativeTimeRange": {"from": 600, "to": 0},
            "datasourceUid": "-100",
            "model": {
                "type": "math",
                "expression": "1 > 0"
            }
        },
        {
            "refId": "C",
            "datasourceUid": "-100",
            "model": {
                "type": "threshold",
                "expression": "A",
                "conditions": [{"evaluator": {"params": [0], "type": "gt"}}]
            }
        }
    ],
    "noDataState": "NoData",
    "execErrState": "Error",
    "folderUID": os.environ.get("GRAFANA_FOLDER_UID", "ffh2hh"),
    "orgID": 1,
    "ruleGroup": "Acme Hotel IoT Checks",
    "for": "1m",
    "labels": {
        "severity": "critical",
        "service": "iot_controllers"
    },
    "annotations": {
        "summary": "FIRING: Digital lock controllers are offline.",
        "description": "BLE/NFC devices across hotels are not responding."
    }
}

print(f"[DEBUG] POST {GRAFANA_URL}/api/v1/provisioning/alert-rules")
print(f"[DEBUG] folderUID: {payload['folderUID']}")

response = requests.post(
    f"{GRAFANA_URL}/api/v1/provisioning/alert-rules",
    headers=headers,
    json=payload,
    timeout=15
)

if response.status_code == 201:
    print("[+] Grafana Alert Rule created successfully.")
elif response.status_code == 200:
    print("[+] Grafana Alert Rule updated successfully (already existed).")
else:
    print(f"[-] Grafana Error HTTP {response.status_code}")
    print(f"[-] Response: {response.text}")
    if response.status_code == 404:
        print("[!] Verify that GRAFANA_FOLDER_UID exists in your Grafana instance.")
