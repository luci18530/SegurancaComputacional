# monitoring_module.py

import time
import threading
import re
from datetime import datetime
from collections import defaultdict
from alert_module import send_alert
from config import MAX_FAILED_ATTEMPTS, BUSINESS_HOURS, SENSITIVE_AREAS

LOG_FILE = 'auth.log'

class LogMonitor:
    def __init__(self):
        self.failed_attempts = defaultdict(list)

    def monitor_logs(self):
        """Monitora o arquivo de log em tempo real."""
        with open(LOG_FILE, 'r') as file:
            # Move o cursor para o final do arquivo
            file.seek(0, 2)
            while True:
                line = file.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                self.process_log_line(line)

    def process_log_line(self, line):
        """Processa cada linha do log."""
        timestamp_str = line.split(' - ')[0]
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
        message = line.strip()

        # Verificar tentativas de login falhas
        if 'LOGIN_FAILURE' in message:
            username = re.search(r'User: (\w+)', message).group(1)
            self.failed_attempts[username].append(timestamp)
            self.check_failed_attempts(username)

        # Verificar acessos fora do horário comercial
        elif 'LOGIN_SUCCESS' in message:
            username = re.search(r'User: (\w+)', message).group(1)
            area = re.search(r'Area: (\w+)', message).group(1)
            self.check_off_hours_access(timestamp, username)
            self.check_sensitive_area_access(username, area)

    def check_failed_attempts(self, username):
        """Verifica múltiplas tentativas falhas em curto período."""
        attempts = self.failed_attempts[username]
        # Considerar tentativas nos últimos 5 minutos
        window = datetime.now() - attempts[0]
        if window.total_seconds() > 300:
            attempts.pop(0)
        if len(attempts) >= MAX_FAILED_ATTEMPTS:
            send_alert(f'Múltiplas tentativas de login falhas para o usuário {username}.')

    def check_off_hours_access(self, timestamp, username):
        """Verifica acessos fora do horário comercial."""
        if not BUSINESS_HOURS[0] <= timestamp.hour < BUSINESS_HOURS[1]:
            send_alert(f'Acesso fora do horário por {username} às {timestamp}.')

    def check_sensitive_area_access(self, username, area):
        """Verifica acesso a áreas sensíveis."""
        if area in SENSITIVE_AREAS and username != 'admin':
            send_alert(f'Usuário {username} tentou acessar área sensível: {area}.')

def start_monitoring():
    monitor = LogMonitor()
    monitoring_thread = threading.Thread(target=monitor.monitor_logs)
    monitoring_thread.daemon = True
    monitoring_thread.start()

if __name__ == '__main__':
    start_monitoring()
    while True:
        time.sleep(1)
