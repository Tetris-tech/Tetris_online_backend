# TETRIS_ONLINE_BACKEND

## Prerequisites

Before starting, ensure you have the following installed on your system:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Deployment Steps

1. **Clone the Repository**

   Clone the repository to your local machine:

   ```bash
   git clone https://github.com/Tetris-tech/Tetris_online_backend.git
   cd Tetris_online_backend
   ```

2. **Set Up Environment Variables**

   Ensure the required environment variables are configured. Create a `.env` file in the `config` directory if it doesn't already exist. The `postgres` service uses this file for configuration.

3. **Build and Start the Application**

   Run the following command to build and start the application:

   ```bash
   docker compose up --build
   ```

   This command will:
   - Start the backend services, including the API server, Celery workers, PostgreSQL, Redis, MinIO, and more.
   - Expose the API on port `8000`.

4. **Accessing the Services**

   - **API**: The API is available at [http://localhost:8000](http://localhost:8000).
   - **Redis**: Accessible on port `6379`.
   - **PostgreSQL**: Accessible on port `5432`.
   - **MinIO Console**: Accessible at [http://localhost:9000](http://localhost:9000) (default user: `root`, password: `rootroot`).
   - **Mailpit**: Accessible at [http://localhost:8025](http://localhost:8025) for viewing emails.

5. **Stop the Application**

   To stop the application and remove containers, networks, and volumes, run:

   ```bash
   docker compose down
   ```

## Application Architecture

The `docker-compose.yml` file defines the following services:

- **`base_app`**: Base configuration for the application services.
- **`migration`**: Handles database migrations.
- **`app`**: Base application service dependencies.
- **`api`**: The main API service exposing port `8000`.
- **`celery_worker`**: Celery worker for background tasks.
- **`celery_beat`**: Celery beat for periodic tasks.
- **`postgres`**: PostgreSQL database.
- **`redis`**: Redis server for caching and task queuing.
- **`mailpit`**: Mail testing service.
- **`nginx`**: Nginx for reverse proxy.
- **`minio`**: Object storage similar to AWS S3.
- **`minio-create-bucket`**: Service to create a default bucket in MinIO.

## Notes

- Ensure that the `src` directory exists in the repository root, as it is mounted in the container.
- Modify the `docker-compose.yml` file if you need to change any default configurations.
