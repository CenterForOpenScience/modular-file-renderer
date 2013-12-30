import os
import unittest
import pandas
from pandas.util.testing import assert_frame_equal
from nose.tools import *
from pandas import read_csv
from .renderers import CSVRenderer, STATARenderer, ExcelRenderer, SPSSRenderer

here, _ = os.path.split(os.path.abspath(__file__))


class TestCSV(unittest.TestCase):
    def setUp(self):
        self.renderer = CSVRenderer()

    # Test renderer
    def test_build_df_csv(self):
        file_pointer = open(os.path.join(here, 'fixtures/test.csv'))
        file_path = 'fixtures/test.csv'
        df = self.renderer._build_df(file_pointer)
        test_df = pandas.DataFrame(index = [0,1,2,3])
        test_df['A'] = [1, 2, 3, 4]
        test_df['B'] = [2, 3, 4, 5]
        assert_frame_equal(df, test_df)


class TestSTATA(unittest.TestCase):
    def setUp(self):
        self.renderer = STATARenderer()

    # Test renderer
    def test_build_df_dta(self):
        file_pointer = open(os.path.join(here, 'fixtures/test.dta'))
        df = self.renderer._build_df(file_pointer)
        test_df = pandas.DataFrame(index=[0, 1, 2, 3])
        test_df['A'] = [1, 2, 3, 4]
        test_df['B'] = [2, 3, 4, 5]
        assert_frame_equal(df, test_df)


class TestExcel(unittest.TestCase):
    def setUp(self):
        self.renderer = ExcelRenderer()

    # Test renderer
    def test_build_df_xls(self):
        file_pointer = open(os.path.join(here, 'fixtures/test.xls'))
        df = self.renderer._build_df(file_pointer)
        test_df = pandas.DataFrame(index=[0, 1, 2, 3])
        test_df['A'] = [1.0, 2.0, 3.0, 4.0]
        test_df['B'] = [2.0, 3.0, 4.0, 5.0]
        print df
        print test_df
        assert_frame_equal(df, test_df)

    def test_build_df_xlsx(self):
        file_pointer = open(os.path.join(here, 'fixtures/test.xlsx'))
        df = self.renderer._build_df(file_pointer)
        test_df = pandas.DataFrame(index=[0, 1, 2, 3])
        test_df['A'] = [1.0, 2.0, 3.0, 4.0]
        test_df['B'] = [2.0, 3.0, 4.0, 5.0]
        assert_frame_equal(df, test_df)