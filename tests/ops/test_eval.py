import pytest
from tests.tutils import runcli
from csvwrangle.exceptions import MissingAssignment


def test_eval_stdin():
    data = "a,b,c\n1,2,3\n"
    res = runcli(
        [
            "-",
            "--eval",
            "d = a + b * c",
        ],
        input=data,
    )
    assert res.stdout.splitlines() == [
        "a,b,c,d",
        "1,2,3,7",
    ]


def test_eval_basic():
    res = runcli(
        [
            "examples/dummy.csv",
            "--eval",
            "A = X+X",
            "--eval",
            "B = Y+Y*Y",
            "--eval",
            "Z = A+X",
        ]
    )
    assert res.stdout.splitlines() == [
        "X,Y,A,B,Z",
        "a,1,aa,2,aaa",
        "b,2,bb,6,bbb",
        "c,3,cc,12,ccc",
        "d,4,dd,20,ddd",
    ]


def test_eval_error_when_no_assignment():
    with pytest.raises(MissingAssignment) as err:
        runcli(["examples/dummy.csv", "--eval", "X + X"])

    assert "eval expects the expression to have an assignment" in str(err.value)
