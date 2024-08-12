FROM python:3.12.1

LABEL authors="e1_m"

WORKDIR /app

COPY poetry.lock ./
COPY pyproject.toml ./

RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install

COPY . .

EXPOSE 8000
