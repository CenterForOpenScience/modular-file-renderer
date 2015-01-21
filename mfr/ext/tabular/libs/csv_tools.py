from mfr_tabular.utilities import header_population, data_population
import csv
import re
from tempfile import NamedTemporaryFile


def csv_csv(fp):
    """Read and convert a csv file to JSON format using the csv library
    :param fp: File pointer object
    :return: tuple of table headers and data
    """
    with NamedTemporaryFile(mode='w+b') as temp:
        data = re.sub('%.*?\n', '', fp.read()).encode('ascii', 'ignore')
        temp.write(data)
        temp.seek(0)
        dialect = csv.Sniffer().sniff((temp).read(1024))
        temp.seek(0)
        reader = csv.reader(temp, dialect)
    complete_data = [row for row in reader]

    # Assume that the first line is the header, other lines are data
    header = header_population(complete_data[0])
    data = data_population(complete_data[1:], complete_data[0])

    return header, data
