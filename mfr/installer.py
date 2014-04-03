"""mfr: CLI for installing mfr modules.

Usage:
    mfr init
    mfr install [--exclude-static]

Options:
    -h --help       Show this screen.
    -d --debug      Use debug mode.
    install         Reads mfrconfig file and installs all necessary dependencies.

"""
import logging

from docopt import docopt

logger = logging.getLogger(__name__)


def parse_args():
    args = docopt(__doc__)
    return args


def install_module():
    # TODO(sloria)
    pass


def main():
    # TODO(sloria)
    args = parse_args()
    if args['--debug']:
        logging.basicConfig(
            format='%(levelname)s %(filename)s: %(message)s',
            level=logging.DEBUG)
    logger.debug(args)
    module = args['<module>']

if __name__ == '__main__':
    main()
