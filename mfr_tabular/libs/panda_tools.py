import pandas
from mfr_tabular.utilities import header_population


def csv_pandas(fp):
    """Read and convert a csv file to JSON format using the pandas library
    :param fp: File pointer object
    :return: tuple of table headers and data
    """
    dataframe = pandas.read_csv(fp.name)
    return data_from_dataframe(dataframe)


def dta_pandas(fp):
    """Read and convert a dta file to JSON format using the pandas library
    :param fp: File pointer object
    :return: tuple of table headers and data
    """
    dataframe = pandas.read_stata(fp)
    return data_from_dataframe(dataframe)


def sav_pandas(fp):
    """Read and convert a sav file to JSON format using the pandas library
    :param fp: File pointer object
    :return: tuple of table headers and data
    """
    dataframe = robjectify(fp)
    return data_from_dataframe(dataframe)


def data_from_dataframe(dataframe):
    """Convert a dataframe object to a list of dictionaries
    :param fp: File pointer object
    :return: tuple of table headers and data
    """

    fields = dataframe.keys()
    header = header_population(fields)
    data = [data.to_dict() for _, data in dataframe.iterrows()]

    return header, data


def robjectify(fp):
    """Create a dataframe object using R"""

    import pandas.rpy.common as common
    import rpy2.robjects as robjects
    r = robjects
    r.r("require(foreign)")
    r.r('x <- read.spss("{}",to.data.frame=T)'.format(fp.name))
    r.r('row.names(x) = 0:(nrow(x)-1)')
    return common.load_data('x')
