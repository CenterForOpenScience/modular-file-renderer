# -*- coding: utf-8 -*-
import re
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


def find_version(fname):
    '''Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    '''
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version

__version__ = find_version("mfr/__init__.py")


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content

setup(
    name='mfr',
    version=__version__,
    description='HTML file renderer for Python',
    long_description=(read("README.rst") + '\n\n' +
                      read("HISTORY.rst")),
    author='Center for Open Science',
    author_email='contact@cos.io',
    url='https://github.com/CenterForOpenScience/modular-file-renderer',
    packages=find_packages(exclude=("test*", "player*")),
    include_package_data=True,
    package_data={
        "": ['templates/*', 'static/*/*'],
    },
    license=read("LICENSE"),
    zip_safe=False,
    keywords='mfr',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    entry_points={
        'console_scripts': [
            "mfr = mfr.cli:main"
        ]
    },
    test_suite='tests',
    tests_require=['pytest'],
    cmdclass={'test': PyTest}

)
