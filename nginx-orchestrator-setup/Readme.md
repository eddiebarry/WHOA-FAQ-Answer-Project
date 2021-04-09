### Docker setup
docker build -t reverse_proxy .

## Go to nginx
docker build -t server_host .

## Raise orchestrator behind a reverse proxy
docker-compose up --build --force-recreate --no-deps