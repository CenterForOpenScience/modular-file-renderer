# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1405664055.049842
_enable_loop = True
_template_filename = '/home/pfan/modular-file-renderer/mfr_ipynb/templates/ipynb.mako'
_template_uri = '/home/pfan/modular-file-renderer/mfr_ipynb/templates/ipynb.mako'
_source_encoding = 'ascii'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        body = context.get('body', UNDEFINED)
        STATIC_PATH = context.get('STATIC_PATH', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'<link href="')
        __M_writer(unicode(STATIC_PATH))
        __M_writer(u'/ipynb/css/pygments.css" rel="stylesheet">\n')
        __M_writer(u'\n<style type="text/css">\n    .imgwrap {\n        text-align: center;\n    }\n    .input_area {\n        padding: 0.4em;\n    }\n    div.input_area > div.highlight > pre {\n        margin: 0px;\n        padding: 0px;\n        border: none;\n    }\n\n</style>\n<div class="mfr-ipynb-body">\n')
        __M_writer( body )
        __M_writer(u'\n</div>\n<script type="text/javascript">\n    (function() {\n    if (window.MathJax) {\n        // MathJax loaded\n        MathJax.Hub.Config({\n            tex2jax: {\n                inlineMath: [ [\'$\',\'$\'], ["\\\\(","\\\\)"] ],\n                displayMath: [ [\'$$\',\'$$\'], ["\\\\[","\\\\]"] ]\n            },\n            displayAlign: \'left\', // Change this to \'center\' to center equations.\n            "HTML-CSS": {\n                styles: {\'.MathJax_Display\': {"margin": 0}}\n            }\n        });\n        MathJax.Hub.Queue(["Typeset", MathJax.Hub]);\n    }\n})();\n</script>\n\n')
        __M_writer(u'<script type="text/javascript" src="https://c328740.ssl.cf1.rackcdn.com/mathjax/latest/MathJax.js"></script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "ascii", "line_map": {"34": 28, "15": 0, "22": 1, "23": 1, "24": 1, "25": 5, "26": 21, "27": 21, "28": 43}, "uri": "/home/pfan/modular-file-renderer/mfr_ipynb/templates/ipynb.mako", "filename": "/home/pfan/modular-file-renderer/mfr_ipynb/templates/ipynb.mako"}
__M_END_METADATA
"""
