FROM python:3.12.1

LABEL authors="e1_m"

WORKDIR /app

COPY poetry.lock ./
COPY pyproject.toml ./

RUN pip install poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]