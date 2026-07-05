FROM python:3.12-slim

LABEL maintainer="thiagobotelho"

# Boas práticas de runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1
    
# Cria diretório de trabalho
WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copia o código
COPY src/main.py .

# Executa sem root
RUN useradd -r -u 10001 -s /usr/sbin/nologin app && chown -R app:app /app
USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/metrics', timeout=2)"

# Define o comando de inicialização
CMD ["python", "main.py"]
