FROM python:3.11-slim

# Instala dependências
RUN pip install --no-cache-dir prometheus_client requests

# Copia código
WORKDIR /app
COPY src/main.py /app/main.py

# Define porta e comando de entrada
EXPOSE 8000
CMD ["python", "/app/main.py"]
