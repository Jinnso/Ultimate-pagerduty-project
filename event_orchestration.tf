# event_orchestration.tf

# 1. Obtenemos los IDs de las prioridades configuradas en la cuenta
data "pagerduty_priority" "p1" {
  name = "P1"
}

data "pagerduty_priority" "p2" {
  name = "P2"
}

# 2. Orquestación para la API de Reservas en AWS
resource "pagerduty_event_orchestration_service" "aws_api_orchestration" {
  # Vinculamos esta orquestación al servicio técnico creado en services.tf
  service                                = pagerduty_service.cloud_reservation_api.id
  enable_event_orchestration_for_service = true

  set {
    id = "start"

    # Regla 1: Impacto Global (Todos los hoteles) -> Severidad Crítica y P1
    rule {
      label = "Incidente Mayor - Todos los hoteles afectados"
      condition {
        # Evaluamos si el JSON que envía Datadog contiene esta palabra clave
        expression = "event.custom_details.impact matches 'all_hotels'"
      }
      actions {
        severity = "critical"
        priority = data.pagerduty_priority.p1.id
        annotate = "¡ATENCIÓN! Orquestación automatizada: Falla masiva en múltiples propiedades."
      }
    }

    # Regla 2: Impacto Local (Un solo hotel) -> Severidad Alta y P2
    rule {
      label = "Incidente Local - Aislamiento en un hotel"
      condition {
        expression = "event.custom_details.impact matches 'single_hotel'"
      }
      actions {
        severity = "error"
        priority = data.pagerduty_priority.p2.id
        annotate = "Impacto aislado a nivel de sucursal local."
      }
    }
  }

  # Comportamiento por defecto si la alerta no coincide con las reglas anteriores
  catch_all {
    actions {
      severity = "info"
    }
  }
}