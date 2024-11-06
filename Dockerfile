FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED = 1 

WORKDIR /home/raj_ecommerce

COPY requirements.text requirements.text

RUN pip3 install -r requirements.text

COPY . .





