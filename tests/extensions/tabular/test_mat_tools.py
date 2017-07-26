import os

from mfr.extensions.tabular.libs import mat_h5py_scipy

BASE = os.path.dirname(os.path.abspath(__file__))


class TestTabularMatTools:

    def test_mat_73(self):
        with open(os.path.join(BASE, 'files', 'testVer73.mat')) as fp:
            # The two test functions are basically exactly the same. That is because
            # there are different types of mat files. The only way to tell them apart is to
            # try and load them.
            sheets = mat_h5py_scipy()(fp)

        sheet = sheets.popitem()[1]
        assert sheet == ([{'id': 1, 'name': 1, 'field': 1, 'sortable': True}], [{1: 1.0}])

    def test_mat_70(self):
        with open(os.path.join(BASE, 'files', 'testVer70.mat')) as fp:
            # The two test functions are basically exactly the same. That is because
            # there are different types of mat files. The only way to tell them apart is to
            # try and load them.
            sheets = mat_h5py_scipy()(fp)

        sheet = sheets.popitem()[1]
        print(sheet)
        assert sheet == ([{'id': 1, 'name': 1, 'field': 1, 'sortable': True}], [{1: 1.0}])
