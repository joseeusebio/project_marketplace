FROM python:3.11.3-alpine3.18
LABEL maintainer="joseeusebioeng@gmail.com"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    build-base \
    linux-headers

COPY . /backend

WORKDIR /backend

RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r /backend/requirements.txt

RUN mkdir -p /backend/data/web/static && \
    mkdir -p /backend/data/web/media && \
    mkdir -p /backend/data/web/images && \
    chmod -R 775 /backend/data/web/static && \
    chmod -R 775 /backend/data/web/media && \
    chmod -R +x /backend/scripts

ENV PATH="/venv/bin:$PATH"

CMD python manage.py collectstatic --noinput && \
    python manage.py makemigrations --noinput && \
    python manage.py migrate --noinput && \
    gunicorn --bind 0.0.0.0:8000 --timeout 120 product_api.wsgi:application

