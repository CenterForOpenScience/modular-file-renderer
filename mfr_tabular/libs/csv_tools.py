from ..utilities import header_population, data_population
import csv


def csv_csv(fp):
    """Read and convert a csv file to JSON format using the csv library
    :param fp: File pointer object
    :return: tuple of table headers and data
    """

    dialect = csv.Sniffer().sniff((fp).read(1024))
    fp.seek(0)
    reader = csv.reader(fp, dialect)
    complete_data = [row for row in reader]

    # Assume that the first line is the header, other lines are data
    header = header_population(complete_data[0])
    data = data_population(complete_data[1:], complete_data[0])

    return header, data
