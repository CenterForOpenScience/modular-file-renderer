from importlib.metadata import entry_points

from stevedore import driver

from mfr.core import exceptions


def make_provider(name, request, url, action=None):
    """Returns an instance of :class:`mfr.core.provider.BaseProvider`

    :param str name: The name of the provider to instantiate. (osf)
    :param request:
    :param dict url:
    :param action:

    :rtype: :class:`mfr.core.provider.BaseProvider`
    """
    try:
        return driver.DriverManager(
            namespace="mfr.providers",
            name=name.lower(),
            invoke_on_load=True,
            invoke_args=(
                request,
                url,
            ),
            invoke_kwds={"action": action},
        ).driver
    except RuntimeError:
        raise exceptions.MakeProviderError(
            f'"{name.lower()}" is not a supported provider',
            namespace="mfr.providers",
            name=name.lower(),
            invoke_on_load=True,
            invoke_args={
                "request": request,
                "url": url,
            },
        )


def fix_name(name: str):
    name = name.removeprefix(".").replace("+", "p")
    if name == "lasso[89]":
        return "lasso"
    elif name == "php[345]":
        return "php"
    elif name == "css.in":
        return "css"
    elif name == "js.in":
        return "js"
    elif name == "xul.in":
        return "xul"
    return name


def make_exporter(name, source_file_path, output_file_path, file_format, metadata):
    """Returns an instance of :class:`mfr.core.extension.BaseExporter`

    :param str name: The name of the extension to instantiate. (.jpg, .docx, etc)
    :param str source_file_path:
    :param str output_file_path:
    :param str file_format:
    :param metadata:

    :rtype: :class:`mfr.core.extension.BaseExporter`
    """
    normalized_name = fix_name(name and name.lower()) or "none"

    try:
        return driver.DriverManager(
            namespace="mfr.exporters",
            name=normalized_name,
            invoke_on_load=True,
            invoke_args=(
                normalized_name,
                source_file_path,
                output_file_path,
                file_format,
                metadata,
            ),
        ).driver
    except RuntimeError:
        raise exceptions.MakeExporterError(
            namespace="mfr.exporters",
            name=normalized_name,
            invoke_on_load=True,
            invoke_args={
                "source_file_path": source_file_path,
                "output_file_path": output_file_path,
                "format": file_format,
            },
        )


def make_renderer(name, metadata, file_path, url, assets_url, export_url):
    """Returns an instance of :class:`mfr.core.extension.BaseRenderer`

    :param str name: The name of the extension to instantiate. (.jpg, .docx, etc)
    :param: :class:`mfr.core.provider.ProviderMetadata` metadata:
    :param metadata:
    :param str file_path:
    :param str url:
    :param str assets_url:
    :param str export_url:

    :rtype: :class:`mfr.core.extension.BaseRenderer`
    """
    normalized_name = fix_name(name and name.lower()) or "none"
    try:
        return driver.DriverManager(
            namespace="mfr.renderers",
            name=normalized_name,
            invoke_on_load=True,
            invoke_args=(metadata, file_path, url, assets_url, export_url),
        ).driver
    except RuntimeError:
        raise exceptions.MakeRendererError(
            namespace="mfr.renderers",
            name=normalized_name,
            invoke_on_load=True,
            invoke_args={
                "metadata": metadata.serialize(),
                "file_path": file_path,
                "url": url,
                "assets_url": assets_url,
                "export_url": export_url,
            },
        )


def get_renderer_name(name: str) -> str:
    """Return the name of the renderer used for a certain file extension.

    :param str name: The name of the extension to get the renderer name for. (.jpg, .docx, etc)

    :rtype : `str`
    """

    # `ep_iterator` is an iterable object. Must convert it to a `list` for access.
    # `list()` can only be called once because the iterator moves to the end after conversion.
    ep = entry_points().select(group="mfr.renderers", name=name.lower())
    ep_list = list(ep)

    # Empty list indicates unsupported file type.  Return '' and let `make_renderer()` handle it.
    if len(ep_list) == 0:
        return ""

    # If the file type is supported, there must be only one element in the list.
    assert len(ep_list) == 1
    return ep_list[0].value.split(":")[-1]


def get_exporter_name(name: str) -> str:
    """Return the name of the exporter used for a certain file extension.

    :param str name: The name of the extension to get the exporter name for. (.jpg, .docx, etc)

    :rtype : `str`
    """

    # `ep_iterator` is an iterable object. Must convert it to a `list` for access.
    # `list()` can only be called once because the iterator moves to the end after conversion.
    ep = entry_points().select(group="mfr.exporters", name=name.lower())
    ep_list = list(ep)

    # Empty list indicates unsupported export type.  Return '' and let `make_exporter()` handle it.
    if len(ep_list) == 0:
        return ""

    # If the export type is supported, there must be only one element in the list.
    assert len(ep_list) == 1
    return ep_list[0].value.split(":")[-1]


def sizeof_fmt(num, suffix="B"):
    if abs(num) < 1000:
        return "{:3.0f}{}".format(num, suffix)

    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1000.0:
            return "{:3.1f}{}{}".format(num, unit, suffix)
        num /= 1000.0
    return "{:.1f}{}{}".format(num, "Y", suffix)
