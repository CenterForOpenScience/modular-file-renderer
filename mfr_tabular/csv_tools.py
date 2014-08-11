from .utilities import header_population, data_population
import csv


def data_from_csv(fp):
    """Read and convert a csv file to JSON format using the csv library
    :param fp: File pointer object
    :return: tuple of columns and rows
    """

    dialect = csv.Sniffer().sniff((fp).read(1024))
    fp.seek(0)
    # TODO(asmacdo) Nice way of using slickgrid if there is no header
    # has_header = csv.Sniffer().has_header(infile.read())
    # infile.seek(0)
    reader = csv.reader(fp, dialect)
    complete_data = [row for row in reader]

    # First line is the header, other lines are data
    header = header_population(complete_data[0])
    data = data_population(complete_data[1:], complete_data[0])

    return header, data
