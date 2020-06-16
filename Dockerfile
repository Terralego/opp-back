ARG BASE=corpusops/ubuntu-bare:bionic
FROM $BASE
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ARG BUILD_DEV=y
ARG PY_VER=3.6
# See https://github.com/nodejs/docker-node/issues/380
ARG GPG_KEYS=B42F6819007F00F88E364FD4036A9C25BF357DD4
ARG GPG_KEYS_SERVERS="hkp://p80.pool.sks-keyservers.net:80 hkp://ipv4.pool.sks-keyservers.net hkp://pgp.mit.edu:80"

WORKDIR /code
ADD apt.txt /code/apt.txt

# setup project timezone, dependencies, user & workdir, gosu
RUN bash -c 'set -ex \
    && apt-get update -qq \
    && apt-get install -qq -y $(grep -vE "^\s*#" /code/apt.txt  | tr "\n" " ") \
    && apt-get clean all && apt-get autoclean \
    && apt-get clean all && rm -rf /var/apt/lists/* && rm -rf /var/cache/apt/* \
    && : "project user & workdir" \
    && useradd -ms /bin/bash django --uid 1000'

ADD crontab /etc/cron.d/django
CMD chmod 0644 /etc/cron.d/django

ADD prod/start.sh \
    prod/cron.sh \
    prod/init.sh \
    /code/init/

ADD requirements*.txt tox.ini README.md /code/
ADD src /code/src/
ADD lib /code/lib/
ADD private /code/private/

RUN bash -c 'set -ex \
    && chown django:django -R /code \
    && cd /code \
    && gosu django:django bash -exc "python${PY_VER} -m venv venv \
    && venv/bin/pip install -U --no-cache-dir setuptools wheel \
    && venv/bin/pip install -U --no-cache-dir -r ./requirements.txt \
    && if [[ -n \"$BUILD_DEV\" ]];then \
      venv/bin/pip install -U --no-cache-dir \
      -r ./requirements.txt \
      -r ./requirements-dev.txt;\
    fi \
    && mkdir -p public/static public/media"'

# image will drop privileges itself using gosu
WORKDIR /code/src
CMD "/code/init/init.sh"
