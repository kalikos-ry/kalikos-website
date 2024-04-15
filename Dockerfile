FROM python:3.11-slim-buster

RUN apt-get update && apt-get install -y libpq-dev build-essential libjpeg-dev zlib1g

RUN pip install --upgrade pip
RUN pip install pip-tools

WORKDIR /app
COPY . /app

COPY requirements.* /app/

RUN pip-compile
RUN pip install -r requirements.txt
RUN pip install uwsgi==2.0.24

RUN python manage.py compilescss
RUN python manage.py collectstatic --noinput

CMD uwsgi --module kalikos.wsgi --http=0.0.0.0:80