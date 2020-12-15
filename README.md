# WHOA-FAQ-Answer-Project

### To install
```
docker build -t faq_project_output_format_new_flow .
docker run -p 5009:5009 --name faq_project_output_format_new_flow -i -t faq_project_output_format_new_flow
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
wget https://s3.amazonaws.com/botpress-binaries/botpress-v12_10_8-linux-x64.zip
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