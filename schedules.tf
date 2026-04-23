# schedules.tf

# Nota: Este código asume que tienes recursos pagerduty_user creados previamente
# en tu archivo teams_and_users.tf.

# 1. Horario para el Centro de Soporte Corporativo (Tier 1)
resource "pagerduty_schedulev2" "tier1_support" {
  name      = "Tier 1 - Hotel Support Center 24x7"
  time_zone = "America/New_York" # Es vital definir la zona horaria base

  layer {
    name                         = "Rotación Semanal"
    start                        = "2026-05-01T08:00:00-04:00"
    rotation_virtual_start       = "2026-05-01T08:00:00-04:00"
    rotation_turn_length_seconds = 604800 # 1 semana (7 días * 24 hrs * 3600 segs)

    users = [
      pagerduty_user.support_user_1.id,
      pagerduty_user.support_user_2.id,
      pagerduty_user.support_user_3.id
    ]
  }
}

# 2. Horario para DevOps y Operaciones Centrales (Tier 2)
resource "pagerduty_schedulev2" "tier2_devops" {
  name      = "Tier 2 - Central Tech Eng & Ops 24x7"
  time_zone = "America/New_York"

  layer {
    name                         = "Rotación Diaria"
    start                        = "2026-05-01T08:00:00-04:00"
    rotation_virtual_start       = "2026-05-01T08:00:00-04:00"
    rotation_turn_length_seconds = 86400 # 24 horas en segundos

    users = [
      pagerduty_user.devops_user_1.id,
      pagerduty_user.devops_user_2.id,
      pagerduty_user.devops_user_3.id
    ]
  }
}

# 3. Horario para Operaciones Tecnológicas de Hoteles (Tier 2)
resource "pagerduty_schedulev2" "tier2_hotel_tech" {
  name      = "Tier 2 - Hotel Tech Ops 24x7"
  time_zone = "America/New_York"

  layer {
    name                         = "Rotación Semanal"
    start                        = "2026-05-01T08:00:00-04:00"
    rotation_virtual_start       = "2026-05-01T08:00:00-04:00"
    rotation_turn_length_seconds = 604800

    users = [
      pagerduty_user.hotel_tech_user_1.id,
      pagerduty_user.hotel_tech_user_2.id
    ]
  }
}