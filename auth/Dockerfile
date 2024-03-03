FROM python:3.11.6

WORKDIR /code
COPY auth/poetry.lock /code/poetry.lock
COPY auth/pyproject.toml /code/pyproject.toml
ENV POETRY_VERSION=1.7.1
RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY ./auth /code

#CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
#CMD ["uvicorn", "app.main:app_auth", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
CMD ["uvicorn", "main:app_auth", "--host", "0.0.0.0", "--port", "8000"]
#CMD ls -la

