FROM python:3.12-slim

LABEL authors="Dhruv Dole, Nathan Rethwisch, Thanh Mai, Colin Russell"

WORKDIR /app

COPY requirements-dash.txt /requirements.txt

RUN pip install -r /requirements.txt && rm /requirements.txt

COPY ./src /app

ENV ASSETS_ROOT=/app/assets
ENV ENVIRONMENT=prod
ENV PORT=10000
EXPOSE ${PORT}

CMD gunicorn -w ${GUNICORN_WORKERS:-4} -b 0.0.0.0:${PORT} --access-logfile - --error-logfile - main:server
