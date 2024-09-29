# alert_module.py

import smtplib
from email.mime.text import MIMEText
from config import ALERT_EMAIL, SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD

def send_alert(message):
    """Envia um alerta por e-mail."""
    msg = MIMEText(message)
    msg['Subject'] = 'Alerta de Segurança'
    msg['From'] = SMTP_USER
    msg['To'] = ALERT_EMAIL

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, ALERT_EMAIL, msg.as_string())
        server.quit()
        print(f'Alerta enviado: {message}')
    except Exception as e:
        print(f'Falha ao enviar alerta: {e}')
