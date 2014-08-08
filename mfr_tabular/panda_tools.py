from dependencies import pandas
from utilities import header_population


def data_from_pandas(fp):
    """Read and convert a csv to JSON format using the pandas library
    :param fp: File pointer object
    :return: tuple of columns and rows
    """

    dataframe = pandas.read_csv(fp.name)
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
