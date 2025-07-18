import os

from invoke import task

WHEELHOUSE_PATH = os.environ.get('WHEELHOUSE')


@task
def wheelhouse(ctx, develop=False, pty=True):
    extras = '--with dev' if develop else ''
    cmd = f'poetry export --format=requirements.txt {extras} | pip wheel --find-links={WHEELHOUSE_PATH} -r /dev/stdin --wheel-dir={WHEELHOUSE_PATH}'
    ctx.run(cmd, pty=pty)


@task
def install(ctx, develop=False, pty=True):
    extras = '--with dev' if develop else ''
    ctx.run(f'poetry install {extras}', pty=pty)


@task
def flake(ctx):
    ctx.run('poetry run flake8 .', pty=True)


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
        path = f'/{path}' if path else ''
    elif extension:
        path = f'/extensions/{extension}/' if extension else ''
    else:
        path = ''
    coverage = ' --cov-report term-missing --cov mfr' if not nocov else ''
    verbose = '-v' if verbose else ''
    cmd = f'poetry run pytest{coverage} tests{path} {verbose}'
    ctx.run(cmd, pty=True)


@task
def server(ctx):
    if os.environ.get('REMOTE_DEBUG', None):
        import pydevd
        # e.g. '127.0.0.1:5678'
        remote_parts = os.environ.get('REMOTE_DEBUG').split(':')
        pydevd.settrace(remote_parts[0], port=int(remote_parts[1]), suspend=False, stdoutToServer=True, stderrToServer=True)

    from mfr.server.app import serve
    serve()

@task
def celery(ctx, loglevel='INFO', hostname='%h'):
    from mfr.tasks.app import app
    command = ['worker']
    if loglevel:
        command.extend(['--loglevel', loglevel])
    if hostname:
        command.extend(['--hostname', hostname])
    app.worker_main(command)

