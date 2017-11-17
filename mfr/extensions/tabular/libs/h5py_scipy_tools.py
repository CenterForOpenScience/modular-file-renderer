from collections import OrderedDict

import h5py
import scipy.io

from mfr.extensions.tabular import exceptions as tabular_exceptions
from mfr.extensions.tabular.utilities import data_population, header_population


def build_sheets(name, list_data, sheets):
    # add default header to fix rendering of some data formats
    header = [i for i in range(1, 1 + len(list_data[0]))]
    values = data_population(list_data, headers=header)
    header = header_population(header)
    sheets[str(name)] = (header, values)


def mat_v73(fp):
    """Read and convert a mat v7.3 file to JSON format using h5py
    :param fp: File pointer object
    :return: `OrderedDict` of tuples of table headers and data
    """

    # workbook cannot be empty or none. Will at least have some sort of data in it
    workbook = h5py.File(fp.name, 'r')
    sheets = OrderedDict()

    for var in workbook.items():
        name = var[0]
        data = var[1]
        if isinstance(data, h5py.Dataset):
            # h5py Uses row-major ordering. this fixes it so it displays like it does in matlab
            # basically just flip it on its axis
            list_data = list(zip(*data.value.tolist()))
            build_sheets(name, list_data, sheets)

    return sheets


def mat_v7(fp):
    """Read and convert a mat v7.0 and below (v6, v4) file to JSON format using scipy.io.matload
    :param fp: File pointer object
    :return: `OrderedDict` of tuples of table headers and data
    """
    try:
        # workbook cannot be empty or none, will always have header information
        workbook = scipy.io.loadmat(fp.name)
    except NotImplementedError as e:
        raise e
    except Exception:
        raise tabular_exceptions.UnexpectedFormattingError(
            'Cannot render this file at this time.'
            ' The file may not be a .mat file, or may be corrupted')

    sheets = OrderedDict()

    for key in workbook:
        if key in ('__header__', '__version__', '__globals__'):
            continue
        list_data = workbook[key].tolist()
        build_sheets(key, list_data, sheets)

    return sheets

def mat_h5py_scipy(fp):
    # Try to load the mat file with the v7 library first. If it gives a not implemented error
    # that means the file is in the v7.3 format, and we can use mat_v73 to load it.
    # Valid .mat versions are 4, 6, 7, 7.3. matv7 handles 7 and below.
    try:
        return mat_v7(fp)
    except NotImplementedError:
        return mat_v73(fp)
