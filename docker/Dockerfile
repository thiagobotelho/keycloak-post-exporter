FROM python:3.12-slim

LABEL maintainer="thiagobotelho"

# Boas práticas de runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1
    
# Cria diretório de trabalho
WORKDIR /app

# Somente dependências Python (sem apt)
RUN python -m pip install --upgrade pip setuptools wheel && \
    python -m pip install --no-cache-dir prometheus_client requests

# Copia o código
COPY src/main.py .

# Executa sem root
RUN useradd -r -u 10001 -s /usr/sbin/nologin app && chown -R app:app /app
USER app

# Define o comando de inicialização
CMD ["python", "main.py"]
