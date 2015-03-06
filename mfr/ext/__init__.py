# -*- coding: utf-8 -*-

from mfr.ext import (
    audio,
    code_pygments,
    docx,
    image,
    ipynb,
    movie,
    pdb,
    pdf,
    rst,
    tabular,
)

ALL_HANDLERS = [
    audio.Handler,
    code_pygments.Handler,
    docx.Handler,
    image.Handler,
    ipynb.Handler,
    movie.Handler,
    pdb.Handler,
    pdf.Handler,
    rst.Handler,
    tabular.Handler,
]
