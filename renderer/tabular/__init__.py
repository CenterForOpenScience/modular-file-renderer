from .. import FileRenderer
# from .utils import column_population
# from .utils import row_population

import pandas as pd
import json
import os

# data = pd.read_csv('test.csv')

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
    return s

class TabularRenderer(FileRenderer):

    def detect(self, fp):
        return fp.name.endswith('csv')

    def render(self, fp, path):

        data = pd.read_csv('test.csv')
        # print data
        columns = column_population(data)
        rows = row_population(data)
        print columns
        print rows

        html_from_file = open(os.getcwd() + "/renderer/tabular/table.html").read()
        html_with_data = html_from_file % (columns, rows)
        return html_with_data