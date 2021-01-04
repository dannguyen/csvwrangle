import pytest
from csvwrangle.parsers import FillnaParser

PK = FillnaParser()

def test_fillna_all_cols():
    """a single value is interpreted as 'all' columns"""
    assert PK.parse("fval") == [("*", "fval")]
    assert PK.parse('"quoted val"') == [("*", "quoted val")]


def test_specific_column():
    assert PK.parse("x:fval") == [("x", "fval"),]
    # the parser does not handle type conversion
    assert PK.parse("x:42") == [("x", "42"),]

def test_multi_columns():
    assert PK.parse("x:42,y:hey you") == [("x", "42"), ("y", "hey you"),]


@pytest.mark.skip(reason="should break on list of columns with no values")
def test_error_cases():
    """
    Bad vals:

        - x
        - x:hey,y
        - x,y
    """
    pass
