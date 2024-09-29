# config.py

# Configurações de segurança
MAX_FAILED_ATTEMPTS = 3
BUSINESS_HOURS = (9, 18)  # Das 9h às 18h
SENSITIVE_AREAS = ['admin_panel', 'financial_data']

# Configurações de alerta
ALERT_EMAIL = 'admin@example.com'
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
SMTP_USER = 'alert@example.com'
SMTP_PASSWORD = 'yourpassword'

# Configurações de relatório
REPORT_SCHEDULE = 'daily'  # 'daily' ou 'weekly'
