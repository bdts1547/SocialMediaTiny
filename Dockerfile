FROM python:3.9-slim-buster
ENV PYTHONBUFFERED=1
WORKDIR /test_app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt