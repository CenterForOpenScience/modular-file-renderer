import collections
import json

# utils

def column_population(data):
    """make column headers from the keys in dataframe
    :param data:
    :return: a list of dictionaries
    """
    fields = data.keys()
    columns = [{'id': k, 'name': k, 'field': k, } for k in fields]
    return columns


def dict_uni_to_str(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(dict_uni_to_str, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(dict_uni_to_str, data))
    else:
        return data


def row_population(data):
    """Convert the dictionary of lists Pandas has generated from the CSV into
    a list of dicts.
    :param data:
    :return: JSON representation of rows
    """
    #todo this needs to be reformatted NOT to use the row names as a variable
    # to iterate over, this will break spss files that need rownames
    #todo right now it is renaming the rows in [r] when it reads it in
    fields = data.keys()
    num_rows = len(data[fields[0]])
    json_list = []
    for i in range(num_rows):
        json_list.append({})
        for k in fields:
            json_list[i][k] = str(data[k][i])
    return json.dumps(json_list)

