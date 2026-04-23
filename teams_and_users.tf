# Recurso de PagerDuty iterando sobre la lista combinada
resource "pagerduty_team" "local_hotel_teams" {
  # Convertimos la lista en un mapa donde la llave es el nombre del equipo
  for_each = { for team in local.hotel_teams : team.team_name => team }

  name        = each.value.team_name
  description = "Equipo de ${each.value.department} para el hotel ubicado en ${each.value.location}."
}

# --- EQUIPOS CORPORATIVOS FALTANTES ---

resource "pagerduty_team" "corp_hotel_support_center" {
  name        = "Hotel Support Center (Tier 1)"
  description = "Centro de soporte global 24x7 para todos los hoteles."
}

resource "pagerduty_team" "corp_hotel_tech_ops" {
  name        = "Hotel Tech Operations (Tier 2)"
  description = "Especialistas corporativos en WiFi, streaming y POS."
}

# --- USUARIOS REQUERIDOS PARA LOS HORARIOS (Schedules) ---
# Nota: PagerDuty requiere un email válido para crear usuarios. 
# Puedes usar correos ficticios bajo un mismo dominio para este ejercicio.

resource "pagerduty_user" "support_user_1" {
  name  = "Support User 1"
  email = "support1@acmehotel.local"
}
resource "pagerduty_user" "support_user_2" {
  name  = "Support User 2"
  email = "support2@acmehotel.local"
}
resource "pagerduty_user" "support_user_3" {
  name  = "Support User 3"
  email = "support3@acmehotel.local"
}

resource "pagerduty_user" "devops_user_1" {
  name  = "DevOps User 1"
  email = "devops1@acmehotel.local"
}
resource "pagerduty_user" "devops_user_2" {
  name  = "DevOps User 2"
  email = "devops2@acmehotel.local"
}
resource "pagerduty_user" "devops_user_3" {
  name  = "DevOps User 3"
  email = "devops3@acmehotel.local"
}

resource "pagerduty_user" "hotel_tech_user_1" {
  name  = "Hotel Tech User 1"
  email = "hoteltech1@acmehotel.local"
}
resource "pagerduty_user" "hotel_tech_user_2" {
  name  = "Hotel Tech User 2"
  email = "hoteltech2@acmehotel.local"
}