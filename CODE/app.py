from flask import Flask, render_template, request, redirect, url_for
import logging
from datetime import datetime
import re
import config
from patterns import SQL_INJECTION_PATTERNS, XSS_PATTERNS, COMMAND_INJECTION_PATTERNS

app = Flask(__name__)

# Configuração do logger
logger = logging.getLogger('auth_logger')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(config.AUTH_LOG_FILE)

class CustomFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, 'username'):
            record.username = 'unknown'
        if not hasattr(record, 'ip'):
            record.ip = 'unknown'
        return super().format(record)

formatter = CustomFormatter('%(asctime)s - %(levelname)s - User: %(username)s - IP: %(ip)s - Message: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Perfis de usuários simulados
USERS = {
    'admin': 'admin123',
    'user1': 'password1',
    'user2': 'password2',
}

def is_sql_injection(input_str):
    """Verifica se a entrada corresponde a padrões de injeção SQL."""
    for pattern in SQL_INJECTION_PATTERNS:
        if re.search(pattern, input_str, re.IGNORECASE):
            print('SQL Injection detected:', input_str)
            return True
    return False

def is_xss_attempt(input_str):
    """Verifica se a entrada corresponde a padrões de XSS."""
    for pattern in XSS_PATTERNS:
        if re.search(pattern, input_str, re.IGNORECASE):
            print('XSS Attempt detected:', input_str)
            return True
    return False

def is_command_injection(input_str):
    """Verifica se a entrada corresponde a padrões de command injection."""
    for pattern in COMMAND_INJECTION_PATTERNS:
        if re.search(pattern, input_str, re.IGNORECASE):
            print('Command Injection detected:', input_str)
            return True
    return False

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        # Verificar tentativas de SQL injection, XSS e Command Injection separadamente
        sql_injection_detected = is_sql_injection(username) or is_sql_injection(password)
        xss_detected = is_xss_attempt(username) or is_xss_attempt(password)
        command_injection_detected = is_command_injection(username) or is_command_injection(password)

        extra = {'username': username, 'ip': request.remote_addr}

        if username in USERS and USERS[username] == password:
            if sql_injection_detected:
                logger.warning('LOGIN_SUCCESS_WITH_SQL_INJECTION_ATTEMPT', extra=extra)
            elif xss_detected:
                logger.warning('LOGIN_SUCCESS_WITH_XSS_INJECTION_ATTEMPT', extra=extra)
            elif command_injection_detected:
                logger.warning('LOGIN_SUCCESS_WITH_COMMAND_INJECTION_ATTEMPT', extra=extra)
            else:
                logger.info('LOGIN_SUCCESS', extra=extra)
            return f'Bem-vindo, {username}!'
        else:
            # Login falho
            if sql_injection_detected:
                logger.warning('LOGIN_FAILURE_WITH_SQL_INJECTION_ATTEMPT', extra=extra)
            elif xss_detected:
                logger.warning('LOGIN_FAILURE_WITH_XSS_INJECTION_ATTEMPT', extra=extra)
            elif command_injection_detected:
                logger.warning('LOGIN_FAILURE_WITH_COMMAND_INJECTION_ATTEMPT', extra=extra)
            else:
                logger.warning('LOGIN_FAILURE', extra=extra)
            return 'Credenciais inválidas.'
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
