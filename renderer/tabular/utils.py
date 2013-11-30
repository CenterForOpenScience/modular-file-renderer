import pandas as pd
import json

# data = pd.read_csv('/examples/test.csv')

def column_population(data):
    """make column headers from the keys in dataframe
    :param data:
    :return: a list of dictionaries
    """
    fields = data.keys()
    columns = [{'id':k,'name':k,'field':k,} for k in fields]
    return columns

def row_population(data):
    """Convert the dictionary of lists Pandas has generated from the CSV into
    a list of dicts.
    :param data:
    :return: JSON representation of rows
    """
    fields = data.keys()
    num_rows = len(data[fields[0]])
    json_list = []
    for i in range(num_rows):
        json_list.append({})
        for k in fields:
            json_list[i][k] = str(data[k][i])
    s = json.dumps(json_list)
    print s
    return s