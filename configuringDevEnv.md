# Configuring the Development Environment for OSF:

Instructions for MacOS Big Sur compiled from [**README-docker-compose.md**](https://github.com/CenterForOpenScience/osf.io/blob/develop/README-docker-compose.md), correspondence with Fitz Elliot, and the [documentation](https://cosdev.readthedocs.io/en/latest/osf/setup.html): modified to fix errors.


- Clone the repository:
$ git clone [osf.io]
$ cd osf.io}

- Install the Docker Client

- Grant Docker minimum resources of 1 CPU, 8GB memory, 2GB swap, and 32GB disk image size

- Alias the loopback interface:

```$ export libdir='/Library/LaunchDaemons'```

$ export file='com.runlevel1.lo0.192.168.168.167.plist'

$ sudo cp $file $libdir

$ sudo chmod 0644 $libdir/$file

$ sudo chown root:wheel $libdir/$file

$ sudo launchctl load $libdir/$file

- Configure application:
$ cp ./website/settings/local-dist.py ./website/settings/local.py
$ cp ./api/base/settings/local-dist.py ./api/base/settings/local.py
$ cp ./docker-compose-dist.override.yml ./docker-compose.override.yml
$ cp ./tasks/local-dist.py ./tasks/local.py

- Start Application:
$ docker compose up requirements mfr_requirements wb_requirements
$ docker compose up -d elasticsearch postgres mongo rabbitmq
$ rm -Rf ./node_modules
$ docker compose up -d assets
$ docker compose up -d admin_assets
$ docker-compose up -d mfr wb fakecas sharejs
$ docker-compose run --rm web python3 manage.py migrate
$ docker-compose up -d worker web api admin preprints registries ember\_osf\_web

- *Note: once it has been setup, you can [quickstart](https://github.com/CenterForOpenScience/osf.io/blob/develop/README-docker-compose.md\#quickstart-running-all-osf-services-in-the-background) to quickly launch in the future.*

- Access the OSF at **http://localhost:5000**.

- Click sign up to create an account.

- Access the 'web' containers logs to view the confirmation email for new accounts:

- $ docker compose logs -f -{}-tail 1000 web

- Copy the confirmation link and paste into the browser to confirm the account then log in using the email address used to create the account. This allows test files, projects, and folders to be created and accessed through the normal methods.


# Instructions for building and testing the modified MFR container:

- Go to the **modular-file-renderer** directory
- $ docker image build -t mfr:local .
- Go to the **osf.io** directory
- Edit the **docker-compose.yml** file. Under **mfr** and **mfr_requirements**, change the image to **image: mfr:local**
- $ docker compose up -d --force-recreate mfr_requirements
- $ docker compose up -d --force-recreate mfr
- Restart the Docker application

### In order to verify that the version of MFR you are running is the correct, most up to date version:

- Modify the version number in **modular-file-renderer/mfr/version.py** to indicate that changes have been made.
- Check the version of the container at **http://localhost:7778/status**
- If the status version number matches the modified version number, you know that the modified version of the MFR container has been successfully built and deployed by Docker.


## Debugging Problems

- Running out of memory in Docker can be solved by doing a system prune of the containers and reinstalling them. Allocating more memory in Docker is a good idea.
- $ docker system prune -a

# Configuring the development environment for MFR:
Instructions for MacOS Big Sur compiled from []**CONTRIBUTING.rst**](https://github.com/CenterForOpenScience/modular-file-renderer/blob/develop/CONTRIBUTING.rst), [**README.md**](https://github.com/CenterForOpenScience/modular-file-renderer/blob/develop/README.md), the [installation documentation](https://modular-file-renderer.readthedocs.io/en/latest/install.html\#install) and the [contribution documentation](https://modular-file-renderer.readthedocs.io/en/latest/contributing.html) and modified to fix errors.

- Clone the repository:
$ git clone [modular-file-renderer]
$ cd modular-file-renderer
- Create the virtual environment:

- $ pip install virtualenv virtualenvwrapper
- $ brew update
- $ brew install python3 r pspp unoconv pyenv

- Add the following initialization lines to either the **~/.bashrc** or **~/.zprofile** files for either bash or zsh shells respectively:
**eval "$(pyenv init -)"**
**eval "$(pyenv virtualenv-init -)"**

- $ source ~/.[bashrc or zprofile]
- $ pyenv virtualenv 3.6.4 mfr
- $ pip install setuptools==37.0.0
- $ pip install invoke==0.13.0
- Modify **requirements.txt** to update the version number for **reportlab==3.4.0** to **reportlab==3.5.56** due to an incompatibility with the old version.
- $ invoke install -d

- In order to run the development unit testing procedure:

- $ invoke test
