FROM python:3.11-slim

# Instalar dependencias para PostgreSQL (incluyendo pg_isready)
RUN apt-get update && \
    apt-get install -y --no-install-recommends postgresql-client && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el proyecto incluyendo el script
COPY . .

# Comando de inicio modificado
CMD ["flask", "run", "--host=0.0.0.0"]