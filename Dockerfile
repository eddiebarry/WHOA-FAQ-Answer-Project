ARG VERSION=3.7
FROM python:$VERSION

RUN apt-get update \
    && apt-get install -y default-jdk ant

WORKDIR /usr/lib/jvm/default-java/jre/lib
RUN ln -s ../../lib amd64

WORKDIR /usr/src/pylucene
RUN curl https://downloads.apache.org/lucene/pylucene/pylucene-8.3.0-src.tar.gz \
    | tar -xz --strip-components=1
RUN cd jcc \
    && NO_SHARED=1 JCC_JDK=/usr/lib/jvm/default-java python setup.py install
RUN make all install JCC='python -m jcc' ANT=ant PYTHON=python NUM_FILES=8

WORKDIR /usr/src
RUN rm -rf pylucene
RUN pip install tokenizers==0.7 transformers==2.10.0 \
    torch==1.4.0 flask==1.1.2 pandas==1.1.1 \
    tensorflow==2.3.0 xlrd==1.2.0 \
    spacy==2.3.2 spacy-wordnet==0.0.4
RUN python -m nltk.downloader wordnet \
    && python -m nltk.downloader omw && python -m spacy download en
RUN pip install sklearn pysolr==3.9.0

ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache
RUN git clone --branch Output_format_change\
    --recursive https://github.com/eddiebarry/WHOA-FAQ-Answer-Project.git
WORKDIR /usr/src/WHOA-FAQ-Answer-Project/WHO-FAQ-Search-Engine/variation_generation/variation_generator_model_weights
RUN chmod +x ./gdown.pl \
    && ./gdown.pl https://drive.google.com/file/d/1jsIH4q0CU33sEFBzyIcFCucmNuisgJ5v/view?usp=sharing query_expansion_weights.zip \
    && unzip query_expansion_weights.zip \
    && rm query_expansion_weights.zip

WORKDIR /usr/src/WHOA-FAQ-Answer-Project

EXPOSE 5008
# ENTRYPOINT [ "python" ] 
# CMD [ "app.py" ] 