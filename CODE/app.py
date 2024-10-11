from flask import Flask, render_template, request, redirect, url_for
import logging
from datetime import datetime
import re
import config

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

# Padrões comuns de injeção SQL
SQL_INJECTION_PATTERNS = [
    r'(\bor\b|\band\b).*(=|like)',       # Uso de 'OR', 'AND' com operadores
    r'(\bunion\b|\bselect\b|\binsert\b|\bdelete\b|\bdrop\b)',  # Palavras-chave SQL
    r'(--|#)',                            # Comentários SQL
    r'(\*|;)',                            # Caracteres especiais
]

def is_sql_injection(input_str):
    """Verifica se a entrada corresponde a padrões de injeção SQL."""
    for pattern in SQL_INJECTION_PATTERNS:
        if re.search(pattern, input_str, re.IGNORECASE):
            return True
    return False

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        # Verificar tentativas de SQL injection
        sql_injection_detected = False
        if is_sql_injection(username) or is_sql_injection(password):
            sql_injection_detected = True

        extra = {'username': username, 'ip': request.remote_addr}

        if username in USERS and USERS[username] == password:
            # Login bem-sucedido
            if sql_injection_detected:
                logger.warning('LOGIN_SUCCESS_WITH_SQLI_ATTEMPT', extra=extra)
            else:
                logger.info('LOGIN_SUCCESS', extra=extra)
            return f'Bem-vindo, {username}!'
        else:
            # Login falho
            if sql_injection_detected:
                logger.warning('LOGIN_FAILURE_WITH_SQLI_ATTEMPT', extra=extra)
            else:
                logger.warning('LOGIN_FAILURE', extra=extra)
            return 'Credenciais inválidas.'
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
