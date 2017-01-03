""" This library works for some ods files but not others. Because it doesn't
work consistently, we have disabled this for the moment."""

import ezodf
from collections import OrderedDict
from ..utilities import data_population, header_population


def ods_ezodf(fp, renderer_class, extension):
    """Read and convert a ods file to JSON format using the ezodf library
    :param fp: File pointer object
    :return: tuple of table headers and data
    """

    workbook = ezodf.opendoc(fp.name)
    sheets = OrderedDict()

    for sheet in workbook.sheets:
        list_data = [[cell.value for cell in row] for row in sheet.rows()]

        header = header_population(list_data[0])
        data = data_population(list_data)
        sheets[str(sheet)] = (header, data)

    return sheets
