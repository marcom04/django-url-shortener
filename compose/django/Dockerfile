FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_ROOT=/home/django/app

EXPOSE 8000

# basic configuration
RUN apt-get update && \
    # dependencies for building Python packages
    apt-get install -y build-essential && \
    # psycopg2 dependencies
    apt-get install -y libpq-dev postgresql-client-13 && \
    # Translations dependencies
    apt-get install -y gettext && \
    # cleaning up unused files
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
    rm -rf /var/lib/apt/lists/* && \
    # create directories and users
    mkdir -p $APP_ROOT && \
    groupadd -r django &&  \
    useradd -r -s /sbin/nologin django -g django && \
    # create virtualenv
    python -m venv /py && \
    /py/bin/pip install --upgrade pip

# install Pip dependencies
COPY ./requirements.txt /tmp/requirements.txt
RUN /py/bin/pip install wheel && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

# copy and configure scripts
COPY --chown=django:django ./compose/django/entrypoint.sh /home/django/scripts/entrypoint.sh
RUN sed -i 's/\r$//g' /home/django/scripts/entrypoint.sh && \
    chmod -R +x /home/django/scripts

# copy project code
COPY --chown=django:django ./urlcut/ $APP_ROOT

ENV PATH="/py/bin:$PATH"

USER django

WORKDIR $APP_ROOT

ENTRYPOINT [ "/home/django/scripts/entrypoint.sh" ]
