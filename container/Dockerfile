FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update \
  # mysql dependencies
  && apt-get install -y libmariadb-dev gcc default-mysql-client build-essential pkg-config vim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
