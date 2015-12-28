# MFR (Modular File Renderer)

`master` Build Status: [![Build Status](https://travis-ci.org/CenterForOpenScience/modular-file-renderer.svg?branch=master)](https://travis-ci.org/CenterForOpenScience/modular-file-renderer)

`develop` Build Status: [![Build Status](https://travis-ci.org/CenterForOpenScience/modular-file-renderer.svg?branch=develop)](https://travis-ci.org/CenterForOpenScience/modular-file-renderer)

A Python package for rendering files to HTML via an embeddable iframe.

### Startup commands

```bash
# MacOSX: Install the latest version of python3
brew install python3
brew install r
pip install virtualenv
pip install virtualenvwrapper
mkvirtualenv --python=`which python3` mfr
invoke install --develop
invoke server
```

```bash
# ubuntu: Install the latest version of python3.5
apt-get install python3.5
apt-get install r-base
pip install virtualenv
pip install virtualenvwrapper
mkvirtualenv --python=`which python3.5` mfr
pip install invoke
invoke install --develop
invoke server
```

### Create your own module

Interested in adding support for a new provider or file format? Check out the CONTRIBUTING.rst docs.

### License 

Copyright 2013-2015 Center for Open Science

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
