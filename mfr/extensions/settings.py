from mfr import settings

config = settings.child('EXTENSION_CONFIG')

# LOCAL_DEVELOPMENT must be set to true for extensions that produce a waterbutler URL in the
# TEMPLATE to render, when using local docker development environment. Call will be coming from
# browser instead of docker container.

LOCAL_DEVELOPMENT = config.get_bool('LOCAL_DEVELOPMENT', False)
DOCKER_LOCAL_HOST = config.get('DOCKER_LOCAL_HOST', '192.168.168.167')
LOCAL_HOST = config.get('LOCAL_HOST', 'localhost')
