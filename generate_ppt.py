from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pathlib import Path

DARK = RGBColor(0x1A, 0x1A, 0x2E)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
ACCENT = RGBColor(0x05, 0xAC, 0x6A)
SUBTITLE_COLOR = RGBColor(0x66, 0x66, 0x88)

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

def add_bg(slide, color=DARK):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_textbox(slide, left, top, width, height, text, font_size=18,
                color=WHITE, bold=False, alignment=PP_ALIGN.LEFT, font_name="Calibri"):
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    return tf

def add_multi_text(slide, left, top, width, height, lines, font_size=14,
                   color=RGBColor(0x33, 0x33, 0x44), spacing=Pt(6)):
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = line
        p.font.size = Pt(font_size)
        p.font.color.rgb = color
        p.font.name = "Calibri"
        p.space_after = spacing
    return tf

def add_accent_line(slide, left, top, width):
    shape = slide.shapes.add_shape(
        1, Inches(left), Inches(top), Inches(width), Pt(4)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = ACCENT
    shape.line.fill.background()

def card_slide(prs, title, cards):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide, DARK)
    add_textbox(slide, 1.0, 0.5, 11, 0.7, title, 32, WHITE, True)
    add_accent_line(slide, 1.0, 1.3, 2)

    card_w = 3.5
    start_x = 1.0
    gap = 0.3

    for i, (header, body) in enumerate(cards):
        x = start_x + i * (card_w + gap)
        if x + card_w > 12:
            continue

        shape = slide.shapes.add_shape(
            5, Inches(x), Inches(1.8), Inches(card_w), Inches(4.5)
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(0x24, 0x24, 0x40)
        shape.line.fill.background()

        tf = shape.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = header
        p.font.size = Pt(18)
        p.font.color.rgb = ACCENT
        p.font.bold = True
        p.font.name = "Calibri"
        p.space_after = Pt(12)

        for line in body:
            p = tf.add_paragraph()
            p.text = f"• {line}"
            p.font.size = Pt(13)
            p.font.color.rgb = RGBColor(0xCC, 0xCC, 0xDD)
            p.font.name = "Calibri"
            p.space_after = Pt(6)

# ──────────────────────────────────────────────────
# SLIDE 1 – TITLE
# ──────────────────────────────────────────────────
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK)
add_textbox(slide, 1.5, 0.3, 10, 0.5, "PAGERDUTY", 14, ACCENT, True)
add_textbox(slide, 1.5, 1.8, 10, 1.5,
            "Acme Hotel\nSRE Incident Management", 48, WHITE, True)
add_accent_line(slide, 1.5, 3.5, 4)
add_textbox(slide, 1.5, 4.0, 10, 0.6,
            "Digital Transformation Through Modern Incident Response", 20, SUBTITLE_COLOR)
add_textbox(slide, 1.5, 4.8, 10, 0.5,
            "Presented to Acme Hotel Executive Leadership", 16, SUBTITLE_COLOR)
add_textbox(slide, 1.5, 6.5, 10, 0.4, "Confidential", 12, SUBTITLE_COLOR)

# ──────────────────────────────────────────────────
# SLIDE 2 – AGENDA
# ──────────────────────────────────────────────────
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK)
add_textbox(slide, 1.0, 0.5, 11, 0.7, "Agenda", 32, WHITE, True)
add_accent_line(slide, 1.0, 1.3, 2)

agenda = [
    ("1", "The Challenge", "Acme Hotel's operational pain points"),
    ("2", "The Solution", "PagerDuty Operations Cloud architecture"),
    ("3", "Team & Organization", "Global support model with local presence"),
    ("4", "Service Topology", "Business services mapped to infrastructure"),
    ("5", "Event Orchestration", "Automated P0/P1/P2 triage rules"),
    ("6", "Incident Workflows", "Slack + Jira + Jeli automation"),
    ("7", "Live Demo", "End-to-end incident simulation"),
    ("8", "Business Impact", "What this means for Acme Hotel"),
]
for i, (num, title, desc) in enumerate(agenda):
    y = 1.8 + i * 0.68
    add_textbox(slide, 1.5, y, 0.4, 0.5, num, 20, ACCENT, True)
    add_textbox(slide, 2.1, y, 3, 0.4, title, 18, WHITE, True)
    add_textbox(slide, 2.1, y + 0.3, 8, 0.35, desc, 14, SUBTITLE_COLOR)

# ──────────────────────────────────────────────────
# SLIDE 3 – THE CHALLENGE
# ──────────────────────────────────────────────────
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK)
add_textbox(slide, 1.0, 0.5, 11, 0.7, "The Challenge: Acme Hotel Before PagerDuty", 32, WHITE, True)
add_accent_line(slide, 1.0, 1.3, 2)

pain_points = [
    ("Rising Alert Volume",
     "Technology growth and cloud migration generated overwhelming alert noise across all operations teams. No prioritization or filtering mechanism existed."),
    ("Guests Reported Issues First",
     "Local hotel staff and support teams were unaware of problems until guests complained. Online check-in and digital key failures caused front-desk chaos."),
    ("Corporate-Local Disconnect",
     "During major incidents, corporate DevOps and local hotel teams operated in silos. No shared visibility, no coordinated response."),
    ("No Facilities Visibility",
     "Building systems (HVAC, elevators, fire safety) lacked modern APIs. Proactive maintenance was impossible; everything was reactive break/fix."),
    ("Manual Ticketing",
     "Incident tracking relied on spreadsheets, paper forms, and email. No audit trail, no analytics, no accountability."),
]
y = 1.7
for title, desc in pain_points:
    add_textbox(slide, 1.5, y, 3, 0.4, title, 18, ACCENT, True)
    add_textbox(slide, 1.5, y + 0.35, 10, 0.6, desc, 14, SUBTITLE_COLOR)
    y += 1.05

# ──────────────────────────────────────────────────
# SLIDE 4 – SEVERITY MODEL
# ──────────────────────────────────────────────────
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK)
add_textbox(slide, 1.0, 0.5, 11, 0.7, "Acme Hotel Severity Model", 32, WHITE, True)
add_accent_line(slide, 1.0, 1.3, 2)

severities = [
    ("P0", "ALL GUESTS IMPACTED", "Massive reservation failure.\nGuests cannot check in.\nAll executive management notified.", RGBColor(0xE0, 0x3E, 0x2D)),
    ("P1", "ALL HOTELS IMPACTED", "Multi-property failure.\nReservation engine degraded.\nExecutive management notified.", RGBColor(0xE6, 0x7E, 0x22)),
    ("P2", "SINGLE HOTEL IMPACTED", "Isolated property issue.\nLatency or partial outage.\nGM & Guest Experience notified.", RGBColor(0xF1, 0xC4, 0x0F)),
]
card_w = 3.5
for i, (level, label, desc, color) in enumerate(severities):
    x = 1.5 + i * 3.8
    shape = slide.shapes.add_shape(5, Inches(x), Inches(2.0), Inches(card_w), Inches(4.2))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(0x24, 0x24, 0x40)
    shape.line.fill.background()

    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = level
    p.font.size = Pt(48)
    p.font.color.rgb = color
    p.font.bold = True
    p.font.name = "Calibri"
    p.alignment = PP_ALIGN.CENTER

    p = tf.add_paragraph()
    p.text = label
    p.font.size = Pt(14)
    p.font.color.rgb = WHITE
    p.font.bold = True
    p.font.name = "Calibri"
    p.alignment = PP_ALIGN.CENTER
    p.space_after = Pt(16)

    p = tf.add_paragraph()
    p.text = desc
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(0xCC, 0xCC, 0xDD)
    p.font.name = "Calibri"
    p.alignment = PP_ALIGN.CENTER

# ──────────────────────────────────────────────────
# SLIDE 5 – THE SOLUTION
# ──────────────────────────────────────────────────
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK)
add_textbox(slide, 1.0, 0.5, 11, 0.7, "The Solution: PagerDuty Operations Cloud", 32, WHITE, True)
add_accent_line(slide, 1.0, 1.3, 2)

cards = [
    ("Core Configuration", [
        "Terraform Infrastructure as Code",
        "17 teams, 8 users, 24x7 coverage",
        "Business + Technical Services",
        "Service dependencies & topology",
        "Automated escalation policies",
    ]),
    ("Monitoring Ecosystem", [
        "Datadog Synthetic API Tests",
        "Grafana Cloud + Prometheus alerts",
        "Direct Events v2 integration",
        "Real-time health checks",
        "Proactive alerting before guests notice",
    ]),
    ("Automated Response", [
        "Event Orchestration (P0/P1/P2)",
        "Incident Workflows auto-trigger",
        "Slack dedicated channels",
        "Jira ticket auto-creation",
        "Jeli post-incident reviews",
    ]),
]
card_slide(prs, "The Solution: PagerDuty Operations Cloud", cards)

# ──────────────────────────────────────────────────
# SLIDE 6 – ARCHITECTURE
# ──────────────────────────────────────────────────
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK)
add_textbox(slide, 1.0, 0.5, 11, 0.7, "Project Architecture", 32, WHITE, True)
add_accent_line(slide, 1.0, 1.3, 2)

layers = [
    ("TERRAFORM IaC", "Full PagerDuty provisioning: Users, Teams, Schedules, Escalation\nPolicies, Services, Integrations, Event Orchestration, Dependencies", ACCENT),
    ("MONITORING", "Datadog Synthetic Tests + Grafana/Prometheus Alerts\n→ Events v2 API → PagerDuty Services", RGBColor(0x34, 0x94, 0xDB)),
    ("EVENT ORCHESTRATION", "Auto-classification rules: P0 (all_guests), P1 (all_hotels),\nP2 (single_hotel), IoT P1 (FIRING keyword match)", RGBColor(0xE0, 0x3E, 0x2D)),
    ("ESCALATION", "Tier 2 DevOps (10 min) + Tier 1 Support (15 min)\nLocal hotel tech → corporate escalation bridging", RGBColor(0xE6, 0x7E, 0x22)),
    ("INCIDENT WORKFLOWS", "Auto-create Slack channel + Jira ticket on incident trigger\nAuto-archive → Jeli post-mortem on resolution", RGBColor(0x9B, 0x59, 0xB6)),
]
y = 1.8
for name, desc, color in layers:
    add_textbox(slide, 1.5, y, 4, 0.4, name, 18, color, True)
    add_textbox(slide, 1.5, y + 0.4, 10, 0.55, desc, 13, SUBTITLE_COLOR)
    add_textbox(slide, 1.5, y + 0.95, 10, 0.05, "─" * 100, 10, RGBColor(0x33, 0x33, 0x55))
    y += 1.15

# ──────────────────────────────────────────────────
# SLIDE 7 – TEAM STRUCTURE
# ──────────────────────────────────────────────────
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK)
add_textbox(slide, 1.0, 0.5, 11, 0.7, "Team Organization & On-Call Model", 32, WHITE, True)
add_accent_line(slide, 1.0, 1.3, 2)

cols = [
    ("5 Hotel Locations", [
        "Americus, GA / Macon, GA",
        "Birmingham, AL / Augusta, GA",
        "Panama City Beach, FL",
        "",
        "3 departments per hotel:",
        "Guest Relations",
        "Housekeeping",
        "Facilities Engineering",
        "",
        "= 15 local hotel teams",
    ]),
    ("Corporate Teams", [
        "Hotel Support Center",
        "→ Tier 1, 24x7",
        "→ Weekly rotation",
        "",
        "Hotel Tech Operations",
        "→ Tier 2, 24x7",
        "→ Weekly rotation",
        "",
        "Central Tech Eng & Ops",
        "→ Tier 2, 24x7",
        "→ Daily rotation",
    ]),
    ("On-Call Schedules", [
        "Tier 1 Support: weekly",
        "Tier 2 DevOps: daily (24hr)",
        "Tier 2 Hotel Tech: weekly",
        "",
        "Escalation Policies:",
        "Cloud Apps → DevOps (10min)",
        "Local Infra → Tech → Support",
        "   Level 1: specific tech (15m)",
        "   Level 2: Tier 1 schedule (15m)",
    ]),
]
for i, (header, body) in enumerate(cols):
    x = 1.0 + i * 3.9
    shape = slide.shapes.add_shape(5, Inches(x), Inches(1.8), Inches(3.5), Inches(5.0))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(0x24, 0x24, 0x40)
    shape.line.fill.background()
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = header
    p.font.size = Pt(18)
    p.font.color.rgb = ACCENT
    p.font.bold = True
    p.font.name = "Calibri"
    p.space_after = Pt(10)
    for line in body:
        p = tf.add_paragraph()
        p.text = line if line else " "
        p.font.size = Pt(12)
        p.font.color.rgb = RGBColor(0xCC, 0xCC, 0xDD)
        p.font.name = "Calibri"
        p.space_after = Pt(4)

# ──────────────────────────────────────────────────
# SLIDE 8 – SERVICES
# ──────────────────────────────────────────────────
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK)
add_textbox(slide, 1.0, 0.5, 11, 0.7, "Service Topology", 32, WHITE, True)
add_accent_line(slide, 1.0, 1.3, 2)

biz_services = [
    "Web Reservations",
    "Mobile Reservations",
    "Check-In / Digital Key",
    "In-Room Entertainment (WiFi, Streaming, Dining)",
    "Housekeeping Management",
    "Facilities Management",
]
tech_services = [
    ("Cloud Reservation API (AWS)", "→ Datadog Synthetic Monitoring"),
    ("IoT Local Key Controllers", "→ Grafana / Prometheus Alerting"),
]

# Business services column
add_textbox(slide, 1.0, 1.8, 5, 0.4, "BUSINESS SERVICES (6)", 18, ACCENT, True)
shape = slide.shapes.add_shape(5, Inches(1.0), Inches(2.3), Inches(5.5), Inches(2.8))
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(0x24, 0x24, 0x40)
shape.line.fill.background()
tf = shape.text_frame
tf.word_wrap = True
for i, svc in enumerate(biz_services):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.text = f"• {svc}"
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(0xCC, 0xCC, 0xDD)
    p.font.name = "Calibri"
    p.space_after = Pt(8)

# Technical services column
add_textbox(slide, 7.0, 1.8, 5, 0.4, "TECHNICAL SERVICES (2)", 18, ACCENT, True)
shape = slide.shapes.add_shape(5, Inches(7.0), Inches(2.3), Inches(5.5), Inches(2.8))
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(0x24, 0x24, 0x40)
shape.line.fill.background()
tf = shape.text_frame
tf.word_wrap = True
for i, (name, monitoring) in enumerate(tech_services):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.text = f"• {name}"
    p.font.size = Pt(14)
    p.font.color.rgb = WHITE
    p.font.name = "Calibri"
    p.font.bold = True
    p.space_after = Pt(4)
    p2 = tf.add_paragraph()
    p2.text = f"  {monitoring}"
    p2.font.size = Pt(12)
    p2.font.color.rgb = SUBTITLE_COLOR
    p2.font.name = "Calibri"
    p2.space_after = Pt(12)

# Dependencies
add_textbox(slide, 1.0, 5.4, 11, 0.4, "SERVICE DEPENDENCIES", 18, ACCENT, True)
deps = [
    "Cloud Reservation API (AWS)  →  Web Reservations",
    "Cloud Reservation API (AWS)  →  Mobile Reservations",
    "IoT Local Key Controllers     →  Check-In / Digital Key",
    "IoT Local Key Controllers     →  Facilities Management",
]
add_multi_text(slide, 1.5, 5.9, 11, 1.2, deps, 14, RGBColor(0xCC, 0xCC, 0xDD))

# ──────────────────────────────────────────────────
# SLIDE 9 – EVENT ORCHESTRATION
# ──────────────────────────────────────────────────
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK)
add_textbox(slide, 1.0, 0.5, 11, 0.7, "Event Orchestration: Automated Incident Triage", 32, WHITE, True)
add_accent_line(slide, 1.0, 1.3, 2)

add_textbox(slide, 1.0, 1.8, 5.5, 0.4, "CLOUD RESERVATION API", 18, ACCENT, True)
orchestration_rules = [
    ("Rule 1: all_guests", "P0", "critical", "P0 INCIDENT: Full impact on guest experience."),
    ("Rule 2: all_hotels", "P1", "critical", "ATTENTION! Massive failure across multiple properties."),
    ("Rule 3: single_hotel", "P2", "error", "Isolated impact at local branch level."),
    ("Catch-all", "—", "warning", "Unmatched events get warning severity."),
]
y = 2.3
for i, (rule, prio, sev, note) in enumerate(orchestration_rules):
    colors = [ACCENT, RGBColor(0xE6, 0x7E, 0x22), RGBColor(0xF1, 0xC4, 0x0F), SUBTITLE_COLOR]
    add_textbox(slide, 1.5, y, 4.5, 0.3, rule, 14, colors[i], True)
    add_textbox(slide, 6.0, y, 1.5, 0.3, f"Priority: {prio}  |  Severity: {sev}", 12, WHITE)
    add_textbox(slide, 1.5, y + 0.3, 10, 0.25, note, 12, SUBTITLE_COLOR)
    y += 0.8

add_textbox(slide, 1.0, y + 0.3, 5.5, 0.4, "IOT KEY CONTROLLERS", 18, ACCENT, True)
add_textbox(slide, 1.5, y + 0.8, 4.5, 0.3, "Rule: summary matches FIRING or TestAlert", 14, ACCENT, True)
add_textbox(slide, 6.0, y + 0.8, 1.5, 0.3, "Priority: P1  |  Severity: critical", 12, WHITE)
add_textbox(slide, 1.5, y + 1.1, 10, 0.25, "Grafana alert evaluated → automatically elevated to P1 → ChatOps + Jira triggered.", 12, SUBTITLE_COLOR)

# ──────────────────────────────────────────────────
# SLIDE 10 – INTEGRATIONS
# ──────────────────────────────────────────────────
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK)
add_textbox(slide, 1.0, 0.5, 11, 0.7, "Monitoring & Integration Ecosystem", 32, WHITE, True)
add_accent_line(slide, 1.0, 1.3, 2)

cards = [
    ("Datadog", [
        "Synthetic API Test",
        "HTTP health check every 60s",
        "Targets Cloud Reservation API",
        "Alerts via Events v2 → PD",
        "env:production, team:tech_ops",
    ]),
    ("Grafana + Prometheus", [
        "IoT Key Controllers alert",
        "Math expression: 1 > 0",
        "Always-firing for demo",
        "Alerts via Prometheus → PD",
        "Label: severity=critical",
    ]),
    ("Direct Simulation", [
        "Python scripts via Events v2",
        "P0: impact = all_guests",
        "P1: impact = all_hotels",
        "P2: impact = single_hotel",
        "IoT: summary = FIRING: ...",
    ]),
]
card_slide(prs, "Monitoring & Integration Ecosystem", cards)

# ──────────────────────────────────────────────────
# SLIDE 11 – INCIDENT WORKFLOWS
# ──────────────────────────────────────────────────
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK)
add_textbox(slide, 1.0, 0.5, 11, 0.7, "Modern Incident Response: Workflows", 32, WHITE, True)
add_accent_line(slide, 1.0, 1.3, 2)

add_textbox(slide, 1.0, 1.8, 11, 0.5,
            "When a P0/P1/P2 incident is triggered by Event Orchestration:", 18, WHITE)

steps = [
    ("1", "Incident Created", "Event Orchestration auto-classifies severity and priority."),
    ("2", "Slack Channel", "Dedicated incident channel created automatically for real-time collaboration."),
    ("3", "Jira Ticket", "Ticket auto-created with incident details, priority, and PagerDuty link."),
    ("4", "Escalation", "Escalation policy notifies the correct on-call schedule within 10-15 minutes."),
    ("5", "Resolution", "Incident resolved → Slack channel archived → Jeli post-incident review triggered."),
]
y = 2.5
for num, title, desc in steps:
    add_textbox(slide, 1.5, y, 0.5, 0.5, num, 24, ACCENT, True)
    add_textbox(slide, 2.2, y, 2.5, 0.4, title, 18, WHITE, True)
    add_textbox(slide, 2.2, y + 0.35, 9, 0.35, desc, 14, SUBTITLE_COLOR)
    y += 0.85

# Jeli highlight
shape = slide.shapes.add_shape(5, Inches(1.5), Inches(y + 0.3), Inches(10), Inches(1.0))
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(0x1E, 0x3A, 0x1E)
shape.line.fill.background()
tf = shape.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Jeli Post-Incident Review"
p.font.size = Pt(18)
p.font.color.rgb = ACCENT
p.font.bold = True
p.font.name = "Calibri"
p = tf.add_paragraph()
p.text = "Automated post-mortem: timeline reconstruction, impact analysis, action items, lessons learned."
p.font.size = Pt(14)
p.font.color.rgb = RGBColor(0xCC, 0xCC, 0xDD)
p.font.name = "Calibri"

