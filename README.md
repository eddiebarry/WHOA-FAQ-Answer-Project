# WHOA-FAQ-Answer-Project

### To install
```
docker build -t faq_project .
docker run -p 5001:5001 --name faq_project_dev -i -t faq_project
exit()
```

### To restart
```
docker stop faq_project_dev
docker rm faq_project_dev
docker build -t faq_project .
docker run -p 5001:5001 --name faq_project_dev -i -t faq_project
```

### To run
```
docker start faq_project_dev
docker exec -it faq_project_dev /bin/bash
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
git submodule foreach git checkout -b adding_dynamic_qasking
git checkout -b adding_dynamic_qasking
```

### checking out and work on a existing branch
```
git submodule foreach git checkout adding_dynamic_qasking
git checkout adding_dynamic_qasking
git submodule foreach git push --set-upstream origin adding_dynamic_qasking
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


### Loading model only once
[StackOverflow](https://stackoverflow.com/questions/32213893/how-to-cache-a-large-machine-learning-model-in-flask)