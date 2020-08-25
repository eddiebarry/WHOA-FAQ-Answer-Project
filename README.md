# WHOA-FAQ-Answer-Project

### To install
```
docker build -t faq_project .
docker run --name faq_project_test -i -t faq_project
exit()
```

### To run
```
docker start faq_project_test
docker exec -it faq_project_test /bin/bash
```

### Function for updating all submodules
```
git submodule foreach git pull origin master
git add .
git commit -m "updating submodules"
git push origin master
```