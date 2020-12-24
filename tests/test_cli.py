import pytest
from tests.tutils import runcli


def test_main_help():
    result = runcli(["--help"])
    assert result.exit_code == 0
    assert (
        "csvwrangle (cvr) is a command-line tool for wrangling data with Pandas"
        in result.output
    )


def test_just_input_file_no_operations():
    """
    note how `code` is inferred to be numerical, and `costs` are floats, e.g. -7 is -7.0
    """
    result = runcli(["examples/hi.csv"])
    assert result.output.splitlines() == [
        "code,region,costs",
        "1,east,-7.0",
        "2,west,42.5",
    ]


def test_dropna_but_pointless():
    """
    note how `code` is inferred to be numerical, and `costs` are floats, e.g. -7 is -7.0
    """
    result = runcli(["--dropna", "code,region,costs", "examples/hi.csv"])
    assert result.output.splitlines() == [
        "code,region,costs",
        "1,east,-7.0",
        "2,west,42.5",
    ]
