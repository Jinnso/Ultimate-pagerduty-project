# services.tf

# -------------------------------------------------------------------------
# 1. DATA SOURCES (Fetching integration vendor IDs)
# -------------------------------------------------------------------------
data "pagerduty_vendor" "datadog" {
  name = "Datadog"
}

data "pagerduty_vendor" "prometheus" {
  name = "Prometheus"
}


# -------------------------------------------------------------------------
# 2. BUSINESS SERVICES (Business Capabilities - No routing rules)
# -------------------------------------------------------------------------

resource "pagerduty_business_service" "web_reservations" {
  name             = "Web Reservations"
  description      = "Main online reservation channel for Acme Hotel."
  point_of_contact = "E-Commerce Director"
}

resource "pagerduty_business_service" "digital_key" {
  name             = "Check-In / Digital Key"
  description      = "Mobile access and digital key system across hotel properties."
  point_of_contact = "VP of Hotel Operations"
}

resource "pagerduty_business_service" "mobile_reservations" {
  name             = "Mobile Reservations"
  description      = "Reservation channel through the mobile app."
  point_of_contact = "E-Commerce Director"
}

resource "pagerduty_business_service" "in_room_entertainment" {
  name             = "In-Room Entertainment (WiFi, Streaming, Dining)"
  description      = "Network and entertainment services for hotel guests."
  point_of_contact = "VP of Hotel Operations"
}

resource "pagerduty_business_service" "housekeeping_management" {
  name             = "Housekeeping Management"
  description      = "Housekeeping and room status management."
  point_of_contact = "Housekeeping Director"
}

resource "pagerduty_business_service" "facilities_management" {
  name             = "Facilities Management"
  description      = "Physical systems, HVAC, and building maintenance."
  point_of_contact = "Corporate Facilities Director"
}

# -------------------------------------------------------------------------
# 3. TECHNICAL SERVICES (Microservices/Infra - Where alerts arrive)
# -------------------------------------------------------------------------

# Servicio Técnico: API de Reservas en la nube (AWS)
resource "pagerduty_service" "cloud_reservation_api" {
  name                    = "Cloud Reservation API (AWS)"
  description             = "Backend API managing reservation logic."
  auto_resolve_timeout    = 14400 # Resolves only if no incidents in 4 hours
  acknowledgement_timeout = 1800  # Escalates if not acknowledged in 30 minutes

  # Connect the service to the corporate escalation policy
  # Assumes you created a policy for Tier 1 / Tier 2 DevOps in the previous step
  escalation_policy = pagerduty_escalation_policy.cloud_apps_escalation.id

  alert_creation = "create_alerts_and_incidents"

}

# Servicio Técnico: Controladores Locales de Llaves (IoT)
resource "pagerduty_service" "local_key_controllers" {
  name                    = "IoT Local Key Controllers"
  description             = "Door controllers in local hotels."
  auto_resolve_timeout    = 14400
  acknowledgement_timeout = 900 # 15 minutes (more critical locally)

  escalation_policy = pagerduty_escalation_policy.local_hotel_infrastructure.id
  alert_creation    = "create_alerts_and_incidents"

}


# -------------------------------------------------------------------------
# 4. INTEGRATIONS (Connecting external monitoring)
# -------------------------------------------------------------------------

# Endpoint to receive Datadog webhooks for the API
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
# 5. SERVICE DEPENDENCIES (Visual and impact mapping)
# -------------------------------------------------------------------------

# Tell PagerDuty: If the AWS API goes down, the Web Reservations business is impacted.
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

# If local controllers go down, the Digital Key experience is impacted.
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