import pytest
from ppag.utils import find_csv, find_yaml


def test_find_csv_raise_error():
    with pytest.raises(FileNotFoundError):
        find_csv()


def test_find_ymal_raise_error():
    file = find_yaml()
    assert file != ''
