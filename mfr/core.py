# -*- coding: utf-8 -*-
"""Core functions and classes.

Basic Usage: ::

    from mfr.core import detect

    with open('myfile.jpg', 'r') as fp:
        handler = detect(fp)
        if handler:
            html = handler.render(fp)
"""
import os
import shutil
import inspect
import logging

from mfr.config import Config
from mfr.exceptions import ConfigurationError

logger = logging.getLogger(__name__)

#: Mapping of file handler names to classes
# {'tabular': TabularFileHandler}
# TODO(sloria): Possible make this an OrderredDict so that detection is deterministic when
# two filehandlers can handle a file?
_registry = {}

#: Current mfr configuration object
config = Config()


def register_filehandler(name, file_handler):
    """Register a new file handler.
    Usage: ::

        register_filehandler('movie', MovieHandler)

    :param str name: The name of the filehandler.
    :param FileHandler file_handler: The filehandler class.
    """
    _registry[name] = file_handler


def detect(fp, handlers=None, instance=False, *args, **kwargs):
    """Return a :class:`FileHandler <mfr.core.FileHandler>` for a given file,
    or ``False`` if no handler could be found for the file.

    :param list handlers: A list of filehandler names to try. If ``None``,
        try all registered handlers.
    :return: A FileHandler that can handle the file, or False if no handler was
        found.
    """
    handlers = handlers or _registry.keys()
    for handler_name in handlers:
        HandlerClass = _registry.get(handler_name)
        handler = HandlerClass()
        if handler.detect(fp, *args, **kwargs):
            return handler if instance else HandlerClass
    return False


def render(fp, handler=None, renderer=None, *args, **kwargs):
    """Core rendering function. Return the rendered HTML for a given file.

    :param File fp: A file-like object to render.
    :param FileHandler: The file handler class to use.
    :param str renderer: The name of the renderer function to use (must be a key in
        in the handler class's `renderers` dictionary)
    """
    # Get the specified handler, detect it if not given
    HandlerClass = _registry.get(handler) or detect(fp)
    if not HandlerClass:
        raise ValueError('No available handler with name {handler}.'
                        .format(handler=handler))
    handler = HandlerClass()
    return handler.render(fp, renderer=renderer, *args, **kwargs)


def export(fp, handler=None, exporter=None, *args, **kwargs):
    """Core rendering function. Return the rendered HTML for a given file.

    :param File fp: A file-like object to render.
    :param FileHandler: The file handler class to use.
    :param str renderer: The name of the renderer function to use (must be a key in
        in the handler class's `renderers` dictionary)
    """
    # Get the specified handler, detect it if not given
    HandlerClass = _registry.get(handler) or detect(fp)
    if not HandlerClass:
        raise ValueError('No available handler with name {handler}.'
                        .format(handler=handler))
    handler = HandlerClass()
    return handler.export(fp, exporter=exporter, *args, **kwargs)


def get_file_extension(path, lower=True):
    """Get the file extension for a given file path."""
    ext = os.path.splitext(path)[1]
    return ext.lower() if lower else ext


def get_file_exporters(handler):
    try:
        return handler.exporters.keys()
    except AttributeError:
        return None


class FileHandler(object):
    """Abstract base class from which all file handlers must inherit.
    """
    #: Maps renderer names to renderer callables, e.g. {'html': render_img_html}
    renderers = {}
    #: Maps exporter names to exporter callables, e.g. {'png': export_png}
    exporters = {}

    default_renderer = 'html'
    default_exporter = None

    def detect(self, fp):
        """Return whether a given file can be handled by this file handler.
        MUST be implemented by descendant classes.
        """
        raise NotImplementedError('Must define detect method.')

    def render(self, fp, renderer=None, *args, **kwargs):
        """Return the rendered HTML for a file.

        :param fp: A file-like object.
        :param str renderer: The name of the renderer to use. If `None`,
            the default_renderer is used.
        """
        render_func = self.renderers.get(renderer or self.default_renderer)
        # TODO(sloria): check if render_func is callable
        if render_func:
            return render_func(fp, *args, **kwargs)
        else:
            raise ValueError('`render` method called with no renderer specified and '
                            'no default.')

    def export(self, fp, exporter=None, *args, **kwargs):
        """Export a file to a different format.

        :param str exporter: The name of the exporter to use. If `None`,
            the default_exporter is used.
        """
        export_func = self.exporters.get(exporter or self.default_exporter)
        if export_func:
            return export_func(fp, *args, **kwargs)
        else:
            raise ValueError('`export` method called with no exporter specified and '
                            'no default.')

def _get_dir_for_class(cls):
    """Return the absolute directory where a class resides."""
    fpath = inspect.getfile(cls)
    return os.path.abspath(os.path.dirname(fpath))

def get_static_path_for_handler(handler_cls):
    # If STATIC_PATH is defined, use that
    if hasattr(handler_cls, 'STATIC_PATH'):
        static_path = handler_cls.STATIC_PATH
    # Otherwise assume 'static' dir is in the same directory as
    # the handler class's module
    else:
        static_path = os.path.join(_get_dir_for_class(handler_cls), 'static')
    return static_path

def copy_dir(src, dest):
    try:
        shutil.copytree(src, dest)
    except shutil.Error as err:
        logger.warn(err)
    except OSError as err:
        logger.warn(err)

def collect_static(dest=None, dry_run=False):
    dest = dest or config.get('STATIC_PATH')
    if not dest:
        raise ConfigurationError('STATIC_PATH has not been configured.')
    for name, handler_cls in _registry.items():
        static_path = get_static_path_for_handler(handler_cls)
        namespaced_destination = os.path.join(dest, name)
        if dry_run:
            print('Pretending to copy {static_path} to {namespaced_destination}.'
                .format(**locals()))
        else:
            copy_dir(static_path, namespaced_destination)
