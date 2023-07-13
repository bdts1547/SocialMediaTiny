FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /media_social_app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
