# Métricas de autenticação

## O que observar

O exporter mede client_credentials, não login interativo. REQUEST_TIMEOUT_SECONDS limita a requisição e VERIFY_TLS deve permanecer true. A prontidão de /metrics não prova sucesso da chamada ao Keycloak; use a métrica de sucesso e verifique falhas com certificado não confiável, timeout e credencial sintética inválida.

## Roteiro de leitura e validação

1. Leia o README e identifique o componente que recebe a configuração.
2. Confira namespaces, seletores, portas, identidades e dependências nos exemplos.
3. Ajuste apenas os campos necessários em um ambiente isolado; não use credenciais de produção.
4. Valide sintaxe e contratos locais antes de aplicar. Registre o resultado real separado deste guia.
5. Execute um caso permitido e um caso negado, conferindo a causa da resposta.
6. Defina reversão por recurso/arquivo e preserve dados persistentes antes de mudanças.

Os comentários dos manifests explicam escolhas; não comprovam disponibilidade do componente. Exemplos fora de entradas Kustomize não são implantados automaticamente.
