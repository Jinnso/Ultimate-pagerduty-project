# schedules.tf

# Note: This code assumes pagerduty_user resources have been already created
# in your teams_and_users.tf file.

# 1. Schedule for the Corporate Support Center (Tier 1)
resource "pagerduty_schedule" "tier1_support" {
  name      = "Tier 1 - Hotel Support Center 24x7"
  time_zone = "America/New_York" # Is essential to define the base time zone

  layer {
    name                         = "Weekly Rotation"
    start                        = "2026-05-01T08:00:00-04:00"
    rotation_virtual_start       = "2026-05-01T08:00:00-04:00"
    rotation_turn_length_seconds = 604800 # 1 week (7 days * 24 hrs * 3600 secs)

    users = [
      pagerduty_user.support_user_1.id,
      pagerduty_user.support_user_2.id,
      pagerduty_user.support_user_3.id
    ]
  }
}

# 2. Schedule for DevOps and Central Operations (Tier 2)
resource "pagerduty_schedule" "tier2_devops" {
  name      = "Tier 2 - Central Tech Eng & Ops 24x7"
  time_zone = "America/New_York"

  layer {
    name                         = "Daily Rotation"
    start                        = "2026-05-01T08:00:00-04:00"
    rotation_virtual_start       = "2026-05-01T08:00:00-04:00"
    rotation_turn_length_seconds = 86400 # 24 hours in seconds

    users = [
      pagerduty_user.devops_user_1.id,
      pagerduty_user.devops_user_2.id,
      pagerduty_user.devops_user_3.id
    ]
  }
}

# 3. Schedule for Hotel Tech Operations (Tier 2)
resource "pagerduty_schedule" "tier2_hotel_tech" {
  name      = "Tier 2 - Hotel Tech Ops 24x7"
  time_zone = "America/New_York"

  layer {
    name                         = "Weekly Rotation"
    start                        = "2026-05-01T08:00:00-04:00"
    rotation_virtual_start       = "2026-05-01T08:00:00-04:00"
    rotation_turn_length_seconds = 604800

    users = [
      pagerduty_user.hotel_tech_user_1.id,
      pagerduty_user.hotel_tech_user_2.id
    ]
  }
}