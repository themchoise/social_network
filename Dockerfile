# Multi-stage Docker build para Red Social IFTS
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
ENV DJANGO_SETTINGS_MODULE=socialnetwork_project.production_settings
ENV DEBUG=False

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

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
RUN mkdir -p logs media staticfiles

# Copiar scripts de inicialización
COPY init_database.py .
COPY start.sh .

# Hacer ejecutables los scripts
RUN chmod +x init_database.py start.sh

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["./start.sh"]