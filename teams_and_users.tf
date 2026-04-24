# teams_and_users.tf

locals {
  locations = [
    "Americus, GA",
    "Macon, GA",
    "Birmingham, AL",
    "Augusta, GA",
    "Panama City Beach, FL"
  ]

  departments = [
    "Guest Relations",
    "Housekeeping",
    "Facilities Engineering"
  ]

  hotel_teams = [
    for pair in setproduct(local.locations, local.departments) : {
      location   = pair[0]
      department = pair[1]
      team_name  = "${pair[0]} - ${pair[1]}"
    }
  ]
}

# Equipos Locales
resource "pagerduty_team" "local_hotel_teams" {
  for_each    = { for team in local.hotel_teams : team.team_name => team }
  name        = each.value.team_name
  description = "Equipo de ${each.value.department} para el hotel en ${each.value.location}."
}

# Equipos Corporativos
resource "pagerduty_team" "corp_hotel_support_center" {
  name        = "Hotel Support Center (Tier 1)"
  description = "Centro de soporte global 24x7."
}

resource "pagerduty_team" "corp_hotel_tech_ops" {
  name        = "Hotel Tech Operations (Tier 2)"
  description = "Especialistas corporativos en WiFi y sistemas POS."
}

# Usuarios para Soporte Tier 1
resource "pagerduty_user" "support_user_1" { 
  name  = "Support 1"
  email = "support1@live.cl" 
}
resource "pagerduty_user" "support_user_2" { 
  name  = "Support 2"
  email = "support2@live.cl" 
}
resource "pagerduty_user" "support_user_3" { 
  name  = "Support 3"
  email = "support3@live.cl" 
}

# Usuarios para DevOps Tier 2
resource "pagerduty_user" "devops_user_1" { 
  name  = "DevOps 1"
  email = "devops1@live.cl" 
}
resource "pagerduty_user" "devops_user_2" { 
  name  = "DevOps 2"
  email = "devops2@live.cl" 
}
resource "pagerduty_user" "devops_user_3" { 
  name  = "DevOps 3"
  email = "devops3@live.cl" 
}

# Usuarios para Tech Ops Tier 2
resource "pagerduty_user" "hotel_tech_user_1" { 
  name  = "Tech 1"
  email = "tech1@live.cl" 
}
resource "pagerduty_user" "hotel_tech_user_2" { 
  name  = "Tech 2"
  email = "tech2@live.cl" 
}