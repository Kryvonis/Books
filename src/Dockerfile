FROM python:3.4

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

COPY . /app

ADD requirements.txt /app
RUN pip install -r app/requirements.txt


