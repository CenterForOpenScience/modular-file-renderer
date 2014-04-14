"""Libreoffice renderer ."""
import os
import tempfile
import subprocess
import shutil
from flask import Response

LIBREOFFICE_BIN = os.path.expanduser(os.environ.get("LIBREOFFICE_BIN", "soffice"))
# These formats can't be easily exported to html so we export them to PDF instead
EXPORT_PDF_FORMATS = ('.ppt', '.pptx', '.odp', '.csv', '.xls', '.xlsx', '.ods')

def render(fp, src=None):
    """A simple libreoffice html documents converter.

    :param str:
    """
    
    out = ''
    tmpdir = tempfile.mkdtemp()    
    src = fp.name
    base_filename, extension = os.path.splitext(os.path.basename(src))
    mimetype = "text/html"
    
    try:
        if extension in EXPORT_PDF_FORMATS: # Convert to pdf files
            p = subprocess.call([LIBREOFFICE_BIN, "--headless", "--convert-to", "pdf", "--outdir", tmpdir, src])
            if p == 0: # success
                out = open(os.path.join(tmpdir, base_filename + '.pdf'), "rb").read()
                mimetype = "application/pdf"
        else: # convert the rest ot HTML
            p = subprocess.call([LIBREOFFICE_BIN, "--headless", "--convert-to", "html:HTML", "--outdir", tmpdir, src])
            if p == 0: # success
                out = open(os.path.join(tmpdir, base_filename + '.html'), "rb").read()
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            raise ValueError("Libreoffice `soffice` binary file not found. Please set LIBREOFFICE_BIN environment variable.")
        else:
            # Something else went wrong while trying to run `wget`
            raise
    finally:
        # clean temporary directory
        shutil.rmtree(tmpdir)
        
    return Response(out, mimetype=mimetype)