# ──────────────────────────────────────────────────
# SLIDE 12 – TERRAFORM
# ──────────────────────────────────────────────────
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK)
add_textbox(slide, 1.0, 0.5, 11, 0.7, "Infrastructure as Code: Terraform", 32, WHITE, True)
add_accent_line(slide, 1.0, 1.3, 2)

cards = [
    ("Terraform Files", [
        "provider.tf – PagerDuty provider",
        "variables.tf – Token management",
        "teams_and_users.tf – 17 teams, 8 users",
        "schedules.tf – 3 on-call rotations",
        "escalation_policies.tf – 2 policies",
        "services.tf – 6 biz + 2 tech services",
        "event_orchestration.tf – P0/P1/P2",
        "output.tf – Integration keys",
    ]),
    ("Python Scripts", [
        "create_datadog_test.py",
        "create_grafana_alert.py",
        "create_dependencies.py",
        "simulate_datadog_alert.py (P0)",
        "simulate_p1_alert.py (P1)",
        "simulate_p2_alert.py (P2)",
        "simulate_iot_alert.py (IoT P1)",
        "pdf_to_txt.py (utility)",
    ]),
    ("Key Benefits", [
        "Reproducible: deploy in minutes",
        "Version-controlled: git history",
        "Auditable: every change tracked",
        "Modular: separate concerns",
        "Scalable: add hotels via locals {}",
        "",
        "PagerDuty provider v3.32.3",
        "Constraint: ~> 3.0",
    ]),
]
card_slide(prs, "Infrastructure as Code: Terraform", cards)

# ──────────────────────────────────────────────────
# SLIDE 13 – DEMO FLOW
# ──────────────────────────────────────────────────
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK)
add_textbox(slide, 1.0, 0.5, 11, 0.7, "Live Demo: Incident Simulation", 32, WHITE, True)
add_accent_line(slide, 1.0, 1.3, 2)

demo_steps = [
    ("python simulate_datadog_alert.py", "P0", "all_guests → critical severity → all executives notified"),
    ("python simulate_p1_alert.py", "P1", "all_hotels → critical severity → executive escalation"),
    ("python simulate_p2_alert.py", "P2", "single_hotel → error severity → GM + Guest Experience"),
    ("python simulate_iot_alert.py", "P1 IoT", "FIRING keyword → IoT orchestration → P1 elevation"),
]
y = 2.0
for cmd, level, result in demo_steps:
    colors = {
        "P0": RGBColor(0xE0, 0x3E, 0x2D),
        "P1": RGBColor(0xE6, 0x7E, 0x22),
        "P1 IoT": RGBColor(0xE6, 0x7E, 0x22),
        "P2": RGBColor(0xF1, 0xC4, 0x0F),
    }
    add_textbox(slide, 1.5, y, 0.8, 0.4, level, 22, colors[level], True)
    add_textbox(slide, 2.5, y, 5, 0.4, cmd, 16, WHITE, False, font_name="Courier New")
    add_textbox(slide, 2.5, y + 0.35, 9, 0.35, result, 13, SUBTITLE_COLOR)
    y += 0.95

add_textbox(slide, 1.5, y + 0.5, 10, 0.5,
            "Each script sends a PagerDuty Events v2 payload → Orchestration rules match → "
            "Incident Workflows trigger Slack + Jira", 16, WHITE, True)

# ──────────────────────────────────────────────────
# SLIDE 14 – BUSINESS IMPACT
# ──────────────────────────────────────────────────
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK)
add_textbox(slide, 1.0, 0.5, 11, 0.7, "Business Impact for Acme Hotel", 32, WHITE, True)
add_accent_line(slide, 1.0, 1.3, 2)

outcomes = [
    ("Before", "After"),
    ("Guests reported problems first", "Monitoring detects issues before guests notice"),
    ("Spreadsheets & email for incidents", "Automated Jira tickets with full audit trail"),
    ("Corporate & local teams in silos", "Shared Slack channels + coordinated response"),
    ("No incident prioritization", "P0/P1/P2 auto-classification via orchestration"),
    ("Reactive maintenance only", "Proactive monitoring of digital key & facilities"),
    ("No post-incident learning", "Jeli post-mortems capture lessons learned"),
    ("Manual configuration", "Terraform IaC: reproducible, version-controlled"),
]

