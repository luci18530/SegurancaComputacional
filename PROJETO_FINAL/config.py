# config.py

# Configurações de segurança
MAX_FAILED_ATTEMPTS = 3
BUSINESS_HOURS = (9, 18)  # Das 9h às 18h
SENSITIVE_AREAS = ['admin_panel', 'financial_data']

# Configurações de alerta
ALERT_EMAIL = 'admin@gmail.com' # mudar p cada pessoa aqui do grupo
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'usuario@gmail.com' # mudar p cada pessoa aqui do grupo
SMTP_PASSWORD = 'teste12345'

# Configurações de relatório
REPORT_SCHEDULE = 'daily'  # 'daily' ou 'weekly'
