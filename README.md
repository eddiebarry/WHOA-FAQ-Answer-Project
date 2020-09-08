# WHOA-FAQ-Answer-Project

### To install
```
docker build -t faq_project .
docker run -p 5001:5001 --name faq_project_test -i -t faq_project
exit()
```

### To restart
```
docker stop faq_project_test
docker rm faq_project_test
docker build -t faq_project .
docker run -p 5001:5001 --name faq_project_test -i -t faq_project
```

### To run
```
docker start faq_project_test
docker exec -it faq_project_test /bin/bash
```

### Function for updating all submodules
```
git submodule foreach git pull origin adding_first_500_QA_pairs_branch
git add .
git commit -m "updating submodules"
git push origin adding_first_500_QA_pairs_branch
```
### adding_first_500_QA_pairs_branch

### Loading model only once
[StackOverflow](https://stackoverflow.com/questions/32213893/how-to-cache-a-large-machine-learning-model-in-flask)