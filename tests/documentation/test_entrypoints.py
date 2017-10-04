import os
import pytest


class TestEntryPoints:

    def test_entry_points(self):
        parent_dir = os.pardir
        readme_path = os.path.join(os.path.dirname((parent_dir)), 'supportedextensions.md')
        with open(readme_path, 'r') as file:
            readme_ext = [line.strip()[2:] for line in file if '*' in line]
        setup_path = os.path.join(os.path.dirname((parent_dir)), 'setup.py')
        with open(setup_path, 'r') as file:
            parse = False
            setup_ext = []
            for line in file:
                if parse and '#' not in line and ' = ' in line:
                    setup_ext.append(line.strip().split(' = ')[0][1:])
                # after you see this line its okay to start parsing
                if '\'mfr.renderers\': [' in line:
                    parse = True
        setup_ext.remove('none')
        assert sorted(setup_ext) == sorted(readme_ext)
