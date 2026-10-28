# Mtaani Post

Django app for a neighbourhood: residents, posts, contacts, and businesses. I built it in 2021 while learning Django. It is the public sample for the Django and PostgreSQL line on my profile. The court-data pipelines are a different job and stay in the client repository.

A test creates a user, a neighbourhood, and one announcement, and checks that the post is stored on that neighbourhood. Signup also creates a profile and a welcome email.

## Run the test

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py test
```

The test uses SQLite. No `.env` file is required.

## PostgreSQL

Set these when you want the database the app was written for:

```
SECRET_KEY=change-me
DEBUG=True
MODE=dev
DB_NAME=mtaani
DB_USER=postgres
DB_PASSWORD=
DB_HOST=127.0.0.1
ALLOWED_HOSTS=localhost,127.0.0.1
```

Then install the Postgres driver and start the app:

```bash
pip install psycopg2-binary
python manage.py migrate
python manage.py runserver
```
