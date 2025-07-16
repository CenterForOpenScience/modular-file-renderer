FROM python:3.13-slim

# ensure uno libs are on PYTHONPATH
ENV PYTHONPATH=/usr/lib/python3/dist-packages

RUN usermod -d /home www-data \
    && chown www-data:www-data /home \
    # -slim images strip man dirs, but java won't install unless this dir exists.
    && mkdir -p /usr/share/man/man1 \
    && apt-get update \
    # HACK: work around bug in install java (dep of libreoffice)
    && apt-get install -y ca-certificates-java \
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
        libpng-dev \
        libtiff5-dev \
        libxml2-dev \
        libxslt1-dev \
        zlib1g-dev \
        gnupg2 \
        # convert .step to jsc3d-compatible format
        freecad \
        # pspp dependencies
        pspp \
        # libreoffice from Debian
        libreoffice \
        # grab gosu for easy step-down from root
        gosu \
    # install unoserver for headless UNO
    && pip install --no-cache-dir unoserver \
    && apt-get clean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /code
WORKDIR /code

COPY pyproject.toml poetry.lock* /code/

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_VIRTUALENVS_IN_PROJECT=1

RUN pip install poetry==2.1.2 setuptools==80.1.0 \
    && poetry install --no-root --without=docs

# Copy the rest of the code over
COPY ./ /code/

ARG GIT_COMMIT=
ENV GIT_COMMIT=${GIT_COMMIT}

RUN python3 setup.py egg_info
RUN python3 -m pip install .

EXPOSE 7778 2002

CMD ["bash", "-lc", "unoserver --listener --server=0.0.0.0 --port=2002 & exec gosu www-data invoke server"]
