import pandas as pd
from pathlib import Path
from typing import (
    Callable as CallableType,
    Dict as DictType,
    List as ListType,
    NoReturn as NoReturnType,
    Optional as OptionalType,
    Union as UnionType,
)

from csvwrangle.exceptions import InvalidOperationName


class Operation:
    name = "generic"
    is_inplace = True  # whether the operation is inplace type

    def __init__(self, op_args):
        # TK remove index, not needed at this point?
        self.op_args = op_args

    def __repr__(self):
        return self.metatext

    def func_apply(self, df: pd.DataFrame) -> NoReturnType:
        """Defined in each subclass; generally, as a pandas.DataFrame.Function() with inplace=True"""
        pass

    @property
    def metatext(self) -> str:
        return f"{self.name}: {self.op_args}"


class BaseOp(Operation):
    """not sure why I have this"""

    pass


class Hello(BaseOp):
    name = "hello"

    def func_apply(self, df):
        df.drop(columns=df.columns, inplace=True)
        df.drop(df.index, inplace=True)
        df.insert(0, "axe", ["hello", "world"])
        df.insert(1, "bee", [98, 12])


class Dropna(BaseOp):
    name = "dropna"

    def func_apply(self, df: pd.DataFrame) -> NoReturnType:
        arg = self.op_args[0]
        cols = None if arg == "*" else arg.split(",")
        df.dropna(subset=cols, inplace=True)


class Head(BaseOp):
    name = "head"
    is_inplace = False

    def func_apply(self, df):
        n = int(self.op_args[0])
        return df.head(n)


class Tail(BaseOp):
    name = "tail"
    is_inplace = False

    def func_apply(self, df):
        n = int(self.op_args[0])
        return df.tail(n)


class Query(BaseOp):
    name = "query"

    def func_apply(self, df: pd.DataFrame) -> NoReturnType:
        expr, *tkargs = self.op_args
        df.query(expr=expr, inplace=True)


class Replacex(BaseOp):
    name = "replacex"

    def func_apply(self, df: pd.DataFrame) -> NoReturnType:
        rx, rval, cols = self.op_args
        if cols == "*":
            func = lambda df: df.replace(regex=rx, value=rval, inplace=True)
        else:
            cols = cols.split(",")
            to_reps: dict = {cname: rx for cname in cols}
            to_vals: dict = {cname: rval for cname in cols}
            func = lambda df: df.replace(
                to_replace=to_reps, value=to_vals, regex=True, inplace=True
            )

        func(df)


class Sortby(BaseOp):
    name = "sortby"

    def func_apply(self, df: pd.DataFrame) -> NoReturnType:

        cols = []
        ascs = []
        for arg in self.op_args[0].split(","):
            c, *a = arg.split(":", 1)
            cols.append(c)
            a = a[0] if a else "asc"
            ascs.append(a != "desc")

        df.sort_values(by=cols, ascending=ascs, inplace=True)


def build_operation(name: str, op_args: str) -> Operation:
    """factory method"""
    clsname = name.capitalize()
    try:
        cls = globals()[clsname]
    except KeyError as err:
        # import IPython; IPython.embed()
        raise InvalidOperationName(err.args[0].lower())

    return cls(op_args=op_args)
