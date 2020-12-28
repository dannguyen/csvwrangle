import pytest
from tests.tutils import runcli


def test_zed_multifoo():
    args = [
        "examples/fruits.csv",
        "--sed",
        r"ora\w+//citrus",
        "--query",
        "product == 'citrus' | revenue > 100",
        "--sortby",
        "product:asc,season,revenue:desc",
    ]
    res = runcli(args)
    assert res.stdout.splitlines() == [
        "product,revenue,season,region",
        "citrus,70,fall,north",
        "citrus,50,fall,central",
        "citrus,40,fall,south",
        "citrus,110,summer,north",
        "citrus,80,summer,south",
        "citrus,70,summer,central",
        "peaches,110,fall,south",
        "peaches,130,summer,south",
    ]
