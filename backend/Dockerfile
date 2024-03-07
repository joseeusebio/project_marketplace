FROM python:3.11.3-alpine3.18
LABEL mantainer="joseeusebioeng@gmail.com"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /backend

WORKDIR /backend

EXPOSE 8000

RUN python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install -r /backend/requirements.txt && \
  adduser --disabled-password --no-create-home duser && \
  mkdir -p /backend/data/web/static && \
  mkdir -p /backend/data/web/media && \
  mkdir -p /backend/data/web/images && \
  chown -R duser:duser /backend/venv && \
  chown -R duser:duser /backend/data/web/static && \
  chown -R duser:duser /backend/data/web/media && \
  chmod -R 755 /backend/data/web/static && \
  chmod -R 755 /backend/data/web/media && \
  chmod -R +x /backend/scripts

ENV PATH="/backend/scripts:/venv/bin:$PATH"

USER duser

CMD ["commands.sh"]

