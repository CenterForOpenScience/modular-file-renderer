from dependencies import pandas
from utilities import column_population


def data_from_pandas(fp):
    """Read and convert a csv to JSON format using the pandas library
    :param fp: File pointer object
    :return: tuple of columns and rows
    """

    dataframe = pandas.read_csv(fp.name)
    fields = dataframe.keys()
    columns = column_population(fields)
    rows = pandas_row_population(dataframe)

    return columns, rows


def pandas_row_population(dataframe):
    """Convert dataframe into JSON repr of rows
    :param dataframe: object containing data
    :return: rows of data in JSON format
    """

    fields = dataframe.keys()
    rows = []
    for n in range(len(dataframe[fields[0]])):
        rows.append({})
        for col_fields in fields:
            rows[n][col_fields] = str(dataframe[col_fields][n])

    return rows
