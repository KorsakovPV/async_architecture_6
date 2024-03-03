install:
	pip install poetry==1.7.1
	poetry install --with dev

format:
	black .

test:
	pytest -s -vv -m 'not e2e and not alembic'
