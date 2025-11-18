import os

import pytest
from importlib.metadata import entry_points

from mfr.core.utils import fix_name


class TestEntryPoints:

    def test_entry_points(self):

        parent_dir = os.pardir
        readme_path = os.path.join(os.path.dirname(parent_dir), 'supportedextensions.md')
        with open(readme_path) as file:
            readme_ext = [fix_name(line.strip()[2:]) for line in file if '*' in line]
        for ep in entry_points().select(group='mfr.renderers'):
            if ep.name != 'none':
                assert ep.name in readme_ext
