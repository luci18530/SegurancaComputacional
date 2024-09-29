# auth_module.py

import logging
import random
import time
from datetime import datetime

# Configuração do logger
logger = logging.getLogger('auth_logger')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('auth.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Perfis de usuários simulados
USERS = {
    'admin': 'admin123',
    'user1': 'password1',
    'user2': 'password2',
}

def simulate_login(username, password, area='home'):
    """Simula uma tentativa de login."""
    current_time = datetime.now().hour
    if username in USERS and USERS[username] == password:
        # Login bem-sucedido
        logger.info(f'LOGIN_SUCCESS - User: {username} - Area: {area}')
        return True
    else:
        # Login falho
        logger.warning(f'LOGIN_FAILURE - User: {username} - Area: {area}')
        return False

def simulate_activity():
    """Simula atividades de login aleatórias."""
    usernames = list(USERS.keys()) + ['unknown_user']
    areas = ['home', 'dashboard', 'admin_panel', 'financial_data']
    for _ in range(20):  # Simular 20 tentativas
        username = random.choice(usernames)
        password = random.choice(['wrong_pass', USERS.get(username, 'wrong_pass')])
        area = random.choice(areas)
        simulate_login(username, password, area)
        time.sleep(random.uniform(0.1, 1))  # Pausa aleatória entre tentativas

if __name__ == '__main__':
    simulate_activity()
