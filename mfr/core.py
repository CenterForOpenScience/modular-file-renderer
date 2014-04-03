# -*- coding: utf-8 -*-
"""Core mfr functions and classes.
"""

#: Mapping of file handler names to classes
# TODO(sloria): Possible make this an OrderredDict so that detection is deterministic when
# two filehandlers can handle a file?
_registry = {}


def register_filehandler(name, file_handler):
    """Register a new file handler.
    Usage: ::

        register_filehandler('movie', MovieHandler)

    :param str name: The name of the filehandler.
    :param FileHandler file_handler: The filehandler class.
    """
    _registry[name] = file_handler


def detect(fp, handlers=None, *args, **kwargs):
    """Return a :class:`FileHandler <mfr.core.FileHandler>` for a given file.

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
            return handler
    return False


def render(fp, handler, renderer=None, *args, **kwargs):
    """Core rendering function. Return the rendered HTML for a given file.

    :param File fp: A file-like object to render.
    :param FileHandler: The file handler class to use.
    :param str renderer: The name of the renderer function to use (must be a key in
        in the handler class's `renderers` dictionary)
    """
    HandlerClass = _registry.get(handler)
    if not HandlerClass:
        raise ValueError('No available handler with name {handler}.'
                        .format(handler=handler))
    handler = HandlerClass()
    return handler.render(fp, renderer=renderer, *args, **kwargs)


class MFRException(Exception):
    """Base exception from which all MFR-related errors inherit."""
    pass


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


