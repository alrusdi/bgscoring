FROM python:3.11.7-alpine

EXPOSE 8000

WORKDIR bgscoregames

RUN pip install --upgrade pip
RUN apk add gcc musl-dev libffi-dev
RUN pip install poetry

COPY . /bgscoregames

RUN poetry config virtualenvs.create false && poetry install