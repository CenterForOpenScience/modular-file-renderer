# -*- coding: utf-8 -*-

from mfr.ext import (
    audio,
    code_pygments,
    docx,
    image,
    ipynb,
    jsc3d,
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
    jsc3d.Handler,
    movie.Handler,
    pdb.Handler,
    pdf.Handler,
    rst.Handler,
    tabular.Handler,
]
