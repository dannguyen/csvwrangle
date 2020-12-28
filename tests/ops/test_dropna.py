import pytest
from io import StringIO

from tests.tutils import runcli

from click.testing import CliRunner
from csvwrangle.cli import main as maincli

# "code,region,costs",
# "01,east,10",
# ",west,20",
# "03,,42.5",
# "04,east,",


def test_dropna_stdin():
    data = "h1,h2,h3\na,,c\nd,e,f\ng,h,i\n"
    # res = runcli(['--dropna', 'h1,h2,h3', '-'], input=data)
    # assert res.stdout.splitlines() == [
    #     'h1,h2,h3',
    #     'd,e,f',
    #     'g,h,i',
    # ]
    res = CliRunner(mix_stderr=True).invoke(
        maincli, ["--dropna", "h1,h2,h3", "-"], input=data, catch_exceptions=False
    )
    assert res.exit_code == 0
    # assert res.stdout.splitlines() == [
    #     'h1,h2,h3',
    #     'd,e,f',
    #     'g,h,i',
    # ]


def test_dropna_no_matches():
    res = runcli(["--dropna", "name,amount", "examples/tings.csv"])

    assert res.stdout.splitlines() == [
        "name,amount",
        "Alice,20",
        "Bob,10",
        "Carson,30",
        "Dina,50",
        "Ellie,42",
    ]


# def test_dropna_any_default():
#     """with no column arg, any row in which ANY column is NA is dropped"""
#     args = [ "--dropna", "" , "examples/na.csv",]
#     res = runcli(args)
#     assert res.stdout.splitlines() == [
#         "code,region,costs",
#         "1.0,east,10.0",
#     ]


# def test_dropna_any_within_cols():
#     res = runcli(
#         [
#             "--dropna",
#             "costs,code",
#             "examples/na.csv",
#         ]
#     )
#     assert res.stdout.splitlines() == [
#         "code,region,costs",
#         "1.0,east,10.0",
#         "3.0,,42.5",
#     ]
