FROM python:3.11.7-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install --upgrade pip
RUN apk add --no-cache bash
RUN apk add gcc musl-dev libffi-dev
RUN pip install poetry


# Requirements are installed here to ensure they will be cached.
COPY ./poetry.lock /poetry.lock
COPY ./pyproject.toml /pyproject.toml

RUN poetry config virtualenvs.create false && poetry install

COPY ./compose/local/app/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/app/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

WORKDIR /app

ENTRYPOINT ["/entrypoint"]