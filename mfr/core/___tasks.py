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
