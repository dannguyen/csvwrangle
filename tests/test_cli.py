import pytest
from click.testing import CliRunner
from csvwrangle.cli import main as cli


def test_main_help():
    result = CliRunner().invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert (
        "csvwrangle (cvr) is a command-line tool for wrangling data with Pandas"
        in result.output
    )


def test_no_options_just_input_file():
    """
    note how `code` is inferred to be numerical, and `costs` are floats, e.g. -7 is -7.0
    """
    result = CliRunner(mix_stderr=False).invoke(cli, ["examples/hi.csv"])
    assert result.output.splitlines() == [
        "code,region,costs",
        "1,east,-7.0",
        "2,west,42.5",
    ]
