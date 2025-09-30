# Dockerfile multi-stage para optimización
FROM node:20-alpine AS node-builder

# Instalar dependencias Node.js y compilar CSS
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY static/ ./static/
COPY tailwind.config.js ./
RUN npm run build

# Stage principal con Python
FROM python:3.11-slim

# Variables de entorno para producción
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DJANGO_SETTINGS_MODULE=socialnetwork_project.settings
ENV DEBUG=False

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root
RUN adduser --disabled-password --gecos '' appuser

# Crear directorio de trabajo
WORKDIR /app

# Copiar e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Copiar CSS compilado desde el stage anterior
COPY --from=node-builder /app/static/css/output.css ./static/css/

# Crear directorios necesarios
RUN mkdir -p logs media staticfiles && \
    chown -R appuser:appuser /app

# Copiar script de inicio
COPY start.sh .
RUN chmod +x start.sh

# Cambiar a usuario no-root
USER appuser

# Recopilar archivos estáticos
RUN python manage.py collectstatic --noinput

# Exponer puerto
EXPOSE 8000

# Comando de inicio usando el script
CMD ["./start.sh"]