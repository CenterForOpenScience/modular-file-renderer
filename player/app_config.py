import os
_basedir = os.path.abspath(os.path.dirname(__file__))

FILES_DIR = os.path.join(_basedir, 'files')

DEBUG = True

HOST = '127.0.0.1'
PORT = 5000

SECRET_KEY = 'some_secret_key'

THREADS_PER_PAGE = 8

CSRF_ENABLED = True

CSRF_SESSION_KEY = "some_session_key"
