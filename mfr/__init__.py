# -*- coding: utf-8 -*-
import os

__version__ = '0.1.0-dev'
__author__ = 'Center for Open Science'


from mfr.core import render, detect, FileHandler, get_file_extension, register_filehandler, export, get_file_exporters


PACKAGE_DIR = os.path.abspath(os.path.dirname(__file__))
