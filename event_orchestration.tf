# event_orchestration.tf

# 1. Obtenemos los IDs de las prioridades configuradas en la cuenta
data "pagerduty_priority" "p0" {
  name = "P0"
}

data "pagerduty_priority" "p1" {
  name = "P1"
}

data "pagerduty_priority" "p2" {
  name = "P2"
}

# 2. Orquestación para la API de Reservas en AWS
resource "pagerduty_event_orchestration_service" "aws_api_orchestration" {
  service                                = pagerduty_service.cloud_reservation_api.id
  enable_event_orchestration_for_service = true

  set {
    id = "start"

    # Regla 1: Impacto Global (P0)
    rule {
      label = "Major Incident - All Guests Affected"
      condition {
        # Usamos 'matches part' en todo el bloque de detalles para no fallar por formato
        expression = "event.custom_details matches part 'all_guests'"
      }
      actions {
        severity = "critical"
        priority = data.pagerduty_priority.p0.id
        annotate = "P0 INCIDENT: Full impact on guest experience. Notifying stakeholders."
      }
    }

    # Regla 2: Impacto Múltiples Hoteles (P1)
    rule {
      label = "Major Incident - All Hotels Affected"
      condition {
        expression = "event.custom_details matches part 'all_hotels'"
      }
      actions {
        severity = "critical"
        priority = data.pagerduty_priority.p1.id
        annotate = "ATTENTION! Automated orchestration: Massive failure across multiple properties."
      }
    }

    # Regla 3: Impacto Local (P2)
    rule {
      label = "Local Incident - Isolated to a single hotel"
      condition {
        expression = "event.custom_details matches part 'single_hotel'"
      }
      actions {
        severity = "error"
        priority = data.pagerduty_priority.p2.id
        annotate = "Isolated impact at local branch level."
      }
    }
  }

  catch_all {
    actions {
      severity = "warning" # Cambiamos de info a warning para que al menos haga ruido si falla
    }
  }
}

# Orquestación para los controladores IoT (Grafana)
resource "pagerduty_event_orchestration_service" "iot_orchestration" {
  service                                = pagerduty_service.local_key_controllers.id
  enable_event_orchestration_for_service = true

  set {
    id = "start"

    # Regla: Atrapar la alerta de prueba de Grafana
    rule {
      label = "Critical IoT Incident (Elevation to P1)"
      condition {
        # Ahora busca exactamente las palabras que envía tu Grafana
        expression = "event.summary matches part 'FIRING' or event.summary matches part 'TestAlert'"
      }
      actions {
        severity = "critical"
        # ¡Asignamos P1 para gatillar Slack y Jira!
        priority = data.pagerduty_priority.p1.id
        annotate = "Orchestration: Grafana alert evaluated and elevated to P1. Starting ChatOps and Jira."
      }
    }
  }

  catch_all {
    actions {
      severity = "warning"
    }
  }
}