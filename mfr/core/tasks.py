import os
import codecs
import logging

CUSTOM_ERROR_MESSAGES = {}

# Unable to render. Download the file to view it.
def render_mfr_error(err):
    pre = ERROR_PREFIX
    msg = CUSTOM_ERROR_MESSAGES.get(type(err), err.message)
    return u"""
           <div class="osf-mfr-error">
           <p>{pre}</p>
           <p>{msg}</p>
           </div>
        """.format(**locals())


# TODO only allow one task at a time

def _build_rendered_html(download_url, cache_path, temp_path, public_download_url):
    """
    :param str download_url: The url to download the file to be rendered
    :param str cache_path: Location to cache the rendered file
    :param str temp_path: Where the downloaded file will be cached
    """

    if render_is_done_or_happening(cache_path, temp_path):
        return

    # Ensure our paths exists
    # Note: Ensures that cache directories have the same owner
    # as the files inside them
    ensure_path(os.path.split(temp_path)[0])
    ensure_path(os.path.split(cache_path)[0])

    rendered = None
    try:
        save_to_file_or_error(download_url, temp_path)
    except exceptions.RenderNotPossibleException as e:
        # Write out unavoidable errors
        rendered = e.renderable_error
    else:
        encoding = None
        # Workaround for https://github.com/CenterForOpenScience/osf.io/issues/2389
        # Open text files as utf-8
        # Don't specify an encoding for other filetypes. Otherwise filetypes
        # such as docx will break
        if get_file_extension(temp_path) in CODE_EXTENSIONS:
            encoding = 'utf-8'
        with codecs.open(temp_path, encoding=encoding) as temp_file:
            try:
                render_result = mfr.render(temp_file, src=public_download_url)
                # Rendered result
                rendered = _build_html(render_result)
            except MFRError as err:
                # Rendered MFR error
                rendered = render_mfr_error(err)

    # Cache rendered content
    with codecs.open(cache_path, 'w', 'utf-8') as render_result_cache:
        render_result_cache.write(rendered)

    # Cleanup when we're done
    os.remove(temp_path)



def old_build_rendered_html(file_path, cache_dir, cache_file_name, download_url):
    """
    :param str file_path: Full path to raw file on disk
    :param str cache_dir: Folder to store cached file in
    :param str cache_file_name: Name of cached file
    :param str download_url: External download URL
    """
    with codecs.open(file_path) as file_pointer:

        # Build path to cached content
        # Note: Ensures that cache directories have the same owner as the files
        # inside them
        ensure_path(cache_dir)
        cache_file_path = os.path.join(cache_dir, cache_file_name)

        with codecs.open(cache_file_path, 'w', 'utf-8') as write_file_pointer:
            # Render file
            try:
                render_result = mfr.render(file_pointer, src=download_url)
            except MFRError as err:
                rendered = render_mfr_error(err).format(download_path=download_url)
            else:
                rendered = _build_html(render_result)

            # Cache rendered content
            write_file_pointer.write(rendered)

    os.remove(file_path)
    return True


def _build_css_asset(css_uri):
    """Wrap a css asset so it can be included on an html page"""
    return '<link rel="stylesheet" href="{uri}" />'.format(uri=css_uri)


def _build_js_asset(js_uri):
    """Wrap a js asset so it can be included on an html page"""
    return '<script src="{uri}"></script>'.format(uri=js_uri)


def build_html(render_result, assets):
    """Build all of the assets and content into an html page"""
    if assets:
        css_list = assets.get('css') or []
        css_assets = u'\n'.join(
            [_build_css_asset(css_uri) for css_uri in css_list]
        )

        js_list = assets.get('js') or []
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