resource "pagerduty_escalation_policy" "local_hotel_infrastructure" {
  name        = "Local Hotel Infrastructure Escalation"
  description = "Escalation from local infrastructure to corporate support."
  num_loops   = 2
  teams       = [pagerduty_team.corp_hotel_tech_ops.id]

  # Level 1: Target a specific USER from the tech team
  rule {
    escalation_delay_in_minutes = 15
    target {
      type = "user_reference"
      id   = pagerduty_user.hotel_tech_user_1.id
    }
  }

  # Level 2: Target the Tier 1 24x7 ROTATION (Schedule)
  rule {
    escalation_delay_in_minutes = 15
    target {
      type = "schedule_reference"
      id   = pagerduty_schedule.tier1_support.id
    }
  }
}

resource "pagerduty_escalation_policy" "cloud_apps_escalation" {
  name        = "Cloud Applications Escalation"
  description = "Escalation for Cloud infrastructure. Goes straight to DevOps."
  num_loops   = 2

  teams = [pagerduty_team.corp_hotel_tech_ops.id]

  rule {
    escalation_delay_in_minutes = 10
    target {
      type = "schedule_reference"
      id   = pagerduty_schedule.tier2_devops.id
    }
  }
}