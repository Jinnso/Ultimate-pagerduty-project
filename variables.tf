# variables.tf
variable "pagerduty_token" {
  description = "API Token de acceso general para PagerDuty"
  type        = string
  sensitive   = true
}
