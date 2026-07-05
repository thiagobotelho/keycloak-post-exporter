# Keycloak POST Exporter

Exporter Prometheus customizado em Python para monitorar o tempo de resposta do endpoint de token do Keycloak (POST para `/protocol/openid-connect/token`).

## 📌 Visão Geral
Este projeto executa periodicamente uma requisição POST no endpoint do Keycloak com `grant_type=client_credentials`, e expõe o tempo de resposta como métrica Prometheus (`external_keycloak_token_post_duration_seconds`).

Ideal para comparar com métricas internas de APM e validar gargalos reais do ambiente.

## 🧱 Estrutura
```
keycloak-post-exporter/
├── .github/workflows/docker-build.yml   # Pipeline de CI para build e push da imagem Docker
├── docker/Dockerfile                    # Dockerfile do exporter
├── manifests/                           # YAMLs de deploy no OpenShift
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── servicemonitor.yaml
│   └── secret.example
├── src/main.py                          # Código-fonte do exporter
├── .gitignore
└── README.md
```

## 🚀 Deploy no OpenShift
1. Crie o Secret sem gravar credenciais no Git:

```bash
oc create secret generic keycloak-auth-secret \
  --from-literal=CLIENT_ID="$CLIENT_ID" \
  --from-literal=CLIENT_SECRET="$CLIENT_SECRET" \
  --from-literal=KEYCLOAK_URL="$KEYCLOAK_URL"
```

2. Aplique os manifests:
```bash
oc apply -f manifests/
```
3. O Prometheus deve descobrir o serviço automaticamente via `ServiceMonitor`

## 📈 Métrica exposta
```promql
external_keycloak_token_post_duration_seconds
```

## 🛠 Variáveis de ambiente
- `CLIENT_ID` – Client ID do Keycloak
- `CLIENT_SECRET` – Client Secret do Keycloak
- `KEYCLOAK_URL` – endpoint completo de token
- `VERIFY_TLS` – valida certificados TLS; padrão `true`
- `CHECK_INTERVAL_SECONDS` – intervalo de coleta; padrão `60`
- `REQUEST_TIMEOUT_SECONDS` – timeout HTTP; padrão `10`

Essas variáveis são consumidas via `Secret` e injetadas no container.

## 📦 Build da imagem Docker
A imagem é construída automaticamente pelo GitHub Actions com base no workflow `.github/workflows/docker-build.yml`.

---

**Licença:** MIT
