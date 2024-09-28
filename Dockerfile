FROM python:3.11-slim

WORKDIR /reports

RUN apt update && apt -y install libpq-dev gcc

COPY ./requirements.txt /reports

RUN pip3 install -r requirements.txt

COPY ./alembic.ini /reports
COPY ./migrations /reports/migrations
