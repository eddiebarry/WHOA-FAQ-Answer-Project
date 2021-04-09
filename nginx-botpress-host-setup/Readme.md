container_name=nginx
docker build -t $container_name . && docker run -it --net=host $container_name

docker rm nginx_load_balance
docker build -t nginx_test .
docker run --net=host --name nginx_load_balance nginx_test




# Rebuild
```
docker build -t reverseproxy .
docker-compose up --build --force-recreate --no-deps
```

# Install
```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

sudo curl -L "https://github.com/docker/compose/releases/download/1.28.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```