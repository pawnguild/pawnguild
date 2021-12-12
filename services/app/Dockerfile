FROM python:3.9

ENV PYTHONUNBUFFERED=1

RUN apt-get -y update
RUN apt-get -y install libxml2-dev libxmlsec1-dev

WORKDIR /app

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .