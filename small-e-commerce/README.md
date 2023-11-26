# Small e-commerce

Homework

## Run Locally with Docker

1. Clone the project

2. Setup env

    - Install poetry: https://python-poetry.org/docs/
    - Install packages on local `poetry install`


3. Build & Run db

    ```bash
      docker compose -f ./docker-compose.yml build && \
      docker compose -f ./docker-compose.yml up
    ```

4. Migrate database locally

    ```bash
    make alembic-upgrade
    ```

5. Run command to insert dummy data from local

    ```bash
    poetry run python small_ecommerce/manage.py dumpdummy
    ```

6. Go to api doc `localhost:8000/docs`

7. Shutdonw the db

    ```bash
      docker compose down
    ```