# main.py

import threading
from auth_module import simulate_activity
from monitoring_module import start_monitoring
from report_module import schedule_reports

def main():
    # Iniciar monitoramento
    monitoring_thread = threading.Thread(target=start_monitoring)
    monitoring_thread.daemon = True
    monitoring_thread.start()

    # Iniciar agendamento de relatórios
    reporting_thread = threading.Thread(target=schedule_reports)
    reporting_thread.daemon = True
    reporting_thread.start()

    # Simular atividades de login
    simulate_activity()

if __name__ == '__main__':
    main()
