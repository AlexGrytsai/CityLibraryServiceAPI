FROM python:3.12.0
LABEL authors="agrytsai"

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN adduser \
    --disabled-password \
    --no-create-home \
    myuser

RUN chown -R myuser:myuser /app

RUN chmod -R 777 /app

USER myuser
