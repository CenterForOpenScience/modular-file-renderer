FROM python:3.5-slim

#
# * example usage:
#
# $ docker build -t="mfr" .
#
# $ docker run -d -p 7778:7778 \
#    -e SERVER_CONFIG_ADDRESS=0.0.0.0 \
#    -e SERVER_CONFIG_PROVIDER_NAME=http \
#    -e SERVER_CONFIG_ALLOWED_PROVIDER_DOMAINS=http://www.example.com/  \
#    --name mfr_server \
#    mfr
#



EXPOSE 7778
CMD ["circusd", "--log-level=ERROR", "/etc/circus.ini"]

RUN usermod -d /home www-data && chown www-data:www-data /home

RUN apt-get update \
    # mfr dependencies
    && apt-get install -y \
        git \
        make \
        gcc \
        build-essential \
        gfortran \
        r-base \
        libblas-dev \
        libevent-dev \
        libfreetype6-dev \
        libjpeg-dev \
        libpng12-dev \
        libxml2-dev \
        libxslt1-dev \
        zlib1g-dev \
    # installing vim so the mfr-test.json config can be customized
        vim \
    # unoconv dependencies
    && apt-get install -y \
        unoconv \
    # pspp dependencies
    && apt-get install -y \
        pspp \
    && apt-get clean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# grab gosu for easy step-down from root
ENV GOSU_VERSION 1.4
RUN apt-get update \
    && apt-get install -y \
        curl \
    && gpg --keyserver pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4 \
    && curl -o /usr/local/bin/gosu -SL "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$(dpkg --print-architecture)" \
  	&& curl -o /usr/local/bin/gosu.asc -SL "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$(dpkg --print-architecture).asc" \
  	&& gpg --verify /usr/local/bin/gosu.asc \
  	&& rm /usr/local/bin/gosu.asc \
  	&& chmod +x /usr/local/bin/gosu \
    && apt-get clean \
    && apt-get autoremove -y \
        curl \
    && rm -rf /var/lib/apt/lists/*

# ensure unoconv can locate the uno library
ENV PYTHONPATH=/usr/lib/python3/dist-packages

RUN mkdir -p /code
WORKDIR /code

RUN pip install -U pip
RUN pip uninstall -y setuptools
RUN rm -f /usr/local/lib/python3.5/site-packages/mfr-nspkg.pth
RUN pip install setuptools==30.4.0

COPY ./requirements.txt /code/

RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy the rest of the code over
COPY ./ /code/

ARG GIT_COMMIT=
ENV GIT_COMMIT ${GIT_COMMIT}

RUN python setup.py develop

RUN pip install circus

COPY circus.ini /etc/circus.ini

RUN mkdir -p /root/.cos/

COPY travis-config.json /root/.cos/waterbutler-test.json
COPY travis-config.json /root/.cos/mfr-test.json
