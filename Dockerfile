FROM python:3.7

WORKDIR /app
RUN mkdir repos

RUN apt-get -yq update

RUN pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt