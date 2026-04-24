# services.tf

# -------------------------------------------------------------------------
# 1. DATA SOURCES (Obteniendo los IDs de los proveedores de integración)
# -------------------------------------------------------------------------
data "pagerduty_vendor" "datadog" {
  name = "Datadog"
}

data "pagerduty_vendor" "prometheus" {
  name = "Prometheus"
}


# -------------------------------------------------------------------------
# 2. BUSINESS SERVICES (Capacidades de Negocio - Sin reglas de enrutamiento)
# -------------------------------------------------------------------------

resource "pagerduty_business_service" "web_reservations" {
  name             = "Web Reservations"
  description      = "Canal principal de reservas online para Acme Hotel."
  point_of_contact = "Director de E-Commerce"
}

resource "pagerduty_business_service" "digital_key" {
  name             = "Check-In / Digital Key"
  description      = "Acceso móvil y sistema de llaves digitales en las propiedades."
  point_of_contact = "VP de Operaciones Hoteleras"
}

resource "pagerduty_business_service" "mobile_reservations" {
  name             = "Mobile Reservations"
  description      = "Canal de reservas a través de la aplicación móvil."
  point_of_contact = "Director de E-Commerce"
}

resource "pagerduty_business_service" "in_room_entertainment" {
  name             = "In-Room Entertainment (WiFi, Streaming, Dining)"
  description      = "Servicios de red y entretenimiento para los huéspedes."
  point_of_contact = "VP de Operaciones Hoteleras"
}

resource "pagerduty_business_service" "housekeeping_management" {
  name             = "Housekeeping Management"
  description      = "Gestión de limpieza y estado de habitaciones."
  point_of_contact = "Director de Housekeeping"
}

resource "pagerduty_business_service" "facilities_management" {
  name             = "Facilities Management"
  description      = "Sistemas físicos, HVAC y mantenimiento del edificio."
  point_of_contact = "Director de Facilities corporativo"
}

# -------------------------------------------------------------------------
# 3. TECHNICAL SERVICES (Microservicios/Infra - Donde llegan las alertas)
# -------------------------------------------------------------------------

# Servicio Técnico: API de Reservas en la nube (AWS)
resource "pagerduty_service" "cloud_reservation_api" {
  name                    = "Cloud Reservation API (AWS)"
  description             = "Backend API gestionando la lógica de reservas."
  auto_resolve_timeout    = 14400 # Resuelve solo si no hay incidentes en 4 horas
  acknowledgement_timeout = 1800  # Escala si no se reconoce en 30 minutos

  # Aquí conectamos el servicio con la política de escalamiento corporativa
  # Asume que creaste una política para Tier 1 / Tier 2 DevOps en el paso anterior
  escalation_policy = pagerduty_escalation_policy.cloud_apps_escalation.id
    
  alert_creation = "create_alerts_and_incidents"

}

# Servicio Técnico: Controladores Locales de Llaves (IoT)
resource "pagerduty_service" "local_key_controllers" {
  name                    = "IoT Local Key Controllers"
  description             = "Controladores de puertas en los hoteles locales."
  auto_resolve_timeout    = 14400
  acknowledgement_timeout = 900 # 15 minutos (más crítico localmente)

  escalation_policy = pagerduty_escalation_policy.local_hotel_infrastructure.id
  alert_creation    = "create_alerts_and_incidents"

}


# -------------------------------------------------------------------------
# 4. INTEGRATIONS (Conectando el monitoreo externo)
# -------------------------------------------------------------------------

# Endpoint para recibir webhooks de Datadog en la API
resource "pagerduty_service_integration" "datadog_reservation_api" {
  name    = "Datadog Monitor - AWS API"
  service = pagerduty_service.cloud_reservation_api.id
  vendor  = data.pagerduty_vendor.datadog.id
}

resource "pagerduty_service_integration" "prometheus_key_controllers" {
  name    = "Prometheus Alertmanager - IoT Nodes"
  service = pagerduty_service.local_key_controllers.id
  vendor  = data.pagerduty_vendor.prometheus.id
}


# -------------------------------------------------------------------------
# 5. SERVICE DEPENDENCIES (La vista gráfica y de impacto)
# -------------------------------------------------------------------------

# Le decimos a PagerDuty: Si la API de AWS cae, el negocio de Reservas Web se impacta.
resource "pagerduty_service_dependency" "api_supports_web_reservations" {
  dependency {
    dependent_service {
      id   = pagerduty_business_service.web_reservations.id
      type = "business_service"
    }
    supporting_service {
      id   = pagerduty_service.cloud_reservation_api.id
      type = "service"
    }
  }
}

# Si los controladores locales caen, la experiencia de Digital Key se impacta.
resource "pagerduty_service_dependency" "iot_supports_digital_key" {
  dependency {
    dependent_service {
      id   = pagerduty_business_service.digital_key.id
      type = "business_service"
    }
    supporting_service {
      id   = pagerduty_service.local_key_controllers.id
      type = "service"
    }
  }
}