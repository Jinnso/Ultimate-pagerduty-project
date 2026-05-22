output "datadog_integration_key" {
  value     = pagerduty_service_integration.datadog_reservation_api.integration_key
  sensitive = true
}

output "grafana_prometheus_integration_key" {
  description = "Integration key for the IoT Key Controllers service (Prometheus/Grafana)"
  value       = pagerduty_service_integration.prometheus_key_controllers.integration_key
  sensitive   = true
}