import os
import time
import threading
import requests
from prometheus_client import Gauge, start_http_server

# Variáveis de ambiente
KEYCLOAK_URL = os.environ.get("KEYCLOAK_URL")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

if not KEYCLOAK_URL or not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("Variáveis de ambiente KEYCLOAK_URL, CLIENT_ID e CLIENT_SECRET são obrigatórias.")

# Métrica Prometheus
keycloak_post_duration = Gauge(
    'external_keycloak_token_post_duration_seconds',
    'Tempo de resposta da requisição POST ao endpoint /token do Keycloak'
)

# Loop de medição
def measure_loop():
    while True:
        try:
            start = time.time()
            response = requests.post(
                KEYCLOAK_URL,
                data={
                    'grant_type': 'client_credentials',
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET
                },
                timeout=10,
                verify=False
            )
            duration = time.time() - start
            keycloak_post_duration.set(duration)
        except Exception as e:
            print(f"Erro ao fazer POST: {e}")
            keycloak_post_duration.set(-1)

        time.sleep(60)  # Intervalo de 1 minuto entre requisições

# Inicializa o exportador
if __name__ == '__main__':
    start_http_server(8000)  # Exposição HTTP na porta 8000
    threading.Thread(target=measure_loop).start()
