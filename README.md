# Acme Hotel — SRE Incident Management with PagerDuty

End-to-end incident management system built for **Acme Hotel**, a regional hotel chain undergoing digital transformation. This project provisions a complete PagerDuty organization using Terraform Infrastructure as Code and provides Python automation scripts for external monitoring integrations, incident simulation, and service dependency mapping.

---

## Table of Contents

- [Customer Profile](#customer-profile)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Incident Severity Model](#incident-severity-model)
- [Terraform Resources](#terraform-resources)
- [Python Scripts](#python-scripts)
- [Integrations](#integrations)

---

## Customer Profile

**Acme Hotel** is a 100-year-old, family-owned hotel chain operating across the rural Southeast United States with over 50 hotels and 1,500 rooms. The company is in the early stages of cloud migration (partnering with AWS) and developing a new cloud-native guest reservation and online check-in application.

**First five modernized hotels:**
| City | State |
|------|-------|
| Americus | GA |
| Macon | GA |
| Birmingham | AL |
| Augusta | GA |
| Panama City Beach | FL |

**Key pain points addressed:**
- Rising alert volume from rapid technology change
- Guests reporting problems before support teams are aware
- Disconnect between corporate DevOps and local hotel teams
- No visibility into hotel facilities (HVAC, elevators, door access)
- Manual ticketing via spreadsheets and email

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    EXTERNAL MONITORING                       │
│  ┌──────────┐  ┌───────────────┐  ┌──────────────────────┐  │
│  │ Datadog   │  │ Grafana Cloud │  │ Python Simulation    │  │
│  │ Synthetic │  │ Alert Rules   │  │ Scripts             │  │
│  │ API Tests │  │ (Prometheus)  │  │ (Events v2 direct)  │  │
│  └────┬─────┘  └──────┬────────┘  └──────────┬───────────┘  │
│       │               │                      │              │
└───────┼───────────────┼──────────────────────┼──────────────┘
        │               │                      │
        ▼               ▼                      ▼
┌───────────────────────────────────────────────────────────────┐
│                    PAGERDUTY OPERATIONS CLOUD                   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              EVENT ORCHESTRATION                         │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐               │   │
│  │  │ P0 Rule  │  │ P1 Rule  │  │ P2 Rule  │               │   │
│  │  │all_guests│  │all_hotels│  │single_htl│               │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘               │   │
│  └───────┼─────────────┼─────────────┼──────────────────────┘   │
│          ▼              ▼             ▼                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                ESCALATION POLICIES                        │   │
│  │  Cloud Apps → Tier 2 DevOps (10min)                       │   │
│  │  Local Infra → Hotel Tech (15min) → Tier 1 Support (15m)  │   │
│  └──────────────────────────────────────────────────────────┘   │
│          │                                                       │
│          ▼                                                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │               INCIDENT WORKFLOWS                          │   │
│  │  Incident Triggered → Slack Channel → Jira Ticket         │   │
│  │  Incident Resolved → Archive Slack → Jeli Post-Mortem     │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
├── terraform/                          # IaC — all PagerDuty configuration
│   ├── provider.tf                     # PagerDuty provider (v3.x)
│   ├── variables.tf                    # Input variable declarations
│   ├── teams_and_users.tf              # 17 teams, 8 users, tags
│   ├── schedules.tf                    # 3 on-call rotations (24x7)
│   ├── escalation_policies.tf          # 2 escalation policies
│   ├── services.tf                     # 6 business + 2 technical services
│   ├── event_orchestration.tf          # P0/P1/P2 auto-classification rules
│   └── output.tf                       # Integration key outputs
│
├── scripts/                            # Python automation
│   ├── create_datadog_test.py          # Datadog Synthetic API Test
│   ├── create_grafana_alert.py         # Grafana alert rule (IoT)
│   ├── create_dependencies.py          # Service dependency mapping
│   ├── simulate_datadog_alert.py       # Trigger P0 incident (simulated)
│   ├── simulate_p1_alert.py            # Trigger P1 incident (simulated)
│   ├── simulate_p2_alert.py            # Trigger P2 incident (simulated)
│   ├── simulate_iot_alert.py           # Trigger IoT P1 (simulated)
│   ├── trigger_datadog_test.py         # Trigger real Datadog test → PD
│   ├── trigger_grafana_alert.py        # Trigger real Grafana alert → PD
│   ├── pdf_to_txt.py                   # Utility: PDF text extraction
│   └── generate_ppt.py                 # Utility: presentation generation
│
├── .env.example                        # Environment variable template
├── .gitignore
├── .terraform.lock.hcl                 # Provider lock file
└── requirements.txt                    # Python dependencies
```

---

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Terraform | ≥ 1.0 | Provision PagerDuty resources |
| Python | ≥ 3.10 | Run automation scripts |
| PagerDuty account | Trial or paid | Core platform |
| Datadog account | Trial | Synthetic monitoring (optional) |
| Grafana Cloud | Free tier | IoT alerting (optional) |

---

## Setup

### 1. Clone and install dependencies

```bash
git clone <repo-url>
cd pagerduty-proyect

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Configure environment variables

Copy the template and fill in your API keys:

```bash
cp .env.example .env
```

Required variables in `.env`:

```ini
PAGERDUTY_API_KEY=u+xxxxxxxxxxxx
PAGERDUTY_EVENTS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx        # Datadog integration key
PAGERDUTY_IOT_EVENTS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx     # Prometheus integration key
DATADOG_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DATADOG_APP_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DATADOG_SITE=us5.datadoghq.com
GRAFANA_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GRAFANA_URL=https://your-instance.grafana.net
GRAFANA_FOLDER_UID=xxxxxx
```

### 3. Deploy Terraform infrastructure

```bash
# Initialize Terraform
terraform init

# Review the plan
terraform plan

# Apply
terraform apply

# Get integration keys for .env
terraform output datadog_integration_key
terraform output grafana_prometheus_integration_key
```

### 4. Run setup scripts (in order)

```bash
# 1. Create Datadog Synthetic Test
python create_datadog_test.py

# 2. Create Grafana Alert Rule
python create_grafana_alert.py

# 3. Build service dependency map (per-hotel + generic)
python create_dependencies.py
```

---

## Usage

### Simulate incidents (bypass monitoring tools)

These scripts send PagerDuty Events v2 payloads directly — instant results, no external tool dependencies.

```bash
python simulate_datadog_alert.py    # P0: all guests impacted
python simulate_p1_alert.py         # P1: all hotels impacted
python simulate_p2_alert.py         # P2: single hotel impacted
python simulate_iot_alert.py        # P1: IoT controllers offline
```

### Trigger real monitoring alerts

These scripts use Datadog and Grafana APIs to trigger actual alerts that flow through the monitoring pipeline to PagerDuty. Requires active Datadog/Grafana accounts.

```bash
python trigger_datadog_test.py      # Run Datadog Synthetic Test → PD alert
python trigger_grafana_alert.py     # Fire Grafana alert → PD alert
```

### Utility scripts

```bash
python pdf_to_txt.py                # Extract text from PDF
python generate_ppt.py              # Generate project presentation
```

---

## How It Works

### End-to-End Incident Flow (P0 example)

```
1. simulate_datadog_alert.py
   └─ POST to events.pagerduty.com/v2/enqueue
      └─ custom_details.impact = "all_guests"

2. PagerDuty receives event → routes to "Cloud Reservation API (AWS)" service

3. Event Orchestration evaluates the event:
   └─ Rule: event.custom_details matches part 'all_guests'
      └─ Actions: severity = critical, priority = P0

4. Escalation Policy triggers:
   └─ Cloud Apps Escalation → Tier 2 DevOps schedule (10 minutes)

5. Incident Workflow fires:
   └─ Step 1: Create dedicated Slack channel
   └─ Step 2: Create Jira ticket with incident details

6. On resolution:
   └─ Slack channel archived
   └─ Jeli post-incident review generated
```

### IoT Incident Flow

```
1. simulate_iot_alert.py
   └─ POST event with summary = "FIRING: Digital lock controllers are offline."

2. PagerDuty receives → routes to "IoT Local Key Controllers" service

3. Event Orchestration:
   └─ Rule: event.summary matches part 'FIRING'
      └─ Actions: severity = critical, priority = P1

4. Escalation Policy:
   └─ Local Hotel Infrastructure → Hotel Tech User (15 min)
   └─ Then → Tier 1 Support schedule (15 min)
```

---

## Incident Severity Model

| Priority | Keyword | Trigger | Severity | Who is notified |
|----------|---------|---------|----------|-----------------|
| **P0** | `all_guests` | All guests across all hotels impacted | critical | Executive management |
| **P1** | `all_hotels` | Multiple hotels impacted | critical | Executive management |
| **P2** | `single_hotel` | One hotel property impacted | error | GM + Guest Experience |
| **P1 IoT** | `FIRING` (in summary) | IoT controllers offline | critical | Hotel Tech + Tier 1 Support |

The Event Orchestration rules use `matches part` for substring matching, so the keyword only needs to appear anywhere in the specified field.

---

## Terraform Resources

### Teams & Users

| Resource | Count | Details |
|----------|-------|---------|
| Local hotel teams | 15 | 5 locations × 3 departments |
| Corporate teams | 2 | Hotel Support Center (Tier 1) + Hotel Tech Operations (Tier 2) |
| Total users | 8 | 3 support + 3 DevOps + 2 hotel tech |
| Tags | 2 | Expertise_AWS, Language_Spanish |

### On-Call Schedules

| Schedule | Rotation | Users |
|----------|----------|-------|
| Tier 1 - Hotel Support Center | Weekly | 3 support users |
| Tier 2 - Central Tech Eng & Ops | Daily (24hr) | 3 DevOps users |
| Tier 2 - Hotel Tech Ops | Weekly | 2 hotel tech users |

### Services

| Type | Service | Monitoring |
|------|---------|------------|
| Technical | Cloud Reservation API (AWS) | Datadog |
| Technical | IoT Local Key Controllers | Grafana / Prometheus |
| Business | Web Reservations | — |
| Business | Mobile Reservations | — |
| Business | Check-In / Digital Key | — |
| Business | In-Room Entertainment | — |
| Business | Housekeeping Management | — |
| Business | Facilities Management | — |

### Service Dependencies (Service Graph)

```
Cloud Reservation API (AWS)  →  Web Reservations
Cloud Reservation API (AWS)  →  Mobile Reservations
Cloud Reservation API (AWS)  →  In-Room Entertainment
Cloud Reservation API (AWS)  →  Housekeeping Management
IoT Local Key Controllers     →  Check-In / Digital Key
IoT Local Key Controllers     →  Facilities Management
IoT Local Key Controllers     →  [20 per-hotel business services]
```

---

## Python Scripts

### Setup scripts (run once, in order)

| Script | Creates | External API |
|--------|---------|-------------|
| `create_datadog_test.py` | Datadog Synthetic HTTP Test (paused) | Datadog API v1 |
| `create_grafana_alert.py` | Grafana alert rule (always firing via `1 > 0`) | Grafana API |
| `create_dependencies.py` | 30 per-hotel business services + ~60 dependencies | PagerDuty API v2 |

### Simulation scripts (run anytime)

| Script | Priority | Event keyword | Target service |
|--------|----------|---------------|----------------|
| `simulate_datadog_alert.py` | P0 | `all_guests` | Cloud Reservation API |
| `simulate_p1_alert.py` | P1 | `all_hotels` | Cloud Reservation API |
| `simulate_p2_alert.py` | P2 | `single_hotel` | Cloud Reservation API |
| `simulate_iot_alert.py` | P1 IoT | `FIRING` (summary) | IoT Local Key Controllers |

### Real-trigger scripts (require active Datadog/Grafana)

| Script | What it does |
|--------|-------------|
| `trigger_datadog_test.py` | Unpauses + runs the Datadog Synthetic Test → Datadog alert → PagerDuty |
| `trigger_grafana_alert.py` | Fires test alert notification in Grafana → Prometheus → PagerDuty |

---

## Integrations

### External tools connected to PagerDuty

| Tool | Type | Integration Method | Service |
|------|------|-------------------|---------|
| **Datadog** | Monitoring | PagerDuty Service Integration (vendor) | Cloud Reservation API |
| **Grafana / Prometheus** | Monitoring | PagerDuty Service Integration (vendor) | IoT Local Key Controllers |
| **Slack** | ChatOps | Incident Workflow auto-create channel | All incidents |
| **Jira** | Ticketing | Incident Workflow auto-create ticket | All incidents |
| **Jeli** | Post-mortem | Incident Workflow on resolution | All incidents |
