# report_module.py

import schedule
import time
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from config import REPORT_SCHEDULE

LOG_FILE = 'auth.log'

def generate_report():
    """Gera um relatório das atividades de login."""
    df = pd.read_csv(LOG_FILE, sep=' - ', header=None, engine='python')
    df.columns = ['Timestamp', 'Level', 'Message']
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Contagem de tentativas de login
    login_attempts = df['Level'].value_counts()

    # Gráfico de atividades
    df['Hour'] = df['Timestamp'].dt.hour
    activity = df.groupby('Hour').size()

    plt.figure(figsize=(10, 5))
    activity.plot(kind='bar')
    plt.title('Atividade de Login por Hora')
    plt.xlabel('Hora do Dia')
    plt.ylabel('Número de Tentativas')
    plt.savefig('login_activity_report.png')
    plt.close()

    print('Relatório gerado com sucesso.')

def schedule_reports():
    """Agenda a geração de relatórios."""
    if REPORT_SCHEDULE == 'daily':
        schedule.every().day.at("18:00").do(generate_report)
    elif REPORT_SCHEDULE == 'weekly':
        schedule.every().monday.at("09:00").do(generate_report)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    schedule_reports()
