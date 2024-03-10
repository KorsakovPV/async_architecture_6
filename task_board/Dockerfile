FROM python:3.11.6

WORKDIR /code
COPY task_board/poetry.lock /code/poetry.lock
COPY task_board/pyproject.toml /code/pyproject.toml
ENV POETRY_VERSION=1.7.1
RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY ./task_board /code

#CMD ["uvicorn", "main:app_task_board", "--host", "0.0.0.0", "--port", "8001"]

