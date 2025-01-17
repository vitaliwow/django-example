## Project structure

The main django app is called `core`. It contains `.env` file for django-environ. For examples see `src/core/.env.ci`. Here are some usefully app-wide tools:
* `core.admin` — app-wide django-admin customizations (empty yet), check out usage [examples](https://github.com/f213/django/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/src/app/admin)
* `core.test.api_client` (available as `api` and `anon` fixtures within pytest) — a [convinient DRF test client](https://github.com/f213/django/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/src/users/tests/tests_whoami.py#L6-L16).

Django's user model is located in the separate `users` app.

Also, feel free to add as much django apps as you want.

## Installing on a local machine
<details>
 <summary>
Running a project with docker (preferred method)
 </summary>
<br />

1. Install docker and docker compose  suitable for your operating system. [official docker website](https://docs.docker.com/engine/install/)
```bash
docker compose version

~ Docker Compose version v2.2.3
```
2. Clone a project in /your_dir/

3. Create a .env file and add variables as per "/your_dir/main/infra/.env.example"
```bash
cd /your_dir/main/  # go to main dir
touch .env  # create .env file
nano .env   # open the .env file and add variables as in .env.example
```
4. Start project.
```bash
docker compose up --build -d
```
</details>

<details>
 <summary>
Run the project by installing all packages
 </summary>
<br />
This project requires python 3.11. Deps are managed by [Poetry](https://python-poetry.org/docs/).

Install requirements:

**Install Poetry**
If you haven't already, you need to install Poetry, a tool for managing Python dependencies. You can find the installation guide at [python-poetry.org](https://python-poetry.org/docs/).

**Install Ruff**
If you haven't already, you need to install Ruff, a tool for linting code. You can find the installation guide at [docs.astral.sh/ruff](https://docs.astral.sh/ruff/).


Run the server:

```bash
$ cd src && cp core/.ci.env core/.env  # default environment variables
$ ./manage.py migrate
$ ./manage.py createsuperuser
$ ./manage.py runserver
```

Testing(run it before pushing your code):
```bash
# run lint
$ make lint

# fix lint issues
$ make fmt

# run unit tests
$ make test
```

Development servers:

```bash
# run django dev server
$ ./manage.py runserver

```
</details>

## Backend Code requirements

### Style

* Obey [django's style guide](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/#model-style).
* Configure your IDE to use [Ruff](https://docs.astral.sh/ruff/) for checking your python code. To run our linters manualy, do `make lint`
* Prefer English over your native language in comments and commit messages.
* Commit messages should contain the unique id of issue they are linked to (refs #100500)
* Every model, service and model method should have a docstring.

### Code organisation

* KISS and DRY.
* Obey [django best practices](http://django-best-practices.readthedocs.io/en/latest/index.html).
* **No logic is allowed within the views or serializers**. Only services and models. When a model grows beyond 500 lines of code — go create some services.
* Use PEP-484 [type hints](https://www.python.org/dev/peps/pep-0484/) when possible.
* Prefer composition to inheritance.
* Never use [signals](https://docs.djangoproject.com/en/dev/topics/signals/) or [GenericRelations](https://docs.djangoproject.com/en/dev/ref/contrib/contenttypes/) in your own code.
* No l10n is allowed in python code, use [django translation](https://docs.djangoproject.com/en/dev/topics/i18n/translation/).
