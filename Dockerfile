# Dockerfile für Quart mit Build-Tools
FROM python:3.12-slim

# Arbeitsverzeichnis
WORKDIR /app

# Systemabhängigkeiten für native Python-Module
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Python-Abhängigkeiten kopieren und installieren
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Quellcode kopieren
COPY . .

# Upgrading to the newest migration and running the service
CMD ["alembic", "upgrade", "heads"]
CMD ["uvicorn", "app:create_app", "--factory", "--host", "0.0.0.0", "--port", "5000"]