import pytest
from tests.tutils import runcli


def test_head_basic():
    res = runcli(["--head", "2", "examples/dummy.csv"])
    assert res.stdout.splitlines() == [
        "X,Y",
        "a,1",
        "b,2",
    ]


def test_head_non_integer():
    with pytest.raises(ValueError) as err:
        res = runcli(["--head", "a", "examples/dummy.csv"])

    assert """invalid literal for int() with base 10: 'a'""" in str(err.value)


def test_tail_basic():
    res = runcli(["--tail", "2", "examples/dummy.csv"])
    assert res.stdout.splitlines() == [
        "X,Y",
        "c,3",
        "d,4",
    ]


def test_tail_non_integer():
    with pytest.raises(ValueError) as err:
        res = runcli(["--tail", "a", "examples/dummy.csv"])

    assert """invalid literal for int() with base 10: 'a'""" in str(err.value)
