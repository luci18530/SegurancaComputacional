import time
import threading
import re
from datetime import datetime
from collections import defaultdict
import logging
import config

LOG_FILE = config.AUTH_LOG_FILE

# Configurações de segurança
MAX_FAILED_ATTEMPTS = config.MAX_FAILED_ATTEMPTS
BUSINESS_HOURS = config.BUSINESS_HOURS



class LogMonitor:
    def __init__(self):
        self.failed_attempts = defaultdict(list)
        self.logger = logging.getLogger('alert_logger')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(config.ALERT_LOG_FILE)
        formatter = logging.Formatter('%(asctime)s - ALERT - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.test_logging()
    
    def test_logging(self):
        self.logger.info('Teste de logging iniciado com sucesso.')

    def monitor_logs(self):
        """Monitora o arquivo de log em tempo real."""
        try:
            with open(LOG_FILE, 'r') as file:
                # Move o cursor para o final do arquivo
                file.seek(0, 2)
                while True:
                    line = file.readline()
                    if not line:
                        time.sleep(0.1)
                        continue
                    self.process_log_line(line)
        except Exception as e:
            self.logger.error(f"Erro ao abrir o arquivo de log: {e}")
            print(f"Erro ao abrir o arquivo de log: {e}")

    def process_log_line(self, line):
        """Processa cada linha do log."""
        timestamp_str = line.split(' - ')[0]
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
        # Extrair nível, usuário, IP, mensagem
        match = re.match(r'.* - (\w+) - User: (.*) - IP: (.*) - Message: (.*)', line)
        if match:
            level = match.group(1)
            username = match.group(2)
            ip = match.group(3)
            message = match.group(4)
        else:
            return

        # Verificar tentativas de SQL injection
        if 'SQLI_ATTEMPT' in message:
            alert_message = f'Possível tentativa de SQL Injection pelo usuário {username} do IP {ip}.'
            print(alert_message)
            self.logger.warning(alert_message)

        if 'XSS_INJECTION' in (message):
            alert_message = f'Possível tentativa de Script Injection (XSS) pelo usuário {username} do IP {ip}.'
            print(alert_message)
            self.logger.warning(alert_message)

        if 'COMMAND_INJECTION' in (message):
            alert_message = f'Possível tentativa de Command Injection pelo usuário {username} do IP {ip}.'
            print(alert_message)
            self.logger.warning(alert_message)

        # Verificar tentativas de login falhas
        if 'LOGIN_FAILURE' in message:
            self.failed_attempts[username].append(timestamp)
            self.check_failed_attempts(username)
        elif 'LOGIN_SUCCESS' in message:
            self.check_off_hours_access(timestamp, username)

    def check_failed_attempts(self, username):
        """Verifica múltiplas tentativas falhas em curto período."""
        attempts = self.failed_attempts[username]
        now = datetime.now()
        # Considerar tentativas nos últimos 5 minutos
        attempts = [attempt for attempt in attempts if (now - attempt).total_seconds() <= 300]
        self.failed_attempts[username] = attempts
        if len(attempts) >= MAX_FAILED_ATTEMPTS:
            alert_message = f'Múltiplas tentativas de login falhas para o usuário {username}.'
            print(alert_message)
            self.logger.warning(alert_message)

    def check_off_hours_access(self, timestamp, username):
        """Verifica acessos fora do horário comercial."""
        if not BUSINESS_HOURS[0] <= timestamp.hour < BUSINESS_HOURS[1]:
            alert_message = f'Acesso fora do horário por {username} às {timestamp}.'
            print(alert_message)
            self.logger.warning(alert_message)

def start_monitoring():
    monitor = LogMonitor()
    monitoring_thread = threading.Thread(target=monitor.monitor_logs)
    monitoring_thread.daemon = True
    monitoring_thread.start()

if __name__ == '__main__':
    start_monitoring()
    while True:
        time.sleep(1)
