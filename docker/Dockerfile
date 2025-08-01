FROM python:3.11-slim

# Instala dependências do sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        iputils-ping \
        dnsutils \
        netcat-openbsd \
        ca-certificates \
        gnupg \
        apt-transport-https && \
    pip install --no-cache-dir prometheus_client requests && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copia código
WORKDIR /app
COPY src/main.py /app/main.py

# Define porta e comando de entrada
EXPOSE 8000
CMD ["python", "/app/main.py"]
