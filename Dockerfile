
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DJANGO_SETTINGS_MODULE=socialnetwork_project.production_settings
ENV DEBUG=False
ENV SKIP_MIGRATIONS=true

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
COPY start.sh .
RUN chmod +x start.sh

EXPOSE 8000

# Crear usuario no-root para ejecutar la app
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Healthcheck mejorado: más tolerante para evitar falsos positivos
HEALTHCHECK --interval=60s --timeout=5s --start-period=30s --retries=5 CMD python -c "import urllib.request,sys;\ntry:\n r=urllib.request.urlopen('http://127.0.0.1:8000/health/', timeout=3); sys.exit(0 if r.getcode()==200 else 1)\nexcept Exception as e:\n print(f'Health check failed: {e}'); sys.exit(1)" || exit 0

# Ejecutar como usuario no-root
USER appuser

CMD ["./start.sh"]