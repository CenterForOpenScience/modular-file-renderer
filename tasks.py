import os

from invoke import task, run

WHEELHOUSE_PATH = os.environ.get('WHEELHOUSE')


@task
def wheelhouse(develop=False):
    req_file = 'dev-requirements.txt' if develop else 'requirements.txt'
    cmd = 'pip wheel --find-links={} -r {} --wheel-dir={}'.format(WHEELHOUSE_PATH, req_file, WHEELHOUSE_PATH)
    run(cmd, pty=True)


@task
def install(develop=False):
    run('python setup.py develop')
    req_file = 'dev-requirements.txt' if develop else 'requirements.txt'
    cmd = 'pip install --upgrade -r {}'.format(req_file)

    if WHEELHOUSE_PATH:
        cmd += ' --no-index --find-links={}'.format(WHEELHOUSE_PATH)
    run(cmd, pty=True)


@task
def flake():
    run('flake8 .', pty=True)


@task
def test(verbose=False):
    flake()
    cmd = 'py.test --cov-report term-missing --cov mfr tests'
    if verbose:
        cmd += ' -v'
    run(cmd, pty=True)


@task
def server():
    from mfr.server.app import serve
    serve()
