FROM python:3.13-slim


RUN usermod -d /home www-data \
    && chown www-data:www-data /home \
    && apt-get update

    # mfr dependencies
RUN apt-get install -y \
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
        # grab gosu for easy step-down from root
        gosu
RUN apt-get clean
RUN apt-get autoremove -y
RUN rm -rf /var/lib/apt/lists/*

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

RUN poetry install --without=docs

EXPOSE 7778

CMD ["gosu", "www-data", "invoke", "server"]
