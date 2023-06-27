# User Management Service Database

This repository contains the Dockerfile and initialization SQL script to set up a PostgreSQL database for the User Management Service.

## Prerequisites

- Docker

## Getting Started

1. Clone this repository to your local machine.

2. Build the Docker image by running the following command in the root directory:

   ```shell
   docker build -t user-management-db .
   ```
3. Start the Docker container by running the following command:

   ```shell
   docker run -d --name user-management-db -p 5432:5432 user-management-db
   ```
   This command will start the PostgreSQL database container and map the host port `5432` to the container port `5432`.

4. Wait for the container to start up. You can check the container logs to see if the database initialization is successful:
    ```shell
    docker logs user-management-db
    ```
    If the initialization is successful, you should see log messages indicating the creation of the users and tokens tables.

5. Once the container is running and the database is initialized, you can connect to the database using your preferred PostgreSQL client tool (e.g., psql or a GUI tool).


