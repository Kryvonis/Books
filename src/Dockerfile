FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

COPY . /app
WORKDIR /app
ADD requirements.txt /app
RUN pip install -r requirements.txt
CMD ["test_books.py"]
