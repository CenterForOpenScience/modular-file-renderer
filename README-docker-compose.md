# MFR docker-compose README
Note: These instructions are for running with the [Open Science Framework](https://github.com/CenterForOpenScience/osf.io/) (OSF) and its docker-compose setup.  [Check here](https://github.com/CenterForOpenScience/osf.io/blob/develop/README-docker-compose.md) for more info on working with docker/docker-compose/docker-sync. 

## Adding new extensions
When adding a new extension you will need to add it properly in `setup.py` and then run a `invoke install`.

* In `setup.py` add your new extension in the form of:
```python
'<extension-name> = mfr.extensions.<extension-name>:<renderer-or-exporter-name>',
```

* Make sure you place it under the correct `mfr.exporters` or `mfr.renderers` section.

* Check that your docker-sync is running.

* If you are not in your MFR `virtualenv`, bring it up.

* Run:

```bash
invoke install
```

* This will build your `mfr.egg-info` folder and add the new entrypoints.

## Building a new image
When working on an exporter or renderer, you may need a third party library to export certain file types. In order to do this easily you will need to edit the `Dockerfile` and rebuild your image.

Example Dockerfile changes
```bash
RUN apt-get update \
    # mfr dependencies
    && apt-get install -y \
        git \
        make \
        gcc \
        build-essential \
        gfortran \
        r-base \
        <new program> \
```

* You can usually just add the required tool to this list in the dockerfile as above.

* In the same directory as your dockerfile run:

``` bash
docker build -t <image-name> ./>
```
* If docker hasn't cached this command recently it will take quite a while to finish.

* In order to use your new image, you will have to change the `docker-compose.yml` file in your copy of the OSF. Comment out the default and add your own.

```bash
  mfr:
    image: <image-name> # quay.io/centerforopenscience/mfr:develop
    command: invoke server
    restart: unless-stopped
    ports:
      - 7778:7778
    env_file:
      - .docker-compose.mfr.env
    volumes:
      - mfr_requirements_vol:/usr/local/lib/python3.5
      - mfr_requirements_local_bin_vol:/usr/local/bin
    stdin_open: true
```

* Running `docker-compose up -d` should now bring up MFR based on your new image.


## Running mfr_requirements
When you add a new python library to the requirements.txt, you can install it by running the `mfr_requirements` container.

* Make sure you are in your OSF directory.

* Bring up your MFR container with:

```bash
docker-compose up --no-deps --force-recreate mfr
```

* Then run:

```bash
docker-compose up mfr_requirements
```

* Sometimes the requirements will get stuck. Restarting the container, docker, or trying again can help.


## Manually installing packages and programs in a docker container
While not always the best solution, sometimes it can be useful to forgo running mfr_requirements or building an image. When this is the case, you can exec into a docker container directly and install them. This is mostly useful for testing/updating packages.

* Find your container ID:

```bash
docker ps | grep mfr
```
* Usually you only need the first 3 characters of the id.

* Exec into the container:

```bash
docker-exec -ti <id> bash
```

* Once inside the container run your command. If you are using pip, just pip install your required package. If you need to `apt-get install` something, run `apt-get update` and then you can install the package you need.

## Logging information
You can create a logger and use it to report whatever information you want.

* In your python file import logging and create a logger.

```python
  import logging
  logger = logging.getLogger(__name__)
```

* You can now log with the command `logger.info`.

```python
name = 'log me!'
logger.info(name)
```

* To find the log, use `docker-compose logs -f --tail 1000 mfr` or recreate the container and leave it attached to your terminal. IE `docker-compose up --no-deps --no-recreate mfr`.

* Make sure you remove your debugging statements before committing.

## Docker is not syncing correctly
If your docker is not syncing correctly, most of the time it can be one of a few problems.

* Make sure your `docker-sync.yml` and `docker-compose.override.yml` files are set up correctly.

* Run `docker-sync clean`

## Setting up Keen logging in MFR or Waterbutler.

* Go to https://keen.io/ and make an account.

* Locate your unique logging key and ID after making a project.

* Add your keys [here](https://github.com/CenterForOpenScience/waterbutler/blob/develop/waterbutler/settings.py). It should look something like this:

```python
KEEN_PRIVATE_PROJECT_ID = keen_private_config.get_nullable('PROJECT_ID', <YOUR_ID_HERE>)
KEEN_PRIVATE_WRITE_KEY = keen_private_config.get_nullable('WRITE_KEY', <YOUR_KEY_HERE>)
```

* Restart MFR and download a file. Information should appear on your Keen stream.

## Setting up Sentry logging in MFR or Waterbutler.

* Go to https://sentry.io/welcome/ and create an account.

* Make a python project and get your unique url.

* Add your keys [here](https://github.com/CenterForOpenScience/waterbutler/blob/develop/waterbutler/settings.py).
It should look something like this:

```python
SENTRY_DSN = config.get_nullable('SENTRY_DSN', <YOUR_SENTRY_URL_HERE>)
```

* Trigger an error in MFR or in Waterbutler and make sure it is logged correctly to Sentry. 

