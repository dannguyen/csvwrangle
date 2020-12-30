import pytest
from tests.tutils import runcli


def test_round_all():
    data = "a,b,c\n1,2,3\n4.2,-5.65,7.489\n"
    res = runcli(["--round", "*", "-"], input=data)
    assert res.stdout.splitlines() == [
        "a,b,c",
        "1.0,2.0,3.0",
        "4.0,-6.0,7.0",
    ]


def test_round_by_col():
    data = "a,b,c\n1,2,3\n4.2,-5.65,7.489\n"
    res = runcli(["--round", "a,b", "-"], input=data)
    assert res.stdout.splitlines() == [
        "a,b,c",
        "1.0,2.0,3.0",
        "4.0,-6.0,7.489",
    ]


def test_round_with_digits():
    data = "a,b,c\n1,2,3\n4.2,-5.65,7.489\n"
    res = runcli(["--round", "a:1,b,c:2", "-"], input=data)
    assert res.stdout.splitlines() == [
        "a,b,c",
        "1.0,2.0,3.0",
        "4.2,-6.0,7.49",
    ]
