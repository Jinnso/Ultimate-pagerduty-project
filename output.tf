output "datadog_integration_key" {
  value     = pagerduty_integration.datadog_reservation_api.integration_key
  sensitive = true
}