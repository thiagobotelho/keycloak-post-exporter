import os
import time
import threading
import requests
import urllib3
from prometheus_client import Gauge, start_http_server

# Suprime warning de TLS quando verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Variáveis de ambiente obrigatórias
KEYCLOAK_URL = os.environ.get("KEYCLOAK_URL")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

# Labels extras para facilitar identificação no Prometheus/Grafana
INSTANCE = os.environ.get("HOSTNAME", "unknown")
NAMESPACE = os.environ.get("NAMESPACE", "unknown")
POD = os.environ.get("POD_NAME", INSTANCE)

# Validação mínima
if not KEYCLOAK_URL or not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("As variáveis de ambiente KEYCLOAK_URL, CLIENT_ID e CLIENT_SECRET são obrigatórias.")

# Logs iniciais
print("🔄 Inicializando Keycloak POST Exporter na porta 8000...")
print(f"🌐 KEYCLOAK_URL: {KEYCLOAK_URL}")
print(f"🔐 CLIENT_ID: {CLIENT_ID}")
print(f"📛 INSTANCE: {INSTANCE}, NAMESPACE: {NAMESPACE}, POD: {POD}")

# Métrica com labels
keycloak_post_duration = Gauge(
    'external_keycloak_token_post_duration_seconds',
    'Tempo de resposta da requisição POST ao endpoint /token do Keycloak',
    ['instance', 'namespace', 'pod']
)

# Loop de medição contínuo
def measure_loop():
    while True:
        try:
            print("➡️ Iniciando requisição POST ao Keycloak...")
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
            keycloak_post_duration.labels(INSTANCE, NAMESPACE, POD).set(duration)
            print(f"✅ POST bem-sucedido em {duration:.3f}s (status {response.status_code})")

        except Exception as e:
            print(f"❌ Erro ao fazer POST: {e}")
            keycloak_post_duration.labels(INSTANCE, NAMESPACE, POD).set(-1)

        time.sleep(60)

# Start HTTP server e inicia thread
if __name__ == '__main__':
    start_http_server(8000)
    threading.Thread(target=measure_loop, daemon=True).start()
    while True:
        time.sleep(3600)  # Mantém o processo ativo
