import os
import json
import logging
import logging.config

os_env = os.environ

SENTRY_DSN = None

WATERBUTLER_URL = 'http://localhost:7777'
WATERBUTLER_ADDRS = ['127.0.0.1']

# Use Celery for file rendering
USE_CELERY = True

##### Celery #####
## Default RabbitMQ broker
BROKER_URL = 'amqp://'

# Default RabbitMQ backend
CELERY_RESULT_BACKEND = 'amqp://'

# Modules to import when celery launches
CELERY_IMPORTS = (
    'tasks'
)

PROJECT_NAME = 'modular-file-renderer'
PROJECT_CONFIG_PATH = '~/.mfr'

DEFAULT_LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '[%(asctime)s][%(levelname)s][%(name)s]: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'console'
        },
        'syslog': {
            'class': 'logging.handlers.SysLogHandler',
            'level': 'INFO'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console']
    }
}

try:
    config_path = os.environ['{}_CONFIG'.format(PROJECT_NAME.upper())]
except KeyError:
    env = os.environ.get('ENV', 'test')
    config_path = '{}/{}-{}.json'.format(PROJECT_CONFIG_PATH, PROJECT_NAME, env)


config = {}
config_path = os.path.expanduser(config_path)
if not os.path.exists(config_path):
    logging.warning('No \'{}\' configuration file found'.format(config_path))
else:
    with open(os.path.expanduser(config_path)) as fp:
        config = json.load(fp)


def get(key, default):
    return config.get(key, default)

logging_config = get('LOGGING', DEFAULT_LOGGING_CONFIG)
logging.config.dictConfig(logging_config)
