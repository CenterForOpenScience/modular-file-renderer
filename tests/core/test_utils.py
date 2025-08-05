from importlib.metadata import entry_points

from skimage._shared.testing import parametrize

from mfr.core import utils as mfr_utils
from mfr.core.utils import fix_name


class TestGetRendererName:
    def test_get_renderer_name_explicit_assertions(self):
        assert mfr_utils.get_renderer_name("jpg") == "ImageRenderer"
        assert mfr_utils.get_renderer_name("txt") == "CodePygmentsRenderer"
        assert mfr_utils.get_renderer_name("xlsx") == "TabularRenderer"
        assert mfr_utils.get_renderer_name("odt") == "UnoconvRenderer"
        assert mfr_utils.get_renderer_name("pdf") == "PdfRenderer"

    def test_get_renderer_name(self):
        for ep in entry_points().select(group="mfr.renderers"):
            expected = ep.value.split(":")[1].split(".")[0]
            assert mfr_utils.get_renderer_name(ep.name) == expected

    def test_get_renderer_name_no_entry_point(self):
        assert (
            mfr_utils.get_renderer_name(".jpg") == ""
        )  # extensions must begin with a period


class TestGetExporterName:
    def test_get_exporter_name_explicit_assertions(self):
        assert mfr_utils.get_exporter_name("jpg") == "ImageExporter"
        assert mfr_utils.get_exporter_name("odt") == "UnoconvExporter"

    def test_get_exporter_name(self):
        for ep in entry_points().select(group="mfr.exporters"):
            expected = ep.value.split(":")[1].split(".")[0]
            assert mfr_utils.get_exporter_name(ep.name) == expected

    def test_get_exporter_name_no_entry_point(self):
        assert (
            mfr_utils.get_exporter_name(".jpg") == ""
        )  # extensions must begin with a period


@parametrize(
    "inp, out",
    [
        ["jpg", "jpg"],
        ["c++", "cpp"],
        ["h++", "hpp"],
        ["php[345]", "php"],
        ["lasso[89]", "lasso"],
        ["css.in", "css"],
        ["js.in", "js"],
        ["xul.in", "xul"],
    ],
)
def test_fix_name(inp, out):
    assert fix_name(inp) == out
    assert fix_name(f".{inp}") == out
