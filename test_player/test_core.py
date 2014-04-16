# -*- coding: utf-8 -*-
import os
import mfr
import unittest
from player import create_app


class PlayerTest(unittest.TestCase):

    def setUp(self):
        self.FILES_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'files')
        self.app = create_app(
            TESTING=True,
            FILES_DIR=self.FILES_DIR
        ).test_client()

    def tearDown(self):
        pass

    def test_index_request(self):
        index = self.app.get('/')
        assert index.status_code == 200
        data = index.get_data()
        for filename in os.listdir(self.FILES_DIR):
            if filename.startswith('.'):
                assert filename not in data
            else:
                assert filename in data

    def test_render_request(self):
        for filename in os.listdir(self.FILES_DIR):
            fp = open(os.path.join(self.FILES_DIR, filename))
            status_code = self.app.get('/render/{}'.format(filename)).status_code
            if mfr.detect(fp, many=False):
                assert status_code == 200
            else:
                assert status_code == 501

    def test_file_serve_request(self):
        for filename in os.listdir(self.FILES_DIR):
            assert self.app.get('/files/{}'.format(filename)).status_code == 200
