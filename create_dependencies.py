import os
import sys
import requests
import time
from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.environ.get("PAGERDUTY_API_KEY")
if not API_KEY:
    print("[-] ERROR: PAGERDUTY_API_KEY not found in .env")
    sys.exit(1)

BASE_URL = "https://api.pagerduty.com"
HEADERS = {
    "Accept": "application/vnd.pagerduty+json;version=2",
    "Authorization": f"Token token={API_KEY}",
    "Content-Type": "application/json"
}

LOCATIONS = [
    "Americus, GA",
    "Macon, GA",
    "Birmingham, AL",
    "Augusta, GA",
    "Panama City Beach, FL",
]

PER_HOTEL_SERVICES = [
    "Web Reservations",
    "Mobile Reservations",
    "Facilities Management",
    "Check-In / Digital Key",
    "In-Room Entertainment",
    "Housekeeping Management",
]

GENERIC_BUSINESS_SERVICES = [
    "Web Reservations",
    "Mobile Reservations",
    "Check-In / Digital Key",
    "In-Room Entertainment (WiFi, Streaming, Dining)",
    "Housekeeping Management",
    "Facilities Management",
]

TECHNICAL_SERVICES = [
    "Cloud Reservation API (AWS)",
    "IoT Local Key Controllers",
]

# ── helpers ──────────────────────────────────────

def api_get(endpoint, params=None):
    url = f"{BASE_URL}/{endpoint}"
    resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
    if resp.status_code != 200:
        print(f"[-] GET {endpoint} failed: HTTP {resp.status_code}")
        return None
    return resp.json()

def api_post(endpoint, payload):
    url = f"{BASE_URL}/{endpoint}"
    resp = requests.post(url, headers=HEADERS, json=payload, timeout=30)
    return resp

def find_service(name, is_business=False):
    endpoint = "business_services" if is_business else "services"
    data = api_get(endpoint, {"query": name})
    if not data:
        return None
    results = data.get(endpoint, [])
    for svc in results:
        if svc["name"] == name:
            return {"id": svc["id"], "type": "business_service" if is_business else "service"}
    return None

def create_business_service(name, description):
    print(f"    Creating business service: {name}")
    resp = api_post("business_services", {
        "business_service": {
            "name": name,
            "description": description,
        }
    })
    if resp.status_code in (200, 201):
        data = resp.json()
        svc_id = data["business_service"]["id"]
        print(f"    [+] Created. ID: {svc_id}")
        return svc_id
    elif resp.status_code == 400 and "already exists" in resp.text.lower():
        print(f"    [!] Already exists, searching...")
        time.sleep(0.5)
        svc = find_service(name, is_business=True)
        if svc:
            print(f"    [+] Found existing. ID: {svc['id']}")
            return svc["id"]
        return None
    else:
        print(f"    [-] Failed: HTTP {resp.status_code} — {resp.text[:200]}")
        return None

def create_dependency(supporting, dependent):
    resp = api_post("service_dependencies/associate", {
        "relationships": [{
            "supporting_service": supporting,
            "dependent_service": dependent,
        }]
    })
    return resp

# ── main ─────────────────────────────────────────

