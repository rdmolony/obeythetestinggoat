# obeythetestinggoat on `Docker` & `pytest`

I'm adapting [obeythetestinggoat](https://www.obeythetestinggoat.com) for `Docker` and `pytest`

## Install

1. Clone this repository
2. Install [docker](https://docs.docker.com/get-docker/)
3. Run ...

    ```bash
    docker-compose run web bash
    ```

    ... to:

    - Download and install all of the required libraries (`Python`, `Django`, `Selenium` etc.) into a container
    - Launch & hook into a bash shell within it

    & run the test suite via ...

    ```bash
    pytest
    ```