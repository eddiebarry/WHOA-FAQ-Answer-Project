# WHOA-FAQ-Answer-Project

### To install
```
docker build -t faq_project .
docker run --name faq_project_test -i -t faq_project
exit()
```

### To run
```
docker start faq_project
docker run -it faq_project /bin/bash
```

### Function for updating all submodules
```
git submodule foreach git pull origin master
```