resource "pagerduty_escalation_policy" "local_hotel_infrastructure" {
  name        = "Local Hotel Infrastructure Escalation"
  description = "Escalamiento desde infraestructura local hacia soporte corporativo."
  num_loops   = 2
  teams = [pagerduty_team.corp_hotel_tech_ops.id]

  # Nivel 1: Apuntamos a un USUARIO específico del equipo técnico
  rule {
    escalation_delay_in_minutes = 15
    target {
      type = "user_reference"
      id   = pagerduty_user.hotel_tech_user_1.id
    }
  }

  # Nivel 2: Apuntamos a la ROTACIÓN 24x7 (Schedule) de Tier 1
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
  description = "Escalamiento para infraestructura Cloud. Va directo a DevOps."
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