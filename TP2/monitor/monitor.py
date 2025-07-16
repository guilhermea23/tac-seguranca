import re
from datetime import datetime
import time

log_file = "/logs/access.log"
output_file = "/logs/suspicious_activity.log"
pattern = re.compile(
    r"(\bUNION\b|\bSELECT\b|\bDROP\b|\bINSERT\b|--|#|\bOR\b\s+1=1)", re.IGNORECASE
)

print("[INFO] Monitoramento iniciado em", datetime.now())

while True:
    try:
        with open(log_file, "r") as file:
            for line in file:
                if pattern.search(line):
                    alert_msg = f"[SUSPEITO - {datetime.now()}] {line.strip()}\n"
                    print(alert_msg, end="")  # Mostra no console
                    with open(output_file, "a") as f:
                        f.write(alert_msg)  # Registra no arquivo
        time.sleep(10)
    except FileNotFoundError:
        error_msg = f"[ERRO {datetime.now()}] Arquivo de log não encontrado. Tentando novamente...\n"
        print(error_msg, end="")
        with open(output_file, "a") as f:
            f.write(error_msg)
        time.sleep(10)
