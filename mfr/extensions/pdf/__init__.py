# -*- coding: utf-8 -*-
# from mfr.core_methods import FileHandler, get_file_extension
# from .render import render_html
from .render import PdfRenderer

#
# EXTENSIONS = ['.pdf']
#
#
# class Handler(FileHandler):
#     """FileHandler for Portable Document Format files."""
#     renderers = {
#         'html': render_html,
#     }
#
#     exporters = {}
#
#     def detect(self, fp):
#         return get_file_extension(fp.name) in EXTENSIONS
