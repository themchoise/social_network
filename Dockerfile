
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DJANGO_SETTINGS_MODULE=socialnetwork_project.production_settings
ENV DEBUG=False

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p logs media staticfiles

# Copiar scripts de inicialización
COPY init_database.py .
COPY start.sh .

RUN chmod +x init_database.py start.sh

# Crear un usuario no-root para ejecutar la aplicación
RUN adduser --disabled-password --gecos '' appuser || true
RUN chown -R appuser:appuser /app || true

EXPOSE 8000

# Healthcheck simple: verifica que el endpoint raíz responda 200
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 CMD python -c "import urllib.request,sys;\ntry:\n r=urllib.request.urlopen('http://127.0.0.1:8000/', timeout=2); sys.exit(0 if r.getcode()==200 else 1)\nexcept Exception:\n sys.exit(1)"

# Ejecutar como usuario no-root
USER appuser

CMD ["./start.sh"]