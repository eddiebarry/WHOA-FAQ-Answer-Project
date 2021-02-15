# WHOA-FAQ-Answer-Project

### To install
```
docker build -t faq_project_output_format_new_flow .
docker run -e NLTK_DATA=/root -p 5009:5009 --name faq_project_output_format_new_flow -it faq_project_output_format_new_flow /bin/bash
exit()
```

### To restart
```
docker stop faq_project_output_format_new_flow
docker rm faq_project_output_format_new_flow
docker build -t faq_project_output_format_new_flow .
docker run -p 5009:5009 --name faq_project_output_format_new_flow -i -t faq_project_output_format_new_flow
```

### To run
```
docker start faq_project_output_format_new_flow
docker exec -it faq_project_output_format_new_flow /bin/bash
```

### Function for updating all submodules int master
```
branch_name=master
git submodule foreach git pull origin $branch_name
git add .
git commit -m "updating submodules"
git push origin $branch_name
```

### checking out and work on a new branch
```
branch_name=new_branch_name
git submodule foreach git checkout -b $branch_name
git checkout -b $branch_name
```

### checking out and work on a existing branch
```
git submodule foreach git checkout $branch_name
git checkout $branch_name
git submodule foreach git push --set-upstream origin $branch_name
```

### merging all branches and returning to master
```
branch_name=adding_dynamic_qasking
array=(WHO-FAQ-Dialog-Manager/ WHO-FAQ-Keyword-Engine/ WHO-FAQ-Search-Engine/ WHO-FAQ-Update-Engine/)

for i in "${array[@]}"
do
	cd $i
    git init
    git checkout master
    git merge $branch_name
    cd ..
done
```

### clone a particular branch
```
git clone -b $branch_name \
    --recursive \
    https://github.com/eddiebarry/WHOA-FAQ-Answer-Project.git
```

### Loading model only once
[StackOverflow](https://stackoverflow.com/questions/32213893/how-to-cache-a-large-machine-learning-model-in-flask)


### botpress quick install
```
mkdir bot
cd bot
wget https://s3.amazonaws.com/botpress-binaries/botpress-v12_17_1-linux-x64.zip
sudo apt install unzip
unzip botpress-v12_10_8-linux-x64.zip
./bp
```

### install docker
```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### bot dependencies
```
Keyword Directory for keyword engine
QA+Keyword pairs for Bot search engine
Questions per category
```

### To test
```
pytest ./test
```

### Create a buildconfig

```
build_name=orchestrator-container
cat Dockerfile | oc new-build --name $build_name --dockerfile='-'
oc start-build bc/$build_name  --follow
```


### Build botpresss bot
```
docker pull quay.io/whoacademy/botpress-qna-bot
docker run -p 3000:3000 -it --name botpress_project quay.io/whoacademy/botpress-qna-bot /bin/bash
<!-- make changes to bot -->
docker commit botpress_project quay.io/whoacademy/image_repo_name
docker push quay.io/whoacademy/image_repo_name
```

### Setup redis server
#make sure you have base image available
oc create -f https://raw.githubusercontent.com/mjudeikis/redis-openshift/master/openshift/is-base.yaml -n openshift
#create all components
oc create -f https://raw.githubusercontent.com/mjudeikis/redis-openshift/master/list.yaml
#start build and watch 
oc start-build redis-build


### copy logs from remote

#### first login and move logs to disk
```
ssh -i gpu_instance_key.pem.txt ubuntu@ec2-52-16-246-42.eu-west-1.compute.amazonaws.com
docker cp 4561dd7937b7:/usr/src/WHOA-FAQ-Answer-Project/logs/log.txt ./bot_log.txt
```
#### copy to local
```
scp -i gpu_instance_key.pem.txt ubuntu@ec2-52-16-246-42.eu-west-1.compute.amazonaws.com:/home/ubuntu/bot_log.txt ./temp.txt
```

### asynch
```
gunicorn --worker-class gevent   --workers 2   --bind 0.0.0.0:5009   service:app --worker-connections 1000
```