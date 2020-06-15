<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://i.imgur.com/6wj0hh6.jpg" alt="Project logo"></a>
</p>

<h3 align="center">Opp-back</h3>

<div align="center">

  [![Status](https://img.shields.io/badge/status-active-success.svg)]()
  [![GitHub Issues](https://img.shields.io/github/issues/terralego/opp-back.svg)](https://github.com/terralego/opp-back/issues)
  [![GitHub Pull Requests](https://img.shields.io/github/issues-pr/terralego/opp-back.svg)](https://github.com/terralego/opp-back//pulls)
  [![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> Opp-back is the backend of the Opp project. Opp stands for "Photographic Landscapes Observatory" in French (Observatoire Photographique des Paysages).
    <br>
</p>

# 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Usage](#usage)
- [Built Using](#built_using)
- [TODO](../TODO.md)
- [Contributing](../CONTRIBUTING.md)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

# 🧐 About <a name = "about"></a>

Opp-back is the backend part of the Opp applications.

# 🏁 Getting Started <a name = "getting_started"></a>

This section take you by the hand through a series of steps to install a
working version of the backend part of the Opp applications.
Start here if you want a working version of the platform.

There is two parts for the application, the backend and the frontend. Each part
has his own instructions. To see the frontend part go to
[the frontend](https://github.com/terralego/terra-front) repository.

## Prerequisites

In order to install the backend server application, you need to fulfil
the following requirements:

* A linux server with a recent kernel
* [docker](https://docs.docker.com/install/) >= 18.6 installed
* [docker-compose](https://docs.docker.com/compose/install/) >= 1.23.0 installed
* Any load balancer (HaProxy, Traefik, ...) to redirect queries to backend
  (and frontend)
* A hostname pointing to the backend server
* Optional (recommended): a set of extra subdomains also pointing to the backend
  server to serve tiles from the same server but bypass the browser limit.
  Drastically improve performances
* Optional: you can use an instance of [sentry](https://sentry.io/welcome/)
  to track server errors

## Installation

These instructions will guide you to install the application on a development server.
For production purpose, you should understand what you are doing, and use
`docker-compose-prod.yml` file.

Opp-back offers an API that is consumed by the frontend.

To install it we need to achieve the following steps:

- Get the latest version
- Configure the application
- Bootstrap the instance
- Populate initial database


### Get the latest version

You can clone the source code by executing:

    git clone https://github.com/terralego/opp-back.git

/!\ The following commands must be executed in the root directory of the backend
application.

### Configure

To configure the application before the first startup, you need to adapt two
files to your needs.

First the `docker.env` file:

```sh
$ cp docker.env.dist docker.env
```

Use your preferred editor to edit the created file and modify the values.
Read the comments in the file to get hints on the purpose of each variable.

You can now copy the settings file:

```sh
$ cp src/project/settings/local.py.dist src/project/settings/local.py
```

Also edit this file to make the values meet your needs. Again, comments
can help you to find the appropriate values.

**Hint**: You may have to add `0.0.0.0` to `ALLOWED_HOSTS` in `local.py`.
Also, setting your mapbox token and background style is recommended.

Finally, copy `.env.dist` file to `.env`. The file is used when deploying a production environment to set the django built image's name and tag:
```sh
$ cp .env.dist .env
```

### Bootstrap the instance

After a last verification of the files, to run with docker, just type:

#### For development purpose

```sh
# First time you download the app, or sometime to refresh the image
docker-compose -f docker-compose.yml -f docker-compose-dev.yml pull # Call the docker compose pull command
docker-compose -f docker-compose.yml -f docker-compose-dev.yml build # Should be launched once each time you want to start the stack
docker-compose -f docker-compose.yml -f docker-compose-dev.yml up django # Should be launched once each time you want to start the stack
```

#### For production purpose

```sh
# First time you download the app, or sometime to refresh the image
docker-compose -f docker-compose.yml -f docker-compose-prod.yml pull # Call the docker compose pull command
docker-compose -f docker-compose.yml -f docker-compose-prod.yml build # Should be launched once each time you want to start the stack
docker-compose -f docker-compose.yml -f docker-compose-prod.yml up django # Should be launched once each time you want to start the stack
# Migrations will automatically be run with production settings. Once the initial migrations are done, you can launch all containers
docker-compose -f docker-compose.yml -f docker-compose-prod.yml up
```

**notes:** The first startup can be long (5 ~ 10 minutes) as all docker images will be
downloaded and/or built.

### Populate the database

First of all, run all the migrations :

```sh
$ docker-compose exec django /code/venv/bin/python3 /code/src/manage.py migrate
```

To be able to connect you need to create a super user. Execute:

```sh
$ docker-compose exec django /code/venv/bin/python3 /code/src/manage.py createsuperuser
```

Your instance is now up and running.

To test it you can execute:

```sh
curl http://localhost:<port>/api/settings/
```

You should get a json in response.

After that you can stop the server by doing a `Ctrl-c` inside the first shell.

You should now configure your load balancer to serve requests to the backend
and proceed to the frontend installation.

**Notes:**: if you want to serve backend and frontend from the same domain, you must
serve backend from the following prefixes:
`api/, admin/, cms/, media/, static_dj/, 502.html, mailcatcher/`
and the frontend for everything else.

# Troubleshooting

## In general

If you get troubles with the nginx docker env restarting all the time, try recreating it:

```bash
docker-compose -f docker-compose.yml -f docker-compose-dev.yml up -d --no-deps --force-recreate nginx backup
```

If you get the same problem with the django docker env:

```bash
docker-compose -f docker-compose.yml -f docker-compose-dev.yml stop django db
docker volume rm visu-postgresql # check with docker volume ls
docker-compose -f docker-compose.yml -f docker-compose-dev.yml up -d db
# wait fot postgis to be installed
docker-compose -f docker-compose.yml -f docker-compose-dev.yml up django
```

# 🎈 Usage <a name="usage"></a>

## Start a shell inside the django container

- for user shell

```sh
docker-compose exec django bash
```

## Calling Django manage commands

```sh
docker-compose  exec django /code/venv/bin/python3 /code/src/manage.py shell [options]
# For instance:
# docker-compose exec django /code/venv/bin/python3 /code/src/manage.py shell migrate
# docker-compose exec django /code/venv/bin/python3 /code/src/manage.py shell shell
# docker-compose exec django /code/venv/bin/python3 /code/src/manage.py shell createsuperuser
# ...
```

## Docker volumes

Your application extensively uses docker volumes. From times to times you may
need to erase them (eg: burn the db to start from scratch)

```sh
docker volume ls  # hint: |grep \$app
docker volume rm $id
```

# ⛏️ Built Using <a name = "built_using"></a>
- [Postgres](https://www.postgresql.org/) - Database
- [Django](https://www.djangoproject.com/) - Python Framework
- [DjangoRestFramework](https://www.django-rest-framework.org) - Rest Framework
- [Redis](https://nodejs.org/en/) - Broker

# ✍️ Authors <a name = "authors"></a>
- [@terralego](https://github.com/terralego) - Idea & Initial work
