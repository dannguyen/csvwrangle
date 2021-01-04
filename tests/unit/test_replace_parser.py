import pytest
from csvwrangle.parsers import ReplaceParser

PK = ReplaceParser()

@pytest.mark.skip(reason="maybe replace has to have 3 args")
def test_replace_all_cols():
    """a single value is interpreted as 'all' columns"""
    assert PK.parse("pattern/repl") == [("*", "pattern", "repl")]

@pytest.mark.skip(reason="maybe replace has to have 3 args")
def test_specific_column():
    assert PK.parse("x:pattern/repl") == [("x", "pattern", "repl"),]


@pytest.mark.skip(reason="")
def test_error_cases():
    pass
