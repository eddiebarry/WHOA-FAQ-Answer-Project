### Docker setup
docker build -t server_host .

## Go to nginx
docker build -t reverse_proxy .

## Raise orchestrator behind a reverse proxy
docker-compose up --build --force-recreate --no-deps