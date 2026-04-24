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
  # Vinculamos esta orquestación al servicio técnico creado en services.tf
  service                                = pagerduty_service.cloud_reservation_api.id
  enable_event_orchestration_for_service = true

  set {
    id = "start"

    # Regla 1: Impacto Global (Todos los huespedes) -> Severidad Crítica y P0
    rule {
      label = "Incidente Mayor - Todos los huespedes afectados"
      condition {
        # Evaluamos si el JSON que envía Datadog contiene esta palabra clave
        expression = "event.custom_details.impact matches 'all_guests'"
      }
      actions {
        severity = "critical"
        priority = data.pagerduty_priority.p0.id
        annotate = "INCIDENTE P0: Impacto total en la experiencia del huésped. Notificando a Stakeholders."
      }
    }
    # Regla 2: Impacto Global (Todos los hoteles) -> Severidad Crítica y P1
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

    # Regla 3: Impacto Local (Un solo hotel) -> Severidad Alta y P2
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

resource "pagerduty_event_orchestration_service" "iot_orchestration" {
  # Apuntamos esta orquestación al servicio que recibe las alertas de Grafana
  service = pagerduty_service.local_key_controllers.id
  enable_event_orchestration_for_service = true

  set {
    id = "start"

    # Regla: Si la alerta de Grafana dice "Critical", elevar a P1
    rule {
      label = "Incidente Crítico de IoT (Elevación a P1)"
      condition {
        # Grafana suele incluir el estado en el summary o en los labels
        expression = "event.summary matches part 'Critical' or event.custom_details.severity matches 'critical'"
      }
      actions {
        severity = "critical"
        priority = data.pagerduty_priority.p1.id
        annotate = "Orquestación: Alerta de Grafana evaluada y elevada a P1. Iniciando ChatOps y Jira."
      }
    }
  }

  catch_all {
    actions {
      severity = "warning"
    }
  }
}