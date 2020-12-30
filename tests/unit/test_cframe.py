import pytest
import pandas as pd
from csvwrangle.frame import CFrame
from csvwrangle.op import Head


def test_cframe_init():
    """accepts a pathname/str"""
    cf = CFrame("examples/dummy.csv")
    assert isinstance(cf.df, pd.DataFrame)


def test_cframe_to_csv():
    cf = CFrame("examples/dummy.csv")
    assert cf.to_csv() == "X,Y\na,1\nb,2\nc,3\nd,4\n"


def test_cframe_inplace_func_apply():
    """all applied functions do inplace modifications on cframe.df"""
    cf = CFrame("examples/dummy.csv")
    df = pd.read_csv("examples/dummy.csv")

    cf.execute(
        Head(
            [
                3,
            ]
        )
    )

    assert cf.df.equals(df.head(3))
