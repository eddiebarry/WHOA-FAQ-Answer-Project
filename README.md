# WHOA-FAQ-Answer-Project

### To install
```
docker build --tag=faq_project_docker .
docker run -it --name faq_project faq_project_docker:latest
exit
```

### To run
```
docker start faq_project
docker run -it faq_project /bin/bash
```