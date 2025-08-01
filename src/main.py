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

print("Inicializando Keycloak POST Exporter na porta 8000...")
print(f"KEYCLOAK_URL: {KEYCLOAK_URL}")
print(f"CLIENT_ID: {CLIENT_ID}")

# Métrica Prometheus
keycloak_post_duration = Gauge(
    'external_keycloak_token_post_duration_seconds',
    'Tempo de resposta da requisição POST ao endpoint /token do Keycloak'
)

# Loop de medição
def measure_loop():
    while True:
        try:
            print("Iniciando requisição POST ao Keycloak...")
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

            print(f"POST realizado com sucesso: {duration:.3f} segundos - status {response.status_code}")
        except Exception as e:
            print(f"Erro ao fazer POST: {e}")
            keycloak_post_duration.set(-1)

        time.sleep(60)

if __name__ == '__main__':
    start_http_server(8000)
    threading.Thread(target=measure_loop).start()