# Métricas de autenticação


O exporter mede client_credentials, não login interativo. REQUEST_TIMEOUT_SECONDS limita a requisição e VERIFY_TLS deve permanecer true. A prontidão de /metrics não prova sucesso da chamada ao Keycloak; use a métrica de sucesso e verifique falhas com certificado não confiável, timeout e credencial sintética inválida.

## Comparar medições

Associe o alvo do exporter ao realm/client corretos, sem registrar client_secret. Compare sucesso e duração da chamada externa com métricas internas do Keycloak e latência de rede. Uma falha client_credentials não diagnostica, sozinha, login via navegador, SAML, autorização do Argo CD ou mTLS entre proxies.
