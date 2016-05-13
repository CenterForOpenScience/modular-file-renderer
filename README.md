# MFR (Modular File Renderer)

`master` Build Status: [![Build Status](https://travis-ci.org/CenterForOpenScience/modular-file-renderer.svg?branch=master)](https://travis-ci.org/CenterForOpenScience/modular-file-renderer)

`develop` Build Status: [![Build Status](https://travis-ci.org/CenterForOpenScience/modular-file-renderer.svg?branch=develop)](https://travis-ci.org/CenterForOpenScience/modular-file-renderer)

A Python package for rendering files to HTML via an embeddable iframe.

### Startup commands

Install the latest version of python3.5.

For MacOSX users:

```bash
brew install python3
brew install r
```
For Ubuntu users:

```bash
apt-get install python3
apt-get install r-base
```

After installing python3.5, create the virtual environment with the following commands:

```bash
pip install virtualenv
pip install virtualenvwrapper
mkvirtualenv --python=`which python3` mfr
pip install invoke
invoke install --develop
invoke server
```
### Testing Configuration (optional)

MFR looks for local configuration in `~/.cos/mfr-test.json`.  The defaults should suffice for most local testing.  If you're running the OSF on something other than `http://localhost:5000/`, you'll need to update the `ALLOWED_PROVIDER_DOMAINS` settings value:

```json
{
  "SERVER_CONFIG": {
    "ALLOWED_PROVIDER_DOMAINS": ['http://localhost:9999/']
  }
}
```

If you encounter the error message `TypeError: throw() takes 2 positional arguments but 4 were given`, you've run into a [core asyncio bug](https://bugs.python.org/issue25394)!  This bug is triggered by turning on debugging. You'll need to set `SERVER_CONFIG.DEBUG` to `false` in your `mfr-test.json`, e.g.

```json
{
  "SERVER_CONFIG": {
    "DEBUG": false
  }
}
```

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

### COS is Hiring!

Want to help save science? Want to get paid to develop free, open source software? [Check out our openings!](http://cos.io/jobs)
