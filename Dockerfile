FROM python:3.5-slim

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
    # unoconv dependencies
    && apt-get install -y \
        unoconv \
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

RUN mkdir -p /code
WORKDIR /code

RUN pip install -U pip

COPY ./requirements.txt /code/

RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy the rest of the code over
COPY ./ /code/

EXPOSE 7778

CMD ["gosu", "nobody", "invoke", "server"]
