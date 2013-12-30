class TooBigError(Exception):
    pass


def column_population(data):
    """make column headers from the keys in dataframe
    :param data:
    :return: a list of dictionaries
    """
    fields = data.keys()
    columns = [{'id': k, 'name': k, 'field': k, } for k in fields]
    return columns


def row_population(df):
    """Convert the dictionary of lists Pandas has generated from the CSV into
    a list of dicts.
    :param df:
    :return: JSON representation of rows
    """
    #todo this needs to be reformatted NOT to use the row names as a variable
    # to iterate over, this will break spss files that need rownames
    #todo right now it is renaming the rows in [r] when it reads it in
    fields = df.keys()
    num_rows = len(df[fields[0]])
    json_list = []
    for i in range(num_rows):
        json_list.append({})
        for k in fields:
            json_list[i][k] = str(df[k][i])
    return json_list

MAX_COLS = 10
MAX_ROWS = 10


def check_shape(data_frame):
    """ Takes a data_frame and checks if the number of rows or columns is too
    big to quickly reformat into slickgrid's json data
    """
    if data_frame.shape[0] > MAX_ROWS or data_frame.shape[1]>MAX_COLS:
        raise TooBigError



