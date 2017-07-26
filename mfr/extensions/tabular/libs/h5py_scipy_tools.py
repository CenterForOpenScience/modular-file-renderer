from collections import OrderedDict

import h5py
import scipy.io

from mfr.extensions.tabular import exceptions
from mfr.extensions.tabular.utilities import data_population, header_population

def build_sheets(name, list_data, sheets):
    # add default header to fix rendering of some data formats
    header = [i for i in range(1, 1 + len(list_data[0]))]
    values = data_population(list_data, headers=header)
    header = header_population(header)
    sheets[str(name)] = (header, values)
    return sheets

def mat_v73(fp):
    """Read and convert a mat v7.3+ file to JSON format using h5py
    :param fp: File pointer object
    :return: tuple of table headers and data
    """

    # workbook wont be empty. Will atleast have some sort of data in it
    workbook = h5py.File(fp.name, 'r')
    sheets = OrderedDict()
    variables = workbook.items()

    for var in variables:
        name = var[0]
        data = var[1]
        if type(data) is h5py.Dataset:
            # h5py Uses row-major ordering. this fixes it so it displays like it does in matlab
            # basically just flip it on its axis
            list_data = list(zip(*data.value.tolist()))
            sheets = build_sheets(name, list_data, sheets)

    return sheets


def mat_v7(fp):
    """Read and convert a mat v7.0 and below file to JSON format using scipy.io.matload
    :param fp: File pointer object
    :return: tuple of table headers and data
    """
    try:
        # workbook wont be empty, will always have header information
        workbook = scipy.io.loadmat(fp.name)
    except Exception as e:
        if type(e) is NotImplementedError:
            raise e
        else:
            raise(exceptions.UnexpectedFormattingError('''
                Cannot render this file at this time.
                 The file may not be a .mat file, or may be corrupt'''))

    sheets = OrderedDict()

    for key in ('__header__', '__version__', '__globals__'):
        workbook.pop(key, None)

    for key in workbook:
        list_data = workbook[key].tolist()
        sheets = build_sheets(key, list_data, sheets)

    return sheets

def mat_h5py_scipy(fp):
    try:
        return mat_v7(fp)

    except NotImplementedError:
        return mat_v73(fp)
