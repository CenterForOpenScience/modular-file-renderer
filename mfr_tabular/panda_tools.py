from .dependencies import pandas, robjects, common
from .utilities import header_population
from mfr.core import get_file_extension


def data_from_pandas(fp):
    """Read and convert a csv to JSON format using the pandas library
    :param fp: File pointer object
    :return: tuple of columns and rows
    """

    ext = get_file_extension(fp.name)

    if ext == '.csv':
        dataframe = pandas.read_csv(fp.name)
    elif ext == '.dta':
        dataframe = pandas.read_stata(fp)
    elif ext == '.sav':
        dataframe = robjectify(fp)

    fields = dataframe.keys()
    header = header_population(fields)
    data = pandas_data_population(dataframe)

    return header, data


def pandas_data_population(dataframe):
    """Convert dataframe into JSON repr of rows
    :param dataframe: object containing data
    :return: rows of data in JSON format
    """
    return [data.to_dict() for _, data in dataframe.iterrows()]


def robjectify(fp):
    r = robjects
    r.r("require(foreign)")
    r.r('x <- read.spss("{}",to.data.frame=T)'.format(fp.name))
    r.r('row.names(x) = 0:(nrow(x)-1)')
    return common.load_data('x')
