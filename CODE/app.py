from collections import defaultdict
from flask import Flask, render_template, request, redirect, url_for
import logging
from datetime import datetime
import re
import os
import config
from patterns import SQL_INJECTION_PATTERNS, XSS_PATTERNS, COMMAND_INJECTION_PATTERNS

FAILED_LOGINS = defaultdict(int)
BLOCKED_IPS = {}

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
    'professor1': 'password1',
    'student1': 'password1'
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
    if check_rate_limit(request.remote_addr):
        return 'Seu IP foi bloqueado temporariamente devido a tentativas de login falhas.', 403

    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        # Verificar tentativas de SQL injection, XSS e Command Injection separadamente
        sql_injection_detected = is_sql_injection(username) or is_sql_injection(password)
        xss_detected = is_xss_attempt(username) or is_xss_attempt(password)
        command_injection_detected = is_command_injection(username) or is_command_injection(password)

        extra = {'username': username, 'ip': request.remote_addr}

        if username not in USERS or USERS[username] != password:
            print('Login falho:', username)
            track_failed_login(request.remote_addr)

        if username in USERS and USERS[username] == password:
            if sql_injection_detected:
                logger.warning('LOGIN_SUCCESS_WITH_SQL_INJECTION_ATTEMPT', extra=extra)
            elif xss_detected:
                logger.warning('LOGIN_SUCCESS_WITH_XSS_INJECTION_ATTEMPT', extra=extra)
            elif command_injection_detected:
                logger.warning('LOGIN_SUCCESS_WITH_COMMAND_INJECTION_ATTEMPT', extra=extra)
            else:
                logger.info('LOGIN_SUCCESS', extra=extra)
                # Redirecionar para o painel de acordo com o papel do usuário
                if username == 'admin':
                    return redirect(url_for('admin_dashboard'))
                elif username.startswith('user'):
                    return redirect(url_for('user_dashboard'))
                elif username.startswith('professor'):
                    return redirect(url_for('professor_dashboard'))
                else:
                    return redirect(url_for('student_dashboard'))

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

""" rotas para controle de acesso por papeis """

@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/user_dashboard')
def user_dashboard():
    return render_template('user_dashboard.html')

@app.route('/professor_dashboard')
def professor_dashboard():
    return render_template('professor_dashboard.html')

@app.route('/student_dashboard')
def student_dashboard():
    return render_template('student_dashboard.html')


def check_rate_limit(ip_address):
    now = datetime.now()
    if ip_address in BLOCKED_IPS:
        if (now - BLOCKED_IPS[ip_address]).total_seconds() < 600:  # 10 minutos bloqueado
            return True
        else:
            del BLOCKED_IPS[ip_address]
    return False

def track_failed_login(ip_address):
    now = datetime.now()

    # Verificar se o IP já tem uma lista de tentativas, senão inicializar como lista vazia
    if not isinstance(FAILED_LOGINS[ip_address], list):
        FAILED_LOGINS[ip_address] = []

    # Limpar entradas antigas (tentativas com mais de 10 minutos)
    FAILED_LOGINS[ip_address] = [attempt for attempt in FAILED_LOGINS[ip_address] if (now - attempt).total_seconds() < 600]

    # Adicionar a nova tentativa
    FAILED_LOGINS[ip_address].append(now)
    print(f"Tentativas de login falhas para {ip_address}: {FAILED_LOGINS[ip_address]}")

    # Verifica se excedeu o limite de tentativas (5 falhas em 10 minutos)
    if len(FAILED_LOGINS[ip_address]) > 5:
        BLOCKED_IPS[ip_address] = now  # Bloqueia o IP por 10 minutos
        logger.warning(f"IP {ip_address} BLOQUEADO devido a múltiplas tentativas de login falhas.")
        FAILED_LOGINS[ip_address] = []  # Reseta as tentativas após bloquear


""" admin panel para logs """
# Simulando os usuários e suas funções
USERS_ROLES = {
    'admin': 'Administrador',
    'user1': 'Usuário',
    'professor1': 'Professor',
    'student1': 'Estudante',
}


if __name__ == '__main__':
    app.run(debug=True)
