from time import time
from os.path import getctime

from stevedore import driver

from mfr.core import exceptions
from mfr.extensions import settings as ext_settings


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
            invoke_args=(request, url, ),
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


def make_exporter(name, source_file_path, output_file_path, format):
    """Returns an instance of :class:`mfr.core.extension.BaseExporter`

    :param str name: The name of the extension to instantiate. (.jpg, .docx, etc)
    :param str source_file_path:
    :param str output_file_path:
    :param str format:

    :rtype: :class:`mfr.core.extension.BaseExporter`
    """
    normalized_name = (name and name.lower()) or 'none'
    try:
        return driver.DriverManager(
            namespace='mfr.exporters',
            name=normalized_name,
            invoke_on_load=True,
            invoke_args=(normalized_name, source_file_path, output_file_path, format),
        ).driver
    except RuntimeError:
        raise exceptions.MakeExporterError(
            namespace='mfr.exporters',
            name=normalized_name,
            invoke_on_load=True,
            invoke_args={
                'source_file_path': source_file_path,
                'output_file_path': output_file_path,
                'format': format,
            }
        )


def make_renderer(name, metadata, file_path, url, assets_url, export_url):
    """Returns an instance of :class:`mfr.core.extension.BaseRenderer`

    :param str name: The name of the extension to instantiate. (.jpg, .docx, etc)
    :param: :class:`mfr.core.provider.ProviderMetadata` metadata:
    :param str file_path:
    :param str url:
    :param str assets_url:
    :param str export_url:

    :rtype: :class:`mfr.core.extension.BaseRenderer`
    """
    normalized_name = (name and name.lower()) or 'none'
    try:
        return driver.DriverManager(
            namespace='mfr.renderers',
            name=normalized_name,
            invoke_on_load=True,
            invoke_args=(metadata, file_path, url, assets_url, export_url),
        ).driver
    except RuntimeError:
        raise exceptions.MakeRendererError(
            namespace='mfr.renderers',
            name=normalized_name,
            invoke_on_load=True,
            invoke_args={
                'metadata': metadata.serialize(),
                'file_path': file_path,
                'url': url,
                'assets_url': assets_url,
                'export_url': export_url,
            }
        )


def sizeof_fmt(num, suffix='B'):
    if abs(num) < 1000:
        return '%3.0f%s' % (num, suffix)

    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1000.0:
            return '%3.1f%s%s' % (num, unit, suffix)
        num /= 1000.0
    return '%.1f%s%s' % (num, 'Y', suffix)


def file_expired(path: str, ttl: int) -> bool:
    """Helper method that checks if a file's last change time has expired ttl.

    :param path: the path of the file
    :param ttl: the expiration time in seconds
    :return: True if expired, False otherwise
    """

    if (time() - getctime(path)) >= ttl:
        return True
    return False


def get_full_file_ext(metadata_ext: str, metadata_name: str) -> str:
    """Helper method that checks if a secondary extension exists for a file
    with a compressed extension as primary. If so, returns the full extension.

    :param metadata_ext: the file's primary extension
    :param metadata_name: the file name that may contain a secondary extension
    :return: the file's full extension
    """

    compressed_ext = ext_settings.COMPRESSED_EXT
    if metadata_ext in compressed_ext.keys():
        secondary_ext = '.{}'.format(metadata_name.split('.')[-1])
        if secondary_ext in compressed_ext[metadata_ext]:
            return secondary_ext + metadata_ext
    return metadata_ext
