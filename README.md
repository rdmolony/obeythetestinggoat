# obeythetestinggoat on `Docker` & `pytest`

I'm adapting [obeythetestinggoat](https://www.obeythetestinggoat.com) for `Docker` and `pytest`

## Install

Clone this repository, install [docker](https://docs.docker.com/get-docker/) and run ...

```bash
docker-compose build
```

... to download and install all of the required libraries (`Python`, `Django`, `Selenium` etc.)

Run the `Django` server via ...

```bash
docker-compose run --rm --name goat-web web python manage.py runserver 0.0.0.0:8000
```

... launch a shell in the same container as the running server so you can execute tests against it ...

```bash
docker exec -it goat-web bash
```

... and finally run your various tests via ...

```bash
pytest
```