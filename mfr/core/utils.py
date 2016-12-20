from stevedore import driver

from mfr import settings
from mfr.core import exceptions


def make_provider(name, request, url):
    """Returns an instance of :class:`mfr.core.provider.BaseProvider`

    :param str name: The name of the provider to instantiate. (osf)
    :param dict url:

    :rtype: :class:`mfr.core.provider.BaseProvider`
    """
    manager = driver.DriverManager(
        namespace='mfr.providers',
        name=name.lower(),
        invoke_on_load=True,
        invoke_args=(request, url, ),
    )
    return manager.driver


def make_exporter(name, source_file_path, output_file_path, format):
    """Returns an instance of :class:`mfr.core.extension.BaseExporter`

    :param str name: The name of the extension to instantiate. (.jpg, .docx, etc)
    :param str source_file_path:
    :param str output_file_path:
    :param str format:

    :rtype: :class:`mfr.core.extension.BaseExporter`
    """
    try:
        return driver.DriverManager(
            namespace='mfr.exporters',
            name=(name and name.lower()) or 'none',
            invoke_on_load=True,
            invoke_args=(source_file_path, output_file_path, format),
        ).driver
    except RuntimeError:
        keen_data = {'DriverArgs':
                        {'namespace': 'mfr.renderers',
                         'name': (name and name.lower()) or 'none',
                         'invoke_on_load': True,
                         'invoke_args':
                             {'source_file_path': source_file_path,
                              'output_file_path': output_file_path,
                              'format': format}
                         }
                     }
        raise exceptions.MakeExporterError(settings.UNSUPPORTED_EXPORTER_MSG,
                                       code=400, keen_data=keen_data)


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
    try:
        return driver.DriverManager(
            namespace='mfr.renderers',
            name=(name and name.lower()) or 'none',
            invoke_on_load=True,
            invoke_args=(metadata, file_path, url, assets_url, export_url),
        ).driver
    except RuntimeError:
        keen_data = {'DriverArgs':
                        {'namespace': 'mfr.renderers',
                         'name': (name and name.lower()) or 'none',
                         'invoke_on_load': True,
                         'invoke_args':
                            {'metadata': metadata.serialize(),
                             'file_path': file_path,
                             'url': url,
                             'assets_url': assets_url,
                             'export_url': export_url}
                         }
                     }
        raise exceptions.MakeRendererError(settings.UNSUPPORTED_RENDER_MSG,
                                       code=400, keen_data=keen_data)
