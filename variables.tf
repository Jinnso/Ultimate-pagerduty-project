# variables.tf
variable "pagerduty_token" {
  description = "General access API token for PagerDuty"
  type        = string
  sensitive   = true
}
