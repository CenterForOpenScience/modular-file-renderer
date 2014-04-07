# -*- coding: utf-8 -*-
import os
import sys

from invoke import task, run

docs_dir = 'docs'
build_dir = os.path.join(docs_dir, '_build')

@task
def previewer():
    """Run the previewer app."""
    from previewer.main import app
    app.run(debug=True)


@task
def test():
    run('python setup.py test', pty=True)

@task
def clean():
    run("rm -rf build")
    run("rm -rf dist")
    run("rm -rf mfr.egg-info")
    clean_docs()
    print("Cleaned up.")

@task
def clean_docs():
    run("rm -rf %s" % build_dir)

@task
def browse_docs():
    run("open %s" % os.path.join(build_dir, 'index.html'))

@task
def docs(clean=False, browse=False):
    if clean:
        clean_docs()
    run("sphinx-build %s %s" % (docs_dir, build_dir), pty=True)
    if browse:
        browse_docs()

@task
def readme(browse=False):
    run('rst2html.py README.rst > README.html')

@task
def publish(test=False):
    """Publish to the cheeseshop."""
    try:
        __import__('wheel')
    except ImportError:
        print("wheel required. Run `pip install wheel`.")
        sys.exit(1)
    if test:
        run('python setup.py register -r test sdist bdist_wheel upload -r test')
    else:
        run("python setup.py register sdist bdist_wheel upload")
