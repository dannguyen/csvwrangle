import pytest
from tests.tutils import runcli


def test_query_basic():
    args = ["examples/tings.csv", "--query", 'amount < 30 | name == "Ellie"']
    res = runcli(args)
    assert res.stdout.splitlines() == [
        "name,amount",
        "Alice,20",
        "Bob,10",
        "Ellie,42",
    ]
