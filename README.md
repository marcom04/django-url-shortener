# URL Shortener
Simple URL shortening service based on Django and Django REST Framework.

It provides a REST API which allows to create a short URL that redirects to a specified (possibly longer) target URL.

It is possible to use the service both anonymously or as a logged user:
* anonymously: the shortened URL will be valid for 24 hours. After that, the link won't work anymore.
* as a logged user: more features are available, such as:
  * customization of the expiration date (or no expiration date),
  * list of active shortened URLs created with related statistics (number of visits),
  * e-mail notification when a shortened URL expires.

A Celery task, periodically scheduled, looks for expired mappings between short and long URLs and deletes them. 

It includes also a ***very*** basic ReactJS frontend, that can be used only to request a 
shortened URL anonymously.

## Development setup

### Prerequisites

* Docker Engine
* Docker Compose V2

### Build and run

```
docker compose up --build
```

### Run Django tests

```
docker exec -it urlcut-backend python manage.py test
```

### Usage

* The API is available under `http://localhost:8000/api/v1/`
  * See the full API documentation at `http://localhost:8000/api/v1/doc/`
* The Django administration site is available at `http://localhost:8000/admin`
  * A sample admin user is always available with credentials `admin@example.com` / `testpass123`
* The ReactJS frontend is available at `http://localhost:3000`

### Users fixtures

For test purposes, it is possible to load a couple of sample users from a fixture:
```
docker exec -it urlcut-backend python manage.py loaddata apps/users/fixtures/users.json
```

The sample users will have e-mails `user1@example.com`, `user2@example.com`, and password `testpass123`.


## Tech stack

* Django
* Django REST Framework
* Celery
* PostgreSQL
* RabbitMQ
* ReactJS

## Docker containerization

The URL shortener is composed by the following Docker containers:

* `backend`: runs the Django application providing the APIs
* `db`: a PostgreSQL database
* `rabbitmq`: a RabbitMQ broker used by Celery
* `worker`: runs a Celery worker instance for async tasks execution
* `scheduler`: runs a Celery beat instance for tasks scheduling
* `frontend`: proof-of-concept ReactJS frontend

## Folders structure

The `django` folder contains the Django backend and has the following sub-folders:

```
django
├── compose
│   └── [Dockerfile and other files needed for the containerization]
├── urlcut
│   ├── api
│   │   └── [serializers, views, and tests regarding the REST API]
│   ├── apps
│   │   └── [Django applications, keeping models, migrations, tasks, web views, tests]
│   ├── templates
│   │   └── [Django templates (e-mail templates)]
│   ├── urlcut
│   │   └── [Django project folder (settings, main URLs, celery config)]
│   └── manage.py
└── requirements.txt
```

The `react` folder contains the ReactJS frontend.
