
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

COPY init_database.py .
COPY start.sh .

RUN chmod +x init_database.py start.sh

EXPOSE 8000

CMD ["./start.sh"]