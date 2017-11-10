FROM ubuntu:16.04
MAINTAINER Alexander Pushin "work@apushin.com"

RUN apt-get update && apt-get install -y \
    uwsgi

COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

ENV SECRET_KEY='secret_key'

COPY app /app
COPY run.py /run.py

RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi
COPY uwsgi.ini uwsgi.ini
EXPOSE 8000

USER uwsgi

ENTRYPOINT uwsgi --ini uwsgi.ini
