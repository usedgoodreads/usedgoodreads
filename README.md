<h1 align='center'>Used Good Reads</h1>

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


## License

Copyright © 2020 usedgoodreads

Distributed under the MIT License (MIT).
