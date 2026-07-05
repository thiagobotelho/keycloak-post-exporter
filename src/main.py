import logging
import os
import threading
import time
from dataclasses import dataclass

import requests
from prometheus_client import Counter, Gauge, start_http_server


logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(message)s",
)
LOGGER = logging.getLogger(__name__)

DURATION = Gauge(
    "external_keycloak_token_post_duration_seconds",
    "Duração da requisição ao endpoint de token do Keycloak.",
    ["instance", "namespace", "pod"],
)
SUCCESS = Gauge(
    "external_keycloak_token_post_success",
    "1 quando a última requisição retornou sucesso; 0 em caso de falha.",
    ["instance", "namespace", "pod"],
)
HTTP_STATUS = Gauge(
    "external_keycloak_token_post_http_status",
    "Código HTTP retornado pela última requisição.",
    ["instance", "namespace", "pod"],
)
ERRORS = Counter(
    "external_keycloak_token_post_errors_total",
    "Total de falhas ao consultar o endpoint de token.",
    ["instance", "namespace", "pod"],
)


def env_bool(name: str, default: bool = True) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Config:
    url: str
    client_id: str
    client_secret: str
    instance: str
    namespace: str
    pod: str
    verify_tls: bool
    interval: float
    timeout: float
    listen_port: int

    @classmethod
    def from_env(cls) -> "Config":
        required = {
            name: os.getenv(name)
            for name in ("KEYCLOAK_URL", "CLIENT_ID", "CLIENT_SECRET")
        }
        missing = [name for name, value in required.items() if not value]
        if missing:
            raise ValueError(f"Variáveis obrigatórias ausentes: {', '.join(missing)}")

        instance = os.getenv("HOSTNAME", "unknown")
        return cls(
            url=required["KEYCLOAK_URL"] or "",
            client_id=required["CLIENT_ID"] or "",
            client_secret=required["CLIENT_SECRET"] or "",
            instance=instance,
            namespace=os.getenv("NAMESPACE", "unknown"),
            pod=os.getenv("POD_NAME", instance),
            verify_tls=env_bool("VERIFY_TLS", True),
            interval=float(os.getenv("CHECK_INTERVAL_SECONDS", "60")),
            timeout=float(os.getenv("REQUEST_TIMEOUT_SECONDS", "10")),
            listen_port=int(os.getenv("LISTEN_PORT", "8000")),
        )


def measure_once(config: Config, session: requests.Session | None = None) -> bool:
    labels = (config.instance, config.namespace, config.pod)
    client = session or requests.Session()
    started = time.monotonic()
    try:
        response = client.post(
            config.url,
            data={
                "grant_type": "client_credentials",
                "client_id": config.client_id,
                "client_secret": config.client_secret,
            },
            timeout=config.timeout,
            verify=config.verify_tls,
        )
        duration = time.monotonic() - started
        DURATION.labels(*labels).set(duration)
        HTTP_STATUS.labels(*labels).set(response.status_code)
        response.raise_for_status()
        SUCCESS.labels(*labels).set(1)
        return True
    except requests.RequestException as exc:
        DURATION.labels(*labels).set(time.monotonic() - started)
        SUCCESS.labels(*labels).set(0)
        ERRORS.labels(*labels).inc()
        LOGGER.warning("Falha ao consultar o endpoint de token: %s", exc)
        return False


def measure_loop(config: Config) -> None:
    with requests.Session() as session:
        while True:
            measure_once(config, session)
            time.sleep(config.interval)


def main() -> None:
    config = Config.from_env()
    LOGGER.info(
        "Iniciando exporter na porta %s; destino=%s; verify_tls=%s",
        config.listen_port,
        config.url,
        config.verify_tls,
    )
    start_http_server(config.listen_port)
    threading.Thread(target=measure_loop, args=(config,), daemon=True).start()
    threading.Event().wait()


if __name__ == "__main__":
    main()
