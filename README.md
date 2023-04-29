# URL Shortener
Simple URL shortening service based on Django and Django REST Framework.

It allows to create a short URL that redirects to a specified (possibly long) target URL.

It is possible to use the service both anonymously or as a logged user:
* anonymously: the shortened URL will be valid for 24 hours. After that, the link won't work anymore.
* as a logged user: more features are available, such as:
  * customization of the expiration date (or no expiration date),
  * list of active shortened URLs created with related statistics,
  * e-mail notification when a shortened URL expires.

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

The API is available under `http://localhost:8000/api/v1/`.
See the full API documentation at `http://localhost:8000/api/v1/doc/`.

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
