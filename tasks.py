import os

from invoke import task

WHEELHOUSE_PATH = os.environ.get('WHEELHOUSE')
CONSTRAINTS_FILE = 'constraints.txt'


def monkey_patch(ctx):
    # Force an older cacert.pem from certifi v2015.4.28, prevents an ssl failure w/ identity.api.rackspacecloud.com.
    #
    # SubjectAltNameWarning: Certificate for identity.api.rackspacecloud.com has no `subjectAltName`, falling
    # back to check for a `commonName` for now. This feature is being removed by major browsers and deprecated by
    # RFC 2818. (See  https://github.com/shazow/urllib3/issues/497  for details.)
    # SubjectAltNameWarning
    import ssl
    import certifi

    _create_default_context = ssl.create_default_context

    def create_default_context(purpose=ssl.Purpose.SERVER_AUTH, *, cafile=None, capath=None, cadata=None):
        if cafile is None:
            cafile = certifi.where()
        return _create_default_context(purpose=purpose, cafile=cafile, capath=capath, cadata=cadata)
    ssl.create_default_context = create_default_context


@task
def wheelhouse(ctx, develop=False):
    req_file = 'dev-requirements.txt' if develop else 'requirements.txt'
    cmd = 'pip wheel --find-links={} -r {} --wheel-dir={} -c {}'.format(WHEELHOUSE_PATH, req_file, WHEELHOUSE_PATH, CONSTRAINTS_FILE)
    ctx.run(cmd, pty=True)


@task
def install(ctx, develop=False):
    ctx.run('python setup.py develop')
    req_file = 'dev-requirements.txt' if develop else 'requirements.txt'
    cmd = 'pip install --upgrade -r {} -c {}'.format(req_file, CONSTRAINTS_FILE)

    if WHEELHOUSE_PATH:
        cmd += ' --no-index --find-links={}'.format(WHEELHOUSE_PATH)
    ctx.run(cmd, pty=True)


@task
def flake(ctx):
    ctx.run('flake8 .', pty=True)


@task
def test(ctx, verbose=False):
    flake(ctx)
    cmd = 'py.test --cov-report term-missing --cov mfr tests'
    if verbose:
        cmd += ' -v'
    ctx.run(cmd, pty=True)


@task
def server(ctx):
    monkey_patch(ctx)

    if os.environ.get('REMOTE_DEBUG', None):
        import pydevd
        # e.g. '127.0.0.1:5678'
        remote_parts = os.environ.get('REMOTE_DEBUG').split(':')
        pydevd.settrace(remote_parts[0], port=int(remote_parts[1]), suspend=False, stdoutToServer=True, stderrToServer=True)

    from mfr.server.app import serve
    serve()

@task
def export_cache_clean(ctx, extension=''):
    cache_clean('export/', extension)

@task
def render_cache_clean(ctx, extension=''):
    cache_clean('render/', extension)

def cache_clean(folder, extension):
    # NOTE: Manually install gevent & pyrax, no need for it to be depenency just for this method.

    from gevent import monkey
    from gevent.pool import Pool
    from gevent import Timeout

    monkey.patch_all()

    import six
    import pyrax
    import logging
    from mfr.server import settings

    # Monkey patch pyrax for python 3 compatibility.
    def _add_details(self, info):
        """
        Takes the dict returned by the API call and sets the
        corresponding attributes on the object.
        """
        for (key, val) in six.iteritems(info):
            if six.PY2 and isinstance(key, six.text_type):
                key = key.encode(pyrax.get_encoding())
            elif isinstance(key, bytes):
                key = key.decode("utf-8")
            setattr(self, key, val)
    pyrax.resource.BaseResource._add_details = _add_details

    # WARNING: We are using provider specific functions to enumerate files to quickly
    # purge the cache, which can contain hundreds of thousands of objects. Thus
    # asserting the provider, we will need to update if we move providers.
    assert settings.CACHE_PROVIDER_NAME == 'cloudfiles'

    logging.captureWarnings(True)

    pyrax.set_setting('identity_type', 'rackspace')
    pyrax.set_setting('verify_ssl', True)
    pyrax.set_credentials(settings.CACHE_PROVIDER_CREDENTIALS['username'], settings.CACHE_PROVIDER_CREDENTIALS['token'])

    cf = pyrax.connect_to_cloudfiles(region=settings.CACHE_PROVIDER_CREDENTIALS['region'].upper(), public=True)
    container = cf.get_container(settings.CACHE_PROVIDER_SETTINGS['container'])

    def delete_object(obj):
        # added timeout of 5 seconds just in case
        with Timeout(5, False):
            try:
                print(obj)
                obj.delete()
            except Exception as ex:
                print(ex)

    pool = Pool(100)
    objects = container.get_objects(prefix=folder, limit=5000, marker='')
    while objects:
        for obj in objects:
            if obj.name.endswith(extension):
                pool.spawn(delete_object, obj)
        objects = container.get_objects(prefix=folder, limit=5000, marker=objects[-1].name)
    pool.join()

