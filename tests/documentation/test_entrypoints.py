import os
import pytest
import pkg_resources

class TestEntryPoints:

    def test_entry_points(self):

        parent_dir = os.pardir
        readme_path = os.path.join(os.path.dirname((parent_dir)), 'supportedextensions.md')
        with open(readme_path, 'r') as file:
            readme_ext = [line.strip()[2:] for line in file if '*' in line]
        for ep in pkg_resources.iter_entry_points(group='mfr.exporters'):
            assert ep.name in readme_ext
