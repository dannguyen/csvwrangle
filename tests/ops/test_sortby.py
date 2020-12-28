import pytest
from tests.tutils import runcli


def test_sortby_stdin():
    data = "a,b,c\n4,5,6\n1,8,3\n"
    res = runcli(["--sortby", "a", "-"], input=data)
    assert res.stdout.splitlines() == [
        "a,b,c",
        "1,8,3",
        "4,5,6",
    ]


def test_sortby_cols():
    args = ["examples/fruits.csv", "--sortby", "product:asc,season,revenue:desc"]
    res = runcli(args)
    assert res.stdout.splitlines() == [
        "product,revenue,season,region",
        "apples,60,fall,north",
        "apples,50,fall,south",
        "apples,40,fall,central",
        "apples,40,summer,south",
        "apples,30,summer,central",
        "apples,20,summer,north",
        "oranges,70,fall,north",
        "oranges,50,fall,central",
        "oranges,40,fall,south",
        "oranges,110,summer,north",
        "oranges,80,summer,south",
        "oranges,70,summer,central",
        "peaches,110,fall,south",
        "peaches,90,fall,north",
        "peaches,130,summer,south",
        "peaches,70,summer,north",
    ]
