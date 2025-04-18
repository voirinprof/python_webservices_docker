# Python Web Services with Docker

This repository demonstrates how to containerize Python web services using Docker. It includes examples of both Flask and FastAPI applications, showcasing how to build and run them in isolated environments.

## Project Structure

The repository is organized as follows:

- `flask/` – Contains a simple Flask application.
- `fastapi/` – Contains a FastAPI application.
- `nginx/` – Configuration files for Nginx to serve as a reverse proxy.
- `docker-compose.yml` – Defines and manages multi-container Docker applications.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

1. **Clone the repository:**

   ```bash
   git clone https://github.com/voirinprof/python_webservices_docker.git
   cd python_webservices_docker
   ```


2. **Build and run the containers:**

   ```bash
   docker-compose up --build
   ```


3. **Access the applications:**

   - Flask app: [http://localhost:5000](http://localhost:5000)
   - FastAPI app: [http://localhost:8000](http://localhost:8000)
   - Nginx (api test page): [http://localhost](http://localhost)

## Usage

This setup allows you to:

- Develop and test Flask and FastAPI applications in isolated Docker containers.
- Use Nginx as a reverse proxy to manage incoming requests.

## Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).