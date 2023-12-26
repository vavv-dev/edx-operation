FROM ubuntu:22.04 as app

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -qy install --no-install-recommends \
    language-pack-en locales \
    python3.11 python3.11-dev python3-pip libpq-dev gcc \
    # weasyprint requirements
    python3-cffi python3-brotli libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0

# set python3.11 default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

RUN pip install --upgrade pip setuptools
# delete apt package lists because we do not need them inflating our image
RUN rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV DJANGO_SETTINGS_MODULE edx_operation.settings.production

EXPOSE 34013
RUN useradd -m --shell /bin/false app


FROM app as prod

WORKDIR /edx/app/edx-operation

COPY . /edx/app/edx-operation/

RUN pip install -r requirements/production.txt

RUN python manage.py collectstatic --noinput

RUN mkdir -p /edx/var/log

USER app

# Gunicorn 19 does not log to stdout or stderr by default. Once we are past gunicorn 19, the logging to STDOUT need not be specified.
CMD gunicorn --workers=2 --name edx-operation -c /edx/app/edx-operation/edx_operation/docker_gunicorn_configuration.py --log-file - --max-requests=1000 edx_operation.wsgi:application


FROM prod as dev

USER root

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -qy install --no-install-recommends make

RUN pip install -r requirements/dev.txt

CMD bash -c 'while true; do python /edx/app/edx-operation/manage.py runserver 0.0.0.0:34003; sleep 2; done'
