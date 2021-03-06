<h1 align="center">Used Good Reads</h1>

<p align="center"><a href="https://travis-ci.org/usedgoodreads/usedgoodreads"><img src="https://travis-ci.org/usedgoodreads/usedgoodreads.svg?branch=master" /></a></p>

<p align=center>
  <img src="assets/usedgoodreads.png" />
</p>

Finding second hand versions for your books at [Goodreads](https://www.goodreads.com).


## Overview

Goodreads is amazing for exploring new books.
At the same time we want to promote second hand books, used books, and local book stores.
This project's goal is to allow searching for `goodreads.com` books by adding `used` at the front of the link as in `usedgoodreads.com`.

## Quickstart

With [Docker](https://docs.docker.com/engine/) and [Docker Compose](https://docs.docker.com/compose/) start the infrastructure

    docker-compose up

Then in your browser

    https://www.goodreads.com/book/show/36236132-growing-a-revolution

    http://localhost:5000/book/show/36236132-growing-a-revolution


## Development

We require [Docker](https://docs.docker.com/engine/) and [Docker Compose](https://docs.docker.com/compose/) for development in reproducible and self-contained environments.

Workflow
1. Configure the environment using `*.env` files in the `env` directory; see the `env/*.env.example` files
2. Get a shell in the container you are developing for, e.g. the app
3. Use your host editor to make changes to app source code
4. Run tests, linters, the app, etc. in the app container shell

This makes sure our development is self-contained and reproducible.
At the same time it makes away with having to build new images for source code changes.
See [infrastructure](#infrastructure) below for details on e.g. how to get a shell in a container.


## Infrastrcture

Build all docker images

    docker-compose build

Startup infrastructure in daemon mode

    docker-compose up -d

Scale out async worker with the remaining infrastructure being up already

    docker-compose up -d --no-deps --scale worker=10 worker

Check logs for running infrastructure

    docker-compose logs

Shutdown infrastructure

    docker-compose down

Get a shell in a app container for development, dependencies are up, and ports exposed on the host

    docker-compose run --entrypoint bash --service-ports app

The idea is to build the images once.
We then mount the app directory into the corresponding running container.
This allows us to modify the sources on the host and immediately see the changes in the self-contained and reproducible build environment.


## Deployment

On the remote host install
- [Docker](https://docs.docker.com/engine/) and make sure to follow the post-installation steps
- [Docker Compose](https://docs.docker.com/compose/)

On the remote host, increase the number of ssh sessions in `/etc/ssh/sshd_config`

    MaxSessions 256

Then either use a container registry or push your image directly to the remote host

    docker image tag usedgoodreads/app usedgoodreads/app:staging
    docker image save usedgoodreads/app:staging | ssh user@host "docker image load"

Then spawn up the infrastructure on the remote host with staging overrides and a staging project name

    DOCKER_HOST="ssh://user@host" docker-compose \
      -p staging \
      -f docker-compose.yaml \
      -f docker-compose.staging.yaml \
      up --detach

Note: we are using Travis CI/CD to automatically deploy; see the [`.travis.yml`](./.travis.yml).


## Architecture

We run a Flask based API which takes the Goodreads-like book route

    /book/show/36236132-growing-a-revolution

and uses the key `36236132-growing-a-revolution` as a key for two lookups
- Lookup against a Postgres database to see if we have the book's title and isbn. If not, we enqueue an async job (with rq, through Redis) to resolve the book's title and isbn for the key.
- Lookup against a Postgres database to see if we have up to date used book result. If not, we enqueue an async job (with rq, through Redis) to resolve used books for a book's title and isbn for the key.

These jobs run asynchronously and write their results into a Postgres database.
Once we have up to date used book results, the Flaks API renders a Jinja2 template and returns the generated HTML to the user.

```
+-api-------------------------------------------------------------------+
|                                                                       |
| https://www.usedgoodreads.com/book/show/36236132-growing-a-revolution |
|                                                                       |
+----------------------------+------------------------------------------+
                             |
                             |
                             |
+-key------------------------v---+                                 +-postgres---------------------+
|                                +--------------------------------->                              |
|  36236132-growing-a-revolution |                                 | Up to date used book results |
|                                <---------------------------------+                              |
+------------------------+---+---+                                 +-------------------------^----+
+-isbn------------+      |   |                                     +-fetch-----+             |
|                 <------+   +------------------------------------->           |             |
|  9780393608328  |                                                | Goodreads |             |
|                 <------------------------------------------------+           |             |
+-------------+---+                                                +-----------+             |
+-rq-------+  |                                                                              |
|          |  |                                                                              |
|  Worker  <--+                                                                              |
|          |                                                                                 |
+-------+--+                                                                                 |
        |                                                                                    |
        |                                                                                    |
        +------------------------------------------------------------------------------------+
```


## License

Copyright © 2020 usedgoodreads

Distributed under the MIT License (MIT).
