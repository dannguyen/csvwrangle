import pytest
from tests.tutils import runcli


def test_dropna_stdin():
    data = "a,b,c\n4,5,6\n1,8,3\n"
    res = runcli(["--sortby", "a", "-"], input=data)
    assert res.stdout.splitlines() == [
        "a,b,c",
        "1,8,3",
        "4,5,6",
    ]