from pptx.util import Inches
table.columns[0].width = Inches(5.5)
table.columns[1].width = Inches(5.5)

for row_idx, (before, after) in enumerate(outcomes):
    for col_idx, text in enumerate([before, after]):
        cell = table.cell(row_idx, col_idx)
        cell.text = text
        for paragraph in cell.text_frame.paragraphs:
            paragraph.font.size = Pt(14)
            paragraph.font.name = "Calibri"
            if row_idx == 0:
                paragraph.font.bold = True
                paragraph.font.color.rgb = ACCENT if col_idx == 1 else RGBColor(0xE0, 0x3E, 0x2D)
            else:
                paragraph.font.color.rgb = ACCENT if col_idx == 1 else SUBTITLE_COLOR

# ──────────────────────────────────────────────────
# SLIDE 15 – NEXT STEPS
# ──────────────────────────────────────────────────
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK)
add_textbox(slide, 1.0, 0.5, 11, 0.7, "Next Steps", 32, WHITE, True)
add_accent_line(slide, 1.0, 1.3, 2)

next_steps = [
    "Deploy remaining 45 hotel properties into the PagerDuty organization",
    "Integrate building management systems (HVAC, elevators, fire safety) via custom webhooks",
    "Expand monitoring coverage: New Relic and Dynatrace for legacy applications",
    "Configure stakeholder notification rules for P0/P1 executive alerts",
    "Implement Runbook Automation for common incident response procedures",
    "Roll out PagerDuty Mobile for frontline hotel staff",
    "Establish monthly SRE review cadence with Jeli analytics",
]
add_multi_text(slide, 1.5, 1.8, 10, 4, next_steps, 16, RGBColor(0xCC, 0xCC, 0xDD), Pt(10))

# ──────────────────────────────────────────────────
# SLIDE 16 – AI-POWERED DEVELOPMENT
# ──────────────────────────────────────────────────
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK)
add_textbox(slide, 1.0, 0.5, 11, 0.7, "AI-Powered Project Development", 32, WHITE, True)
add_accent_line(slide, 1.0, 1.3, 2)

add_textbox(slide, 1.0, 1.8, 11, 0.5,
            "This entire project was accelerated using AI-assisted development:", 18, WHITE)

ai_cards = [
    ("Terraform IaC", [
        "Teams, users, schedules, escalation",
        "policies, services, integrations",
        "and event orchestration rules",
        "generated and iterated with AI",
        "Code validated for provider v3.32.3",
    ]),
    ("Python Automation", [
        "7 simulation & setup scripts",
        "Datadog Synthetic Test creation",
        "Grafana alert rule provisioning",
        "P0/P1/P2/IoT incident simulation",
        "PDF text extraction utility",
    ]),
    ("Quality & Delivery", [
        "Spanish → English translation",
        "across 14 source files",
        "Syntax validation on every script",
        "Requirements gap analysis vs SOW",
        "Professional PPT auto-generation",
    ]),
]
card_slide(prs, "AI-Powered Project Development", ai_cards)

add_textbox(slide, 1.0, 6.5, 11, 0.6,
            "AI acted as a force multiplier: co-designing architecture, writing & validating code, "
            "translating content, identifying gaps, and generating executive-ready deliverables.",
            14, SUBTITLE_COLOR)

# ──────────────────────────────────────────────────
# SLIDE 17 – THANK YOU
# ──────────────────────────────────────────────────
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK)
add_textbox(slide, 1.5, 2.0, 10, 1.5, "Thank You", 56, WHITE, True)
add_accent_line(slide, 1.5, 3.5, 4)
add_textbox(slide, 1.5, 4.0, 10, 0.6,
            "Acme Hotel is ready for its digital future.", 20, SUBTITLE_COLOR)
add_textbox(slide, 1.5, 4.6, 10, 0.5, "Questions?", 24, ACCENT, True)

# ──────────────────────────────────────────────────
# SAVE
# ──────────────────────────────────────────────────
output = Path(__file__).parent / "Acme_Hotel_PagerDuty_Presentation.pptx"
prs.save(str(output))
print(f"[+] Presentation saved: {output}")
