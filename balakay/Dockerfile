FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

RUN python3 manage.py collectstatic --noinput

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "balakay.wsgi:application"]

ENV DJANGO_ALLOWED_HOSTS="balakay-web-1021550053826.asia-south1.run.app,localhost,127.0.0.1,0.0.0.0"
