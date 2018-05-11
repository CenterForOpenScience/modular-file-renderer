import pkg_resources
from stevedore import driver

from mfr.core import exceptions


def make_provider(name, request, url):
    """Returns an instance of :class:`mfr.core.provider.BaseProvider`

    :param str name: The name of the provider to instantiate. (osf)
    :param request:
    :param dict url:

    :rtype: :class:`mfr.core.provider.BaseProvider`
    """
    try:
        return driver.DriverManager(
            namespace='mfr.providers',
            name=name.lower(),
            invoke_on_load=True,
            invoke_args=(request, url)
        ).driver
    except RuntimeError:
        raise exceptions.MakeProviderError(
            '"{}" is not a supported provider'.format(name.lower()),
            namespace='mfr.providers',
            name=name.lower(),
            invoke_on_load=True,
            invoke_args={
                'request': request,
                'url': url,
            }
        )


def bind_render(metadata, file_stream, url, assets_url, export_url):
    normalized_name = (metadata.ext and metadata.ext.lower()) or 'none'
    try:
        return driver.DriverManager(
            namespace='mfr.renderers',
            name=normalized_name,
            invoke_on_load=True,
            invoke_args=(metadata, file_stream, url, assets_url, export_url),
        ).driver
    except RuntimeError:
        raise exceptions.MakeRendererError(
            namespace='mfr.renderers',
            name=normalized_name,
            invoke_on_load=True,
            invoke_args={
                'metadata': metadata.serialize(),
                'file_stream': file_stream,
                'url': url,
                'assets_url': assets_url,
                'export_url': export_url,
            }
        )

def bind_convert(metadata, file_stream, format):
    normalized_name = (metadata.ext and metadata.ext.lower()) or 'none'
    try:
        return driver.DriverManager(
            namespace='mfr.exporters',
            name=normalized_name,
            invoke_on_load=True,
            invoke_args=(metadata, file_stream, format)
        ).driver
    except RuntimeError:
        raise exceptions.MakeExporterError(
            namespace='mfr.exporters',
            name=normalized_name,
            invoke_on_load=True,
            invoke_args={
                'metadata': metadata.serialize(),
                'input_stream': file_stream,
                'format': format,
            }
        )


def get_plugin_name(name: str, group: str) -> str:
    """ Return the name of the renderer used for a certain file extension.

    :param str name: The name of the extension to get the renderer name for. (.jpg, .docx, etc)

    :rtype : `str`
    """

    # `ep_iterator` is an iterable object. Must convert it to a `list` for access.
    # `list()` can only be called once because the iterator moves to the end after conversion.
    ep_iterator = pkg_resources.iter_entry_points(group=group, name=name.lower())
    ep_list = list(ep_iterator)

    # Empty list indicates unsupported file type.  Return '' and let `make_renderer()` handle it.
    if len(ep_list) == 0:
        return ''

    # If the file type is supported, there must be only one element in the list.
    assert len(ep_list) == 1
    return ep_list[0].attrs[0]

def sizeof_fmt(num, suffix='B'):
    if abs(num) < 1000:
        return '%3.0f%s' % (num, suffix)

    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1000.0:
            return '%3.1f%s%s' % (num, unit, suffix)
        num /= 1000.0
    return '%.1f%s%s' % (num, 'Y', suffix)
