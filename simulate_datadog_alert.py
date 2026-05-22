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
        "summary": "[CRITICAL] Massive failure in Reservation API (Acme Hotel)",
        "source": "Datadog - Synthetic Test",
        "severity": "critical",
        "component": "Cloud Reservation API",
        "group": "Production Servers",
        "custom_details": {
            "impact": "all_guests",
            "error_rate": "100%",
            "region": "us-east-1",
            "message": "The reservation database is unresponsive. Guests cannot check in."
        }
    }
}

print("Simulating P0 incident (impact: all_guests)...")

try:
    response = requests.post(URL, json=payload, timeout=15)
    if response.status_code == 202:
        print(f"[+] P0 sent successfully. HTTP {response.status_code}")
        print("[!] Check PagerDuty: the 'all_guests' rule should assign P0 priority.")
        print("[!] Orchestration will set severity to 'critical' and priority to P0.")
    else:
        print(f"[-] PagerDuty responded with HTTP {response.status_code}")
        print(f"[-] Detail: {response.text}")
except requests.exceptions.RequestException as e:
    print(f"[-] Connection error: {e}")
