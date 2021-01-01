import pytest
from tests.tutils import runcli


def test_replacex_default():
    args = ["examples/tings2.csv", "--replacex", r"\d+|\w{5,}", "HEY", "*"]
    res = runcli(args)
    assert res.stdout.splitlines() == [
        "name,alias",
        "HEY,HEY DHEYg",
        "Bob,HEY",
        "HEY,HEY-HEY-GUY",
        "Dina,HEY",
        "HEY,Elle",
    ]


def test_replacex_on_cols():
    args = ["examples/tings3.csv", "--replacex", r"[A-Z]", "X", "alias,id"]
    res = runcli(args)
    assert res.stdout.splitlines() == [
        "id,name,alias",
        "1X,Alice,Xlpha X0g",
        "2X,Bob,burgerman",
        "3X,Carson,90-210-XXX",
        "4X,Dina,Xinasaur",
        "5X,Ellie,Xlle",
    ]
