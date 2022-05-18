FROM python:3.10.2-alpine
WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev \
    && pip install --no-cache-dir psycopg2-binary \
    && apk del --no-cache .build-deps
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
