FROM python:3.12-slim
LABEL authors="Dhruv Dole"
LABEL authors="Nathan Rethwisch"
LABEL authors="Thanh Mai"
LABEL authors="Colin Russell"

WORKDIR /app

COPY requirements-dash.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY ./src /app

ENV ASSETS_ROOT=/app/assets
ENV ENVIRONMENT=prod

EXPOSE 8080

CMD gunicorn -w ${GUNICORN_WORKERS:-4} -b 0.0.0.0:8080 --access-logfile - --error-logfile - main:server
