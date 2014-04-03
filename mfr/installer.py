"""mfr: CLI for installing mfr modules.

Usage:
    mfrinstall <module> [-d]
    mfrinstall <module> [--render-only | --export-only] [-d]

Options:
    -h --help       Show this screen.
    -d --debug      Use debug mode.

"""
import logging

from docopt import docopt

logger = logging.getLogger(__name__)


def parse_args():
    args = docopt(__doc__)
    return args


def install_module(render_only=False, export_only=False):
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
    install_module(module=module,
        render_only=args['--render-only'],
        export_only=args['--export-only'])


if __name__ == '__main__':
    main()
