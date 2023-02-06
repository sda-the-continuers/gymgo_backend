FROM python:3.8

RUN apt-get update -y && apt-get install -y gettext cron

WORKDIR /app

RUN date
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt


COPY . .

ENV PYTHONUNBUFFERED 1