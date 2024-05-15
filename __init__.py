import os
os.environ["PYTHONPATH"] = "."


# Sample configuration.
# See https://prometheus.io/docs/alerting/configuration/ for documentation.

global:
  # The smarthost and SMTP sender used for mail notifications.
 # smtp_smarthost: 'localhost:25'
 # smtp_from: 'alertmanager@example.org'
 # smtp_auth_username: 'alertmanager'
 # smtp_auth_password: 'password'

# The directory from which notification templates are read.
templates: 
- '/etc/prometheus/alertmanager_templates/*.tmpl'

# The root route on which each incoming alert enters.
route:
  group_by: [alertname]
  group_wait: 10s
  group_interval: 1m
  repeat_interval: 300m
  receiver: telegram

# Inhibition rules allow to mute a set of alerts given that another alert is
# firing.
# We use this to mute any warning-level notifications if the same alert is 
# already critical.
#inhibit_rules:
#- source_match:
#    severity: 'critical'
#  target_match:
#    severity: 'warning'
#  # Apply inhibition if the alertname is the same.
#  equal: ['alertname', 'cluster', 'service']


receivers:
#- name: 'team-X-mails'
#  email_configs:
#  - to: 'team-X+alerts@example.org'

#- name: 'team-X-pager'
#  email_configs:
#  - to: 'team-X+alerts-critical@example.org'
#  pagerduty_configs:
#  - service_key: <team-X-key>

#- name: 'team-Y-mails'
#  email_configs:
#  - to: 'team-Y+alerts@example.org'

#- name: 'team-Y-pager'
#  pagerduty_configs:
#  - service_key: <team-Y-key>

#- name: 'team-DB-pager'
#  pagerduty_configs:
#  - service_key: <team-DB-key>

- name:  'telegram'
    #  text: "<!channel> \nsummary: {{ .CommonAnnotations.summary }}\ndescription: {{ .CommonAnnotations.description }}"
  telegram_configs:
  - bot_token: 'ТВОЙАПИТОКЕНБОТА'
    api_url: 'https://api.telegram.org'
    chat_id: ТВОЙЧАТАЙДИ
    parse_mode: 'HTML'
    send_resolved: true
    message: '{{ template "telegram.default" . }}' # тут темплейт указан объявленый выше в разделе templates
    # message: "событие Пинг монитоpинга:\n{{ .CommonLabels.severity }}\n{{ .CommonAnnotations.summary }}"