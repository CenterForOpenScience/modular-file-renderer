import pytest
import pkg_resources

from mfr.core import utils as mfr_utils


class TestGetRendererName:

    def test_get_renderer_name_explicit_assertions(self):
        assert mfr_utils.get_renderer_name('.jpg') == 'ImageRenderer'
        assert mfr_utils.get_renderer_name('.txt') == 'CodePygmentsRenderer'
        assert mfr_utils.get_renderer_name('.xlsx') == 'TabularRenderer'
        assert mfr_utils.get_renderer_name('.odt') == 'UnoconvRenderer'
        assert mfr_utils.get_renderer_name('.pdf') == 'PdfRenderer'

    def test_get_renderer_name(self):
        entry_points = pkg_resources.iter_entry_points(group='mfr.renderers')
        for ep in entry_points:
            expected = ep.attrs[0]
            assert mfr_utils.get_renderer_name(ep.name) == expected

    def test_get_renderer_name_no_entry_point(self):
        assert mfr_utils.get_renderer_name('jpg') == ''  # extensions must begin with a period


class TestGetExporterName:

    def test_get_exporter_name_explicit_assertions(self):
        assert mfr_utils.get_exporter_name('.jpg') == 'ImageExporter'
        assert mfr_utils.get_exporter_name('.odt') == 'UnoconvExporter'

    def test_get_exporter_name(self):
        entry_points = pkg_resources.iter_entry_points(group='mfr.exporters')
        for ep in entry_points:
            expected = ep.attrs[0]
            assert mfr_utils.get_exporter_name(ep.name) == expected

    def test_get_exporter_name_no_entry_point(self):
        assert mfr_utils.get_exporter_name('jpg') == ''  # extensions must begin with a period
