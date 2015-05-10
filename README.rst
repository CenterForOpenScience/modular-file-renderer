***
mfr
***
.. image:: https://travis-ci.org/CenterForOpenScience/modular-file-renderer.svg?branch=dev
    :target: https://travis-ci.org/CenterForOpenScience/modular-file-renderer

**WARNING: mfr is in a very alpha stage of development. As such, it's API is in constant flux. Expect many breaking changes.**

**mfr** (short for "modular file renderer") is a Python package for rendering files to HTML.

Requirements
============

- Python >= 3.3


### startup commands

```bash
# Make sure that you are using >= python3.3
pip install -U -r requirements.txt
python setup.py develop
invoke server
```

Available modules
=================

There are a number of 3rd-party modules available.

- `mfr_md <https://github.com/TomBaxter/mfr_md>`_

Make your own, then submit a pull request to add it to this list!


Create your own module
======================

Interested in adding support for a new file format? Check out the CONTRIBUTING.rst docs.


License
=======

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
