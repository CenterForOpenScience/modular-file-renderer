"""mfr: CLI for installing mfr modules.

Usage:
    mfr init [-d]
    mfr install <module>... [--exclude-static] [-d]

Options:
    -h --help       Show this screen.
    -d --debug      Use debug mode.
    install         Reads mfrconfig file and installs all necessary dependencies.

"""
import os
import os.path.join as pjoin
import logging

import pip
from docopt import docopt

import mfr

logger = logging.getLogger(__name__)
debug = logger.debug

def parse_args():
    args = docopt(__doc__)
    return args

def find_requirements_files(dir):
    # TODO(sloria)
    pass

def install_module(module_name):
    # TODO(sloria)
    debug('Installing {0!r}'.format(module_name))
    module_dir = pjoin(mfr.PACKAGE_DIR, module_name)
    req_files = find_requirements_files(module_dir)


def main():
    # TODO(sloria)
    args = parse_args()
    if args['--debug']:
        logging.basicConfig(
            format='%(levelname)s %(filename)s: %(message)s',
            level=logging.DEBUG)
    logger.debug(args)
    modules_to_install = args['<module>']
    for module_name in modules_to_install:
        install_module(module_name)



if __name__ == '__main__':
    main()
