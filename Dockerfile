# syntax=docker/dockerfile:1
FROM python:slim

WORKDIR /app

COPY app/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./app .

CMD [ "python3", "app.py" ]