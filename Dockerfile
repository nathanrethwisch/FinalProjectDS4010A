FROM python:3.12-slim
LABEL authors="dhruv"

WORKDIR /app

COPY ./src /app/src

COPY requirements-dash.txt /requirements.txt

RUN pip install -r /requirements.txt

CMD ["python3", "src/main.py"]
