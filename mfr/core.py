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

from mfr._config import Config
from mfr.exceptions import ConfigurationError

logger = logging.getLogger(__name__)

#: Current mfr configuration object
_defaults = {
    'INCLUDE_STATIC': False
}
config = Config(defaults=_defaults)

config['HANDLERS'] = []


def register_filehandler(file_handler):
    """Register a new file handler.
    Usage: ::

        register_filehandler(MovieHandler)

    :param FileHandler file_handler: The filehandler class.
    """
    get_registry().append(file_handler)


def register_filehandlers(handlers):
    """Register multiple file handlers.
    Usage: ::

        register_file_handlers({'image': ImageFileHandler, 'movie': MovieHandler})

    :param dict handler_dict: A dictionary mapping handler names to handler classes
    """
    get_registry().extend(handlers)


def get_registry():
    return config['HANDLERS']


def clear_registry():
    config['HANDLERS'] = []


def reset_config():
    global config
    config = Config(defaults=_defaults)
    config['HANDLERS'] = []


def detect(fp, handlers=None, instance=False, many=True, *args, **kwargs):
    """Return a :class:`FileHandler <mfr.core.FileHandler>` for a given file,
    or ``False`` if no handler could be found for the file.

    :param list handlers: A list of filehandler names to try. If ``None``,
        try all registered handlers.
    :return: A FileHandler that can handle the file, or False if no handler was
        found.
    """
    handlers = handlers or get_registry()
    valid_handlers = []
    for HandlerClass in handlers:
        handler = HandlerClass()
        if handler.detect(fp, *args, **kwargs):
            handler_obj = handler if instance else HandlerClass
            if many:
                valid_handlers.append(handler_obj)
            else:
                return handler_obj
    return valid_handlers


def render(fp, handler=None, renderer=None, *args, **kwargs):
    """Core rendering function. Return the rendered HTML for a given file.

    :param File fp: A file-like object to render.
    :param FileHandler: The file handler class to use.
    :param str renderer: The name of the renderer function to use (must be a key in
        in the handler class's `renderers` dictionary)
    """
    # Get the specified handler, detect it if not given
    HandlerClass = handler or detect(fp, many=False)
    if not HandlerClass:
        raise ValueError('No available handler that can handle {name!r}.'
                        .format(name=fp.name))
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
    HandlerClass = handler or detect(fp)
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
    """Return the absolute path for a given FileHandler class.
    Defaults to a ``static`` folder within the same directory of the handler's
    module.
    """
    # If STATIC_PATH is defined, use that
    if hasattr(handler_cls, 'STATIC_PATH'):
        static_path = handler_cls.STATIC_PATH
    # Otherwise assume 'static' dir is in the same directory as
    # the handler class's module
    else:
        static_path = os.path.join(_get_dir_for_class(handler_cls), 'static')
    return static_path


def copy_dir(src, dest):
    """Recursively copies a directory's contents."""
    try:
        shutil.copytree(src, dest)
    except shutil.Error as err:
        logger.warn(err)
    except OSError as err:
        logger.debug('Skipping {src} (already exists)'.format(src=src))


def get_namespace(handler_cls):
    """Given a FileHandler class, return the namespace used by collect_static.
    The namespace defines the name of the folder that a file module's static
    assets will be copied to.
    """
    # If 'namespace' is defined on the class, use that
    if hasattr(handler_cls, 'namespace'):
        return handler_cls.namespace
    # Otherwise use the base name of the module
    else:
        # mypackage.mymodule.MyHandler => 'mymodule'
        return handler_cls.__module__.split('.')[-1]


def collect_static(dest=None, dry_run=False):
    """Collect all static assets for registered handlers to a single directory.
    Files will be copied to ``dest``, if specified, or the STATIC_PATH config
    variable.
    """
    dest_ = dest or config.get('STATIC_FOLDER')
    if not dest_:
        raise ConfigurationError('STATIC_FOLDER has not been configured.')
    for handler_cls in get_registry():
        static_path = get_static_path_for_handler(handler_cls)
        namespaced_destination = os.path.join(dest_, get_namespace(handler_cls))
        if dry_run:
            print('Pretending to copy {static_path} to {namespaced_destination}.'
                .format(**locals()))
        else:
            copy_dir(static_path, namespaced_destination)
