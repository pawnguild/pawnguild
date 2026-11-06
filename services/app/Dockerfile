FROM python:3.11-bookworm@sha256:726d304906fa5eb468e5531e366548d1903286352f5adb54ef508ac01fbd80c6

ENV PYTHONUNBUFFERED=1

RUN apt-get -y update
RUN apt-get -y install libxml2-dev libxmlsec1-dev

WORKDIR /app

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --only-binary=Pillow -r requirements.txt

COPY . .
