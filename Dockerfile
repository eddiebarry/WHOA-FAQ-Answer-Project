FROM python:3.7

WORKDIR /usr/src

RUN pip install tokenizers==0.7 transformers==2.10.0 \
    torch==1.5.0 flask==1.1.2 pandas==1.1.1 \
    tensorflow==2.3.0 xlrd==1.2.0 numpy==1.18\
    spacy==2.3.2 spacy-wordnet==0.0.4 \
    sklearn==0.0 pysolr==3.9.0 strsim==0.0.3 gunicorn==20.0.4 pytest python-dotenv==0.15.0 --no-cache-dir

RUN python -m nltk.downloader wordnet -d /root\
    && python -m nltk.downloader omw -d /root && python -m spacy download en\
    && python -m nltk.downloader punkt -d /root && python -m nltk.downloader stopwords -d /root


ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache


RUN git clone --branch feature/performance-profiling\
    --recursive https://github.com/eddiebarry/WHOA-FAQ-Answer-Project.git

WORKDIR /usr/src/WHOA-FAQ-Answer-Project/WHO-FAQ-Search-Engine/variation_generation/variation_generator_model_weights

RUN  wget -O query_expansion_weights.zip https://s3-eu-west-1.amazonaws.com/model.weights.project.interakt/query_expansion_weights.zip \
    && unzip query_expansion_weights.zip \
    && rm query_expansion_weights.zip

WORKDIR /usr/src/WHOA-FAQ-Answer-Project

RUN chown 1000680000 -R /root

RUN chmod 777 -R /root

# RUN python /usr/src/WHOA-FAQ-Answer-Project/WHO-FAQ-Search-Engine/variation_generation/__init__.py

EXPOSE 5009


ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:5009", "wsgi:app", "--timeout", "600", '--workers=9']


# gunicorn --bind 0.0.0.0:5009 wsgi:app --timeout 600 --workers=9
# gunicorn server:app -k gevent --worker-connections 1000