def header_population(headers):
    """make column headers from a list
    :param headers: list of column headers
    :return: a list of dictionaries
    """
    return [{'id': field, 'name': field, 'field': field} for field in headers]


def data_population(in_data, headers=None):
    """Convert a list of lists into a list of dicts associating each
    cell with its column header and row
    :param data: two dimensional list of data
    :param fields: column headers
    :return: JSON representation of rows
    """

    if not headers:
        headers = in_data[0]

    out_data = []
    for n in range(len(in_data)):
        out_data.append({})
        for i in range(len(headers)):
            out_data[n][headers[i]] = str(in_data[n][i])
    return out_data
