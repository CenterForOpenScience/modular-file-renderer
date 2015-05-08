def _build_css_asset(css_uri):
    """Wrap a css asset so it can be included on an html page"""
    return '<link rel="stylesheet" href="{uri}" />'.format(uri=css_uri)


def _build_js_asset(js_uri):
    """Wrap a js asset so it can be included on an html page"""
    return '<script src="{uri}"></script>'.format(uri=js_uri)


def build_html(render_result):
    """Build all of the assets and content into an html page"""
    if render_result.assets:
        css_list = render_result.assets.get('css') or []
        css_assets = u'\n'.join(
            [_build_css_asset(css_uri) for css_uri in css_list]
        )

        js_list = render_result.assets.get('js') or []
        js_assets = u'\n'.join(
            [_build_js_asset(js_uri) for js_uri in js_list]
        )
    else:
        css_assets = js_assets = ""

    return u'{css}\n\n{js}\n\n{content}'.format(
        css=css_assets,
        js=js_assets,
        content=render_result.content or '',
    )


def ensure_path(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise