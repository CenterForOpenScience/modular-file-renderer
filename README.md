# MFR (Modular File Renderer)

`master` Build Status: [![Build Status](https://travis-ci.org/CenterForOpenScience/modular-file-renderer.svg?branch=master)](https://travis-ci.org/CenterForOpenScience/modular-file-renderer)

`develop` Build Status: [![Build Status](https://travis-ci.org/CenterForOpenScience/modular-file-renderer.svg?branch=develop)](https://travis-ci.org/CenterForOpenScience/modular-file-renderer)

A Python package for rendering files to HTML via an embeddable iframe.

### Compatibility

MFR is compatible with Python 3.5 (tested up to 3.5.3) and 3.6.


### Documentation

Documentation available at: http://modular-file-renderer.readthedocs.io/en/latest/

### Setting up

Install the latest version of python3.5.

For MacOSX users:

```bash
brew install python3
# optional, needed for some converters
brew install pspp unoconv
```
For Ubuntu users:

```bash
apt-get install python3
# optional, needed for some converters
apt-get install pspp unoconv
```

After installing python3.5, create the virtual environment with the following commands:

```bash
pip install virtualenv
pip install virtualenvwrapper
mkvirtualenv --python=`which python3.5` mfr
pip install setuptools==30.4.0
pip install invoke==0.11.1
invoke install
invoke server
```

### Configuring

MFR configuration is done through a JSON file (`mfr-test.json`) that lives in the `.cos` directory of your home directory.  If this is your first time setting up MFR or its sister project, [WaterButler](https://github.com/CenterForOpenScience/waterbutler/), you probably do not have this directory and will need to create it:

```bash
mkdir ~/.cos
```

The defaults should suffice for most local testing.  If you're running the OSF on something other than `http://localhost:5000/`, you'll need to update the `ALLOWED_PROVIDER_DOMAINS` settings value:

```json
{
  "SERVER_CONFIG": {
    "ALLOWED_PROVIDER_DOMAINS": ["http://localhost:9999/"]
  }
}
```

If you encounter the error message `TypeError: throw() takes 2 positional arguments but 4 were given`, you've run into a [core asyncio bug](https://bugs.python.org/issue25394)!  This bug is triggered by turning on debugging. You'll need to set the `SERVER_CONFIG.DEBUG` flag to `false`:

```json
{
  "SERVER_CONFIG": {
    "DEBUG": false
  }
}
```

### Testing

Before running the tests, you will need to install some additional requirements. In your checkout, run:

```bash
invoke install --develop
invoke test
```

### Known Issues

 - Running `invoke install -d` with setuptools v31 or greater can break MFR.  The symptom error message is: `"AttributeError: module 'mfr' has no attribute '__version__'".`  If you encounter this, you will need to remove the file
`mfr-nspkg.pth` from your virtualenv directory, run `pip install setuptools==30.4.0`, then re-run `invoke install -d`.

- The error `def create_default_context(purpose=ssl.Purpose.SERVER_AUTH, *, cafile=None, capath=None, cadata=None): SyntaxError: invalid syntax` can be fixed by restarting your virtual environment. The problem should not reoccur.

### Create your own module

Interested in adding support for a new provider or file format? Check out the CONTRIBUTING.rst docs.

### License

Copyright 2013-2016 Center for Open Science

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

### COS is hiring!

Want to help save science? Want to get paid to develop free, open source software? [Check out our openings!](https://cos.io/jobs/)
