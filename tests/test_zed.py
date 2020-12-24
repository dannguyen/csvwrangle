"""
this is just a placeholder until i figure out proper click option parsing,
i.e. --query 'amount > 20' --sortby 'name:desc'
instead of:  -z query 'amount > 20' -z sortby 'name:desc'
"""

import pytest
from click.testing import CliRunner
from csvwrangle.cli import main as cli


def runclick(*args):
    return CliRunner(mix_stderr=False).invoke(cli, *args)


def test_zed_dropna_any():
    args = ["examples/na.csv", "-z", "dropna", ""]
    res = runclick(args)
    assert res.stdout.splitlines() == [
        "code,region,costs",
        "1.0,east,10.0",
    ]


def test_zed_dropna_within_cols():
    args = ["examples/na.csv", "-z", "dropna", "costs,code"]
    res = runclick(args)
    assert res.stdout.splitlines() == [
        "code,region,costs",
        "1.0,east,10.0",
        "3.0,,42.5",
    ]


def test_zed_query():
    args = ["examples/tings.csv", "-z", "query", 'amount < 30 | name == "Ellie"']
    res = runclick(args)
    assert res.stdout.splitlines() == [
        "name,amount",
        "Alice,20",
        "Bob,10",
        "Ellie,42",
    ]


def test_zed_sed_default():
    args = ["examples/tings2.csv", "-z", "sed", r"\d+|\w{5,}//HEY"]
    res = runclick(args)
    assert res.stdout.splitlines() == [
        "name,alias",
        "HEY,HEY DHEYg",
        "Bob,HEY",
        "HEY,HEY-HEY-GUY",
        "Dina,HEY",
        "HEY,Elle",
    ]



def test_zed_sed_on_cols():
    args = ["examples/tings3.csv", "-z", "sed", r"[A-Z]//X//alias,id"]
    res = runclick(args)
    assert res.stdout.splitlines() == [
"id,name,alias",
"1X,Alice,Xlpha X0g",
"2X,Bob,burgerman",
"3X,Carson,90-210-XXX",
"4X,Dina,Xinosaur",
"5X,Ellie,Xlle",
   ]

# "id,name,alias",
# "1A,Alice,Alpha D0g",
# "2B,Bob,burgerman",
# "3C,Carson,90-210-GUY",
# "4D,Dina,Dinosaur",
# "5E,Ellie,Elle",


def test_zed_sortby():
    args = ["examples/fruits.csv", "-z", "sortby", "product:asc,season,revenue:desc"]
    res = runclick(args)
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


def test_zed_multifoo():
    args = [
        "examples/fruits.csv",
        "-z",
        "sed",
        r"ora\w+//citrus",
        "-z",
        "query",
        "product == 'citrus' | revenue > 100",
        "-z",
        "sortby",
        "product:asc,season,revenue:desc",
    ]
    res = runclick(args)
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
