import pytest
import mfr_pdb


@pytest.mark.parametrize('filename', [
    'protein.pdb',
    'protein.PDB',
    'protein.pDb',
])
def test_detect_protein_extensions(fakefile, filename):
    fakefile.name = filename
    handler = mfr_pdb.Handler()
    assert handler.detect(fakefile) is True


@pytest.mark.parametrize('filename', [
    'otherpdb',
    'other.protein',
    'other',
    'other.p',
])
def test_does_not_detect_other_extensions(fakefile, filename):
    fakefile.name = filename
    handler = mfr_pdb.Handler()
    assert handler.detect(fakefile) is False
