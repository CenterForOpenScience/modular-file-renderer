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
from collections import defaultdict

from mfr._config import Config
from mfr.exceptions import ConfigurationError

logger = logging.getLogger(__name__)

_defaults = {
    'INCLUDE_STATIC': False
}
#: Global mfr configuration object
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
    """Get the current list of registered filehandlers.

    :rtype: list
    """
    return config["HANDLERS"]


def clear_registry():
    """Reset the list of registered handlers."""
    config["HANDLERS"] = []


def reset_config():
    """Reset config defaults and empty the registry of file handlers."""
    global config
    config.clear()
    config.update(_defaults)
    config["HANDLERS"] = []


def detect(fp, handlers=None, instance=True, many=False, *args, **kwargs):
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
    if many:
        return valid_handlers
    else:
        return None


def render(fp, handler=None, renderer=None, *args, **kwargs):
    """Core rendering function. Return the rendered HTML for a given file.

    :param File fp: A file-like object to render.
    :param FileHandler: The file handler class to use.
    :param str renderer: The name of the renderer function to use (must be a key in
        in the handler class's `renderers` dictionary)
    """
    # Get the specified handler, detect it if not given
    handler = handler or detect(fp, many=False, instance=True)
    if not handler:
        raise ValueError('No available handler that can handle {name!r}.'
                        .format(name=fp.name))
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

def assets_by_extension(assets):
    """Given a list of assets, return a dictionary keyed by extension

    :param list assets: List of asset paths (strings)
    :rtype: dict
    """
    ret = defaultdict(list)
    for asset in assets:
        key = get_file_extension(asset).lstrip('.')
        ret[key].append(asset)
    return ret


class RenderResult(object):
    """ An object that contains the html representation of content and any
     assets that should be included.
    """

    def __init__(self, content, assets=None):
        """
        Initialize a Render result.

        :param content: html representation of content
        :param assets: css, javascript, or other assets to be included
        """
        self.content = content
        if isinstance(assets, (list, tuple)):
            self.assets = assets_by_extension(assets)
        elif isinstance(assets, dict):  # assets is a dict
            self.assets = defaultdict(list, assets)
        else:  # assets is None
            self.assets = defaultdict(list)

    def __str__(self):
        return str(self.content)

    def __repr__(self):
        return '<RenderResult({0!r})>'.format(self.content)

    def __contains__(self, obj):
        """Implements the ``in`` keyword."""
        return obj in str(self.content)

class FileHandler(object):
    """Abstract base class from which all file handlers must inherit.
    """
    #: Maps renderer names to renderer callables, e.g. {'html': render_img_html}
    renderers = {}
    #: Maps exporter names to exporter callables, e.g. {'png': export_png}
    exporters = {}

    default_renderer = 'html'
    default_exporter = None

    def __init__(self):
        self.__assets = defaultdict(list)

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

    def iterstatic(self, url=True):
        """Iterates through the static asset files for the filehandler,
        yielding absolute paths to the files.

        :param bool url: If ``True``, return the static url for each asset.
            If ``False``, return the static folder for each asset.
        """
        static_folder = get_static_path_for_handler(self.__class__)
        for root, dirs, files in os.walk(static_folder):
            for filename in files:
                absolute_path = os.path.join(root, filename)
                if url:
                    namespace = get_namespace(self)
                    static_path = os.path.relpath(absolute_path, static_folder)
                    try:
                        yield os.path.join(config['STATIC_URL'], namespace, static_path)
                    except KeyError:
                        raise KeyError('STATIC_URL is not configured.')
                else:
                    yield absolute_path

    def get_assets(self, extension=None):
        """Get the urls for this handler's static assets. Return either a dict
        keyed by extension or a list of assets if ``extension`` is provided.

        Usage: ::

            >>> handler.get_assets()
            {'css': '/static/myformat/style.css', 'js': '/static/myformat/script.js'}

        """
        if not self.__assets:
            for asset in self.iterstatic(url=True):
                ext = get_file_extension(asset).lstrip('.')
                if ext:
                    self.__assets[ext].append(asset)
                else:
                    self.__assets['_'].append(asset)
        if extension:
            return self.__assets[extension]
        return self.__assets

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

def get_static_url_for_handler(handler_cls):
    if hasattr(handler_cls, 'STATIC_URL'):
        url = os.path.join(config['STATIC_URL'], handler_cls.STATIC_URL)
    else:
        url = os.path.join(config['STATIC_URL'], get_namespace(handler_cls))
    return url


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
