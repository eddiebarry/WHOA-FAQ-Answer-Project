ARG VERSION=3.7
FROM python:$VERSION

WORKDIR /usr/src
RUN pip install tokenizers==0.7 transformers==2.10.0 \
    torch==1.5.0 flask==1.1.2 pandas==1.1.1 \
    tensorflow==2.3.0 xlrd==1.2.0 numpy==1.18\
    spacy==2.3.2 spacy-wordnet==0.0.4 \
    sklearn==0.0 pysolr==3.9.0 strsim==0.0.3 gunicorn==20.0.4 pytest python-dotenv==0.15.0
RUN python -m nltk.downloader wordnet \
    && python -m nltk.downloader omw && python -m spacy download en

ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache
RUN git clone \
    --recursive https://github.com/eddiebarry/WHOA-FAQ-Answer-Project.git
WORKDIR /usr/src/WHOA-FAQ-Answer-Project/WHO-FAQ-Search-Engine/variation_generation/variation_generator_model_weights
RUN chmod +x ./gdown.pl \
    && ./gdown.pl https://drive.google.com/file/d/1jsIH4q0CU33sEFBzyIcFCucmNuisgJ5v/view?usp=sharing query_expansion_weights.zip \
    && unzip query_expansion_weights.zip \
    && rm query_expansion_weights.zip

WORKDIR /usr/src/WHOA-FAQ-Answer-Project
EXPOSE 5009
#gunicorn --bind 0.0.0.0:5008 wsgi:app --timeout 600
# ENTRYPOINT [ "python" ] 
# CMD [ "app.py" ] 