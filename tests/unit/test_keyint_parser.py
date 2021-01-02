import pytest
from csvwrangle.parsers import KeyintParser

PK = KeyintParser()


def test_basic():
    assert PK.parse("x:1") == [("x", 1)]
    assert PK.parse("x") == [("x", 0)]


def test_multi():
    assert PK.parse("x:1,y,z:2") == [("x", 1), ("y", 0), ("z", 2)]
    assert PK.parse('x,y," 9$hey-  ":3') == [("x", 0), ("y", 0), (" 9$hey-  ", 3)]


def test_just_int():
    assert PK.parse("3") == [3]


@pytest.mark.curious(
    reason="the user will have a problem if they have an int column name and pass it in unquoted"
)
def test_edge_colname_as_int():
    assert PK.parse('"3"') == [("3", 0)]
