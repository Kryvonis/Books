FROM ubuntu:latest
FROM python:3.4
RUN apt-get update -y

RUN apt-get install -y python3-pip python-dev build-essential

COPY . /app

ADD requirements.txt /app
RUN pip install -r app/requirements.txt

