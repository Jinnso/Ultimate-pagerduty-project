# escalation_policies.tf

# 1. Política para incidentes en un hotel local (Ej. Falla de WiFi)
resource "pagerduty_escalation_policy" "local_hotel_infrastructure" {
  name        = "Local Hotel Infrastructure Escalation"
  description = "Escalamiento desde el equipo de facilidades local hacia el soporte corporativo Tier 1 y luego Tier 2."
  num_loops   = 2 # Si nadie responde al final, vuelve a empezar el ciclo

  # Nivel 1: Equipo Local de Facilidades (Inmediato)
  rule {
    escalation_delay_in_minutes = 15 # Si no responden en 15 min, sube al Nivel 2
    target {
      type = "team_reference"
      # Aquí referenciarías el ID del equipo local creado en teams.tf
      id = pagerduty_team.local_hotel_teams["Augusta, GA - Facilities Engineering"].id
    }
  }

  # Nivel 2: Soporte Corporativo Tier 1 (Hotel Support Center)
  rule {
    escalation_delay_in_minutes = 15
    target {
      type = "team_reference"
      # Asumiendo que creaste este equipo corporativo
      id = pagerduty_team.corp_hotel_support_center.id
    }
  }

  # Nivel 3: Operaciones Tecnológicas Tier 2
  rule {
    escalation_delay_in_minutes = 30
    target {
      type = "team_reference"
      id   = pagerduty_team.corp_hotel_tech_ops.id
    }
  }
}
resource "pagerduty_escalation_policy" "cloud_apps_escalation" {
  name      = "Cloud Applications Escalation"
  num_loops = 2

  rule {
    escalation_delay_in_minutes = 10
    target {
      type = "schedule_reference"
      id   = pagerduty_schedule.tier2_devops.id 
    }
  }
}