import pytest
from tests.tutils import runcli


# def test_dropna_any_default():
#     """with no column arg, any row in which ANY column is NA is dropped"""
#     args = [ "--dropna", "" , "examples/na.csv",]
#     res = runcli(args)
#     assert res.stdout.splitlines() == [
#         "code,region,costs",
#         "1.0,east,10.0",
#     ]


def test_dropna_any_within_cols():
    res = runcli(
        [
            "--dropna",
            "costs,code",
            "examples/na.csv",
        ]
    )
    assert res.stdout.splitlines() == [
        "code,region,costs",
        "1.0,east,10.0",
        "3.0,,42.5",
    ]
