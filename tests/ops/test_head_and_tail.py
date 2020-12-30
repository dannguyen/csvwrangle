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
    # with pytest.raises(ValueError) as err:
    res = runcli(["--head", "a", "examples/dummy.csv"])
    assert res.exit_code == 2
    assert "Invalid value: a is not a valid integer" in res.stderr


def test_tail_basic():
    res = runcli(["--tail", "2", "examples/dummy.csv"])
    assert res.stdout.splitlines() == [
        "X,Y",
        "c,3",
        "d,4",
    ]


def test_tail_non_integer():
    res = runcli(["--tail", "a", "examples/dummy.csv"])
    assert res.exit_code == 2
    assert "Invalid value: a is not a valid integer" in res.stderr


def test_head_tail_combo():
    res = runcli(["--tail", "3", "--head", "2", "--tail", "2", "examples/dummy.csv"])
    assert res.stdout.splitlines() == [
        "X,Y",
        "b,2",
        "c,3",
    ]
