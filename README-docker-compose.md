## Adding new extensions
When adding a new extension you will need to add it properly in `setup.py` and then run a build.

1. In `setup.py` add your new extension in the form of:
```python
'.<extension-name> = mfr.extensions.<extension-name>:<renderer-or-exporter-name>',

```
Make sure you place it under the correct `mfr.exporters` or `mfr.renderers` section.

2. Make sure your docker-sync is running.

3. Run
```bash
python setup.py build
```
This will build your `mfr.egg-info` folder and add the new entrypoints. You can remove the build directory afterwards

## Building a new image
When working on an exporter or renderer, you may need outside software to export certain file types. In order to do this easily you will  need to edit the `Dockerfile` and rebuild an image off it.

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
        <new program>\
```

1. You can usually just add the required tool to this list in the dockerfile as so.
2. In the same directory as your dockerfile run:
``` bash
docker build -t <image-name> ./>
```
If this is your first time running this command in a while it will take quite a while to finish.

3. In order to use your new image, you will have to change the `docker-compose.yml` file in your copy of the OSF. Comment out the default and add your own.

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

4. Running `docker-compose up -d` should now bring up MFR based on your new image.


## Running mfr_requirements
When you add a new python library to the requirements.txt, you can install it by running the `mfr_requirements` container.

1. Bring up your MFR container with
```bash
docker-compose up --no-deps --force-recreate mfr
```
Make sure you are in your OSF directory

2.  Run
```bash
docker-compose up mfr_requirements
```

3. Sometimes the requirements will get stuck. Restarting the container/docker/trying again will help. Eventually it should work.

## Manually installing packages and programs in a docker container
While not always the best solution, sometimes it can be useful to forgo running mfr-requirements or building an image. When this is the case, you can exec into a docker container directly and install them. This is mostly useful for testing/updating packages.

1. Find your container ID

```bash
docker ps | grep mfr
```
Usually you only need the first 3 characters of the id

2. Exec into the container
```bash
docker-exec -ti <id> bash
```

3. Once inside the container run `apt-get update` and then you can install any package you need.

## Logging information
You can create a logger and use it to report whatever information you want.

1. Import logging and create a logger.

```bash
import logging
logger = logging.getLogger(__name__)
```

2. You can now log with the command `logger.info`

```bash
name = 'log me!'
logger.info(name)
```
3. To find the log, use `docker-compose logs -f --tail 1000 mfr` or recreate the container and leave it attached to your terminal. IE `docker-compose up --no-deps --no-recreate mfr`

## Docker is not syncing correctly
If your docker is not syncing correctly, most of the time it can be one of a few problems

1. Make sure your `docker-sync.yml` and `docker-compose.override.yml` files are set up correctly.

2. Run `docker-sync clean`
