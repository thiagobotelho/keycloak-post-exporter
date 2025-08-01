FROM python:3.11-slim

LABEL maintainer="thiagobotelho"

# Instala ferramentas de diagnóstico e bibliotecas necessárias
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        iputils-ping \
        dnsutils \
        netcat \
        ca-certificates && \
    pip install --no-cache-dir prometheus_client requests && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Cria diretório de trabalho
WORKDIR /app

# Copia o código
COPY main.py .

# Define o comando de inicialização
CMD ["python", "main.py"]