if __name__ == "__main__":
    created_count = 0
    linked_count = 0

    # 1 ─ Find existing technical services
    print("=" * 60)
    print("1. LOCATING TECHNICAL SERVICES")
    print("=" * 60)
    tech_services = {}
    for name in TECHNICAL_SERVICES:
        svc = find_service(name)
        if svc:
            tech_services[name] = svc
            print(f"  [+] Found: {name} ({svc['id']})")
        else:
            print(f"  [-] NOT FOUND: {name}")
        time.sleep(0.5)

    if len(tech_services) < 2:
        print("\n[-] One or more technical services not found. Run Terraform first.")
        sys.exit(1)

    # 2 ─ Find generic business services
    print("\n" + "=" * 60)
    print("2. LOCATING GENERIC BUSINESS SERVICES")
    print("=" * 60)
    generic_biz = {}
    for name in GENERIC_BUSINESS_SERVICES:
        svc = find_service(name, is_business=True)
        if svc:
            generic_biz[name] = svc
            print(f"  [+] Found: {name}")
        else:
            print(f"  [-] NOT FOUND: {name}")
        time.sleep(0.5)

    # 3 ─ Create per-hotel business services
    print("\n" + "=" * 60)
    print("3. CREATING PER-HOTEL BUSINESS SERVICES")
    print("=" * 60)
    hotel_services = {}
    for location in LOCATIONS:
        short = location.split(",")[0]
        for svc_name in PER_HOTEL_SERVICES:
            name = f"{short} - {svc_name}"
            desc = f"{svc_name} for the hotel property in {location}."
            svc_id = create_business_service(name, desc)
            if svc_id:
                hotel_services[name] = {"id": svc_id, "type": "business_service"}
                created_count += 1
            time.sleep(0.5)

    # 4 ─ Link Cloud API → generic business services
    print("\n" + "=" * 60)
    print("4. LINKING: Cloud Reservation API → Business Services")
    print("=" * 60)
    cloud = tech_services["Cloud Reservation API (AWS)"]
    cloud_targets = [
        "Web Reservations",
        "Mobile Reservations",
        "In-Room Entertainment (WiFi, Streaming, Dining)",
        "Housekeeping Management",
    ]
    for biz_name in cloud_targets:
        biz = find_service(biz_name, is_business=True)
        if not biz:
            print(f"  [-] Business service not found: {biz_name}")
            continue
        print(f"  Cloud API → {biz_name}")
        resp = create_dependency(cloud, biz)
        if resp.status_code == 200:
            print(f"    [+] Linked.")
            linked_count += 1
        elif resp.status_code == 409:
            print(f"    [!] Already linked.")
        else:
            print(f"    [-] HTTP {resp.status_code}: {resp.text[:120]}")
        time.sleep(0.5)

    # 5 ─ Link IoT Controllers → generic business services
    print("\n" + "=" * 60)
    print("5. LINKING: IoT Local Key Controllers → Business Services")
    print("=" * 60)
    iot = tech_services["IoT Local Key Controllers"]
    iot_targets = [
        "Check-In / Digital Key",
        "Facilities Management",
        "In-Room Entertainment (WiFi, Streaming, Dining)",
    ]
    for biz_name in iot_targets:
        biz = find_service(biz_name, is_business=True)
        if not biz:
            print(f"  [-] Business service not found: {biz_name}")
            continue
        print(f"  IoT Controllers → {biz_name}")
        resp = create_dependency(iot, biz)
        if resp.status_code == 200:
            print(f"    [+] Linked.")
            linked_count += 1
        elif resp.status_code == 409:
            print(f"    [!] Already linked.")
        else:
            print(f"    [-] HTTP {resp.status_code}: {resp.text[:120]}")
        time.sleep(0.5)

    # 6 ─ Link IoT Controllers → per-hotel services (non-reservation)
    iot_hotel_skip = {"Web Reservations", "Mobile Reservations"}
    print("\n" + "=" * 60)
    print("6. LINKING: IoT Controllers → Per-Hotel Services")
    print("=" * 60)
    for hotel_name, hotel_svc in hotel_services.items():
        should_skip = any(skip in hotel_name for skip in iot_hotel_skip)
        if should_skip:
            continue
        print(f"  IoT Controllers → {hotel_name}")
        resp = create_dependency(iot, hotel_svc)
        if resp.status_code == 200:
            print(f"    [+] Linked.")
            linked_count += 1
        elif resp.status_code == 409:
            print(f"    [!] Already linked.")
        else:
            print(f"    [-] HTTP {resp.status_code}: {resp.text[:120]}")
        time.sleep(0.3)

    # 6b ─ Link Cloud API → per-hotel Web & Mobile services
    cloud_hotel_targets = {"Web Reservations", "Mobile Reservations"}
    print("\n" + "=" * 60)
    print("6b. LINKING: Cloud API → Per-Hotel Web & Mobile")
    print("=" * 60)
    for hotel_name, hotel_svc in hotel_services.items():
        if not any(target in hotel_name for target in cloud_hotel_targets):
            continue
        print(f"  Cloud API → {hotel_name}")
        resp = create_dependency(cloud, hotel_svc)
        if resp.status_code == 200:
            print(f"    [+] Linked.")
            linked_count += 1
        elif resp.status_code == 409:
            print(f"    [!] Already linked.")
        else:
            print(f"    [-] HTTP {resp.status_code}: {resp.text[:120]}")
        time.sleep(0.3)

    # 7 ─ Link per-hotel services → generic business services
    print("\n" + "=" * 60)
    print("7. LINKING: Per-Hotel → Generic Business Services")
    print("=" * 60)
    for hotel_name, hotel_svc in hotel_services.items():
        # Extract the service type from the hotel name (e.g., "Americus - Facilities Management" → "Facilities Management")
        for svc_type in PER_HOTEL_SERVICES:
            if svc_type in hotel_name:
                # Map per-hotel name to generic business service name
                generic_name = svc_type if svc_type != "Check-In / Digital Key" else "Check-In / Digital Key"
                # For In-Room, the generic name is longer
                if svc_type == "In-Room Entertainment":
                    generic_name = "In-Room Entertainment (WiFi, Streaming, Dining)"

                generic_svc = find_service(generic_name, is_business=True)
                if generic_svc:
                    # Link: Per-hotel → Generic (per-hotel supports the generic business capability)
                    print(f"  {hotel_name} → {generic_name}")
                    resp = create_dependency(hotel_svc, generic_svc)
                    if resp.status_code == 200:
                        print(f"    [+] Linked.")
                        linked_count += 1
                    elif resp.status_code == 409:
                        print(f"    [!] Already linked.")
                    else:
                        print(f"    [-] HTTP {resp.status_code}")
                break
        time.sleep(0.3)

    # 8 ─ Summary
    print("\n" + "=" * 60)
    print("SERVICE GRAPH SETUP COMPLETE")
    print("=" * 60)
    print(f"  Per-hotel business services created: {created_count}")
    print(f"  Dependencies linked:                {linked_count}")
    print(f"  Total services in graph:           {len(generic_biz) + created_count + 2}")
    print()
    print("Now the Service Graph shows:")
    print("  • All 6 generic business services")
    print("  • 2 technical services (Cloud API + IoT)")
    print(f"  • {created_count} per-hotel services ({len(LOCATIONS)} locations × {len(PER_HOTEL_SERVICES)} services)")
    print()
    print("When IoT controllers fail in a specific hotel, you'll see exactly which property is impacted.")
