FROM python:3.11-slim


ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV NODE_MAJOR=20


RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    pkg-config \
    && curl -fsSL https://deb.nodesource.com/setup_${NODE_MAJOR}.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app


COPY requirements.txt package.json package-lock.json ./


RUN pip install --no-cache-dir -r requirements.txt


RUN npm ci --only=production

COPY . .


RUN mkdir -p static/css logs media staticfiles


RUN npm run build


RUN python manage.py collectstatic --noinput


RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser


EXPOSE 8000

# Comando de inicio
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]