def column_population(headers):
    """make column headers from a list
    :param headers: list of column headers
    :return: a list of dictionaries
    """
    columns = []
    for field in headers:
        columns.append({
            'id': field,
            'name': field,
            'field': field,
        })
    return columns


def row_population(data, fields=None):
    """Convert a list of lists into a list of dicts associating each
    cell with its column header and row
    :param data: two dimensional list of data
    :param fields: column headers
    :return: JSON representation of rows
    """

    if not fields:
        fields = data[0]

    rows = []
    for n in range(len(data)):
        rows.append({})
        for i in range(len(fields)):
            rows[n][fields[i]] = str(data[n][i])
    return rows
