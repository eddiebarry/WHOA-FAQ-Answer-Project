# Create a dockerfile
docker build --tag botpress .

# login to quay
docker login quay.io

# Create a quay repo
USE GUI

# Commit 
docker commit $container_id $quay_repo_name

# Create a deployment
Use deployment.yaml
Change image name

# give write permissions to all of temp data
chmod a+w -R /temp/

quay_repo_name=quay.io/whoacademy/botpress-team-jarvis

# Push to quay
docker push $quay_repo_name

# Use deployment.yaml to create a deployment
set env variable APP_DATA_PATH = /temp

# create a service which exposes port 3000 for the app you created

# create a route with edge encryption to create a https connection