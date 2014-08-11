from .dependencies import ezodf
from .utilities import data_population, header_population


def data_from_ezodf(fp):

    workbook = ezodf.opendoc(fp.name)
    sheet = workbook.sheets[0]

    list_data = [[cell.value for cell in row] for row in sheet.rows()]

    header = header_population(list_data[0])
    data = data_population(list_data)

    return header, data
