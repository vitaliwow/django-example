manage = poetry run python src/manage.py

.PHONY: format
format:
	poetry run black .
	poetry run ruff check . --fix --exit-zero
	poetry run pre-commit run --all

.PHONY: linting
lint:
	poetry run ruff . --fix

check-manage:
	poetry run dotenv-linter src/core/.env.ci
	$(manage) makemigrations --dry-run --no-input --check
	$(manage) check

test:
	poetry run coverage run -m pytest -x -n 4
	poetry run coverage report
	poetry run coverage xml

report:
	poetry run coverage run -m pytest -x -n 4 --cov --cov-report html:cov_html

test-no-migration:
	mkdir -p src/static
	$(manage) compilemessages
	poetry run pytest --no-migrations

migrate:
	$(manage) migrate

run:
	$(manage) runserver localhost:8001

gitadd: format lint test
	git add .

check:
	$(manage) check
