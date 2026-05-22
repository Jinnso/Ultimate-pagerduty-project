import os
import sys
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

DD_URL = f"https://api.{DD_SITE}/api/v1/synthetics/tests/api"

headers = {
    "DD-API-KEY": DD_API_KEY,
    "DD-APPLICATION-KEY": DD_APP_KEY,
    "Content-Type": "application/json"
}

payload = {
    "name": "Acme Hotel - Cloud Reservation API Health Check",
    "type": "api",
    "subtype": "http",
    "config": {
        "request": {
            "url": "https://httpstat.us/500",
            "method": "GET",
            "timeout": 30
        },
        "assertions": [
            {
                "operator": "is",
                "type": "statusCode",
                "target": 200
            }
        ]
    },
    "message": "@pagerduty-Cloud_Reservation_API\n\n[CRITICAL] Reservation API failure.\n\n{\"impact\": \"all_guests\"}",
    "options": {
        "tick_every": 60,
        "min_failure_duration": 0,
        "min_location_failed": 1,
        "follow_redirects": False,
        "monitor_options": {
            "renotify_interval": 0
        }
    },
    "status": "paused",
    "locations": ["aws:us-east-1"],
    "tags": ["env:production", "team:tech_ops"]
}

print(f"[DEBUG] POST {DD_URL}")
response = requests.post(DD_URL, headers=headers, json=payload, timeout=30)

if response.status_code == 200:
    data = response.json()
    test_id = data.get('public_id')
    print(f"[+] Synthetic Test created successfully. ID: {test_id}")
    print("[+] The test is in 'paused' state. Enable it manually in Datadog when you're ready to start the simulation.")
else:
    print(f"[-] Datadog Error HTTP {response.status_code}")
    print(f"[-] Response: {response.text}")
