import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

ROUTING_KEY = os.environ.get("PAGERDUTY_IOT_EVENTS_KEY")

if not ROUTING_KEY:
    print("[-] ERROR: PAGERDUTY_IOT_EVENTS_KEY not found in .env")
    print("[!] Run 'terraform output grafana_prometheus_integration_key' and copy the value into .env")
    sys.exit(1)

ROUTING_KEY = ROUTING_KEY.strip().replace('"', '').replace("'", "")

URL = "https://events.pagerduty.com/v2/enqueue"

payload = {
    "routing_key": ROUTING_KEY,
    "event_action": "trigger",
    "payload": {
        "summary": "FIRING: Digital lock controllers are offline.",
        "source": "Grafana Alerting - IoT Nodes",
        "severity": "critical",
        "component": "IoT Local Key Controllers",
        "group": "Hotel Edge Devices",
        "class": "iot_controllers",
        "custom_details": {
            "alert_rule": "IoT Local Key Controllers Failure",
            "datasource": "Prometheus",
            "message": "BLE/NFC devices across hotels are not responding. No communication for over 1 minute.",
            "grafana_url": "https://acmehotel.grafana.net"
        }
    }
}

print("Simulating IoT incident (Grafana/Prometheus -> P1 via orchestration)...")

try:
    response = requests.post(URL, json=payload, timeout=15)
    if response.status_code == 202:
        print(f"[+] IoT alert sent successfully. HTTP {response.status_code}")
        print("[!] Check PagerDuty: the 'FIRING' rule in iot_orchestration should elevate to P1.")
        print("[!] Orchestration looks for 'FIRING' in event.summary to assign P1.")
    else:
        print(f"[-] PagerDuty responded with HTTP {response.status_code}")
        print(f"[-] Detail: {response.text}")
except requests.exceptions.RequestException as e:
    print(f"[-] Connection error: {e}")
