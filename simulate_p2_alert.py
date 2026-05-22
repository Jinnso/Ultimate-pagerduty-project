import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

ROUTING_KEY = os.environ.get("PAGERDUTY_EVENTS_KEY")

if not ROUTING_KEY:
    print("[-] ERROR: PAGERDUTY_EVENTS_KEY not found in .env")
    sys.exit(1)

ROUTING_KEY = ROUTING_KEY.strip().replace('"', '').replace("'", "")

URL = "https://events.pagerduty.com/v2/enqueue"

payload = {
    "routing_key": ROUTING_KEY,
    "event_action": "trigger",
    "payload": {
        "summary": "[P2] Isolated hotel failure - Reservation API (Acme Hotel)",
        "source": "Datadog - Synthetic Test",
        "severity": "error",
        "component": "Cloud Reservation API",
        "group": "Production Servers",
        "custom_details": {
            "impact": "single_hotel",
            "error_rate": "30%",
            "region": "us-east-1",
            "message": "Hotel in Augusta, GA reports high latency on the reservation endpoint."
        }
    }
}

print("Simulating P2 incident (impact: single_hotel)...")

try:
    response = requests.post(URL, json=payload, timeout=15)
    if response.status_code == 202:
        print(f"[+] P2 sent successfully. HTTP {response.status_code}")
        print("[!] Check PagerDuty: the 'single_hotel' rule should assign P2 priority.")
        print("[!] Orchestration will set severity to 'error' and priority to P2.")
    else:
        print(f"[-] PagerDuty responded with HTTP {response.status_code}")
        print(f"[-] Detail: {response.text}")
except requests.exceptions.RequestException as e:
    print(f"[-] Connection error: {e}")
