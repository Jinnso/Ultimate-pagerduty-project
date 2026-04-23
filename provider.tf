# provider.tf
terraform {
  required_providers {
    pagerduty = {
      source  = "PagerDuty/pagerduty"
      version = "~> 3.0" 
    }
  }
}

provider "pagerduty" {
  # Usamos la variable declarada
  token = var.pagerduty_token
}