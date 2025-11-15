FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    gettext \
    vim \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ВАЖНО: запускаем manage.py из директории web
# и указываем gunicorn правильный chdir
CMD ["sh", "-c", "python web/manage.py migrate && gunicorn web.wsgi:application --chdir /app/web --bind 0.0.0.0:8000"]
