import pytest
from tests.tutils import runcli


def test_just_text_basic():
    """normally, Y col would be converted to floats"""
    data = "a,b\nx,1\ny,\nz,3"
    res = runcli(
        [
            "-",
            "--just-text",
        ],
        input=data,
    )
    assert res.stdout.splitlines() == [
        "a,b",
        "x,1",
        "y,",
        "z,3",
    ]
