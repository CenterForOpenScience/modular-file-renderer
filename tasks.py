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
def test(ctx, verbose=False, nocov=False, extension=None, path=None):
    """Run full or customized tests for MFR.
    :param ctx: the ``invoke`` context
    :param verbose: the flag to increase verbosity
    :param nocov: the flag to disable coverage
    :param extension: limit the tests to the given extension only
    :param path: limit the tests to the given path only
    :return: None
    """
    flake(ctx)
    # `--extension=` and `--path=` are mutually exclusive options
    assert not (extension and path)
    if path:
        path = '/{}'.format(path) if path else ''
    elif extension:
        path = '/extensions/{}/'.format(extension) if extension else ''
    else:
        path = ''
    coverage = ' --cov-report term-missing --cov mfr' if not nocov else ''
    verbose = '-v' if verbose else ''
    cmd = 'py.test{} tests{} {}'.format(coverage, path, verbose)
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
