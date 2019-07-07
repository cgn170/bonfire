provider "google" {
  project = "{{ project }}"
  region  = "{{ region }}"
  zone    = "{{ zone }}"
}

resource "google_monitoring_notification_channel" "basic" {
  display_name = "Test Notification Channel"
  type = "email"
  labels = {
    email_address = "cgn170@gmail.com"
  }
}

resource "google_monitoring_alert_policy" "alert_policy0" {
  display_name = "1 - Availability - Google Cloud HTTP/S Load Balancing Rule - Request count (filtered) [COUNT]"
  combiner = "OR"
  conditions {
    display_name = "Google Cloud HTTP/S Load Balancing Rule - Request count (filtered) [COUNT]"
    condition_threshold {
      filter = "metric.type=\"loadbalancing.googleapis.com/https/request_count\" resource.type=\"https_lb_rule\" metric.label.response_code!=\"200\""
      duration = "60s"
      comparison = "COMPARISON_GT"
      threshold_value = 1
      trigger {
          count = 1
      }
      aggregations {
        alignment_period = "60s"
        per_series_aligner = "ALIGN_RATE"
        cross_series_reducer = "REDUCE_COUNT"
      }
    }
  }
  documentation {
    content = "The load balancer rule $${condition.display_name} has generated this alert for the $${metric.display_name}."
  }
  notification_channels = [
      ["google_monitoring_notification_channel.basic"],
      ["google_monitoring_notification_channel.basic"],
  ]

  depends_on = ["google_monitoring_notification_channel.basic"]

}
