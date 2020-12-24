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
    pass

    # if self.name == "dropna":
    #     cols = self.args.split(",") if self.args else None
    #     foo = lambda df: df.dropna(subset=cols, inplace=True)

    # elif self.name == "query":
    #     foo = lambda df: df.query(expr=self.args, inplace=True)

    # elif self.name == "sed":
    #     rx, rval, *cols = self.args.split("//")
    #     if cols:
    #         cols = cols[0].split(",")
    #         to_reps: dict = {cname: rx for cname in cols}
    #         to_vals: dict = {cname: rval for cname in cols}
    #         foo = lambda df: df.replace(
    #             to_replace=to_reps, value=to_vals, regex=True, inplace=True
    #         )
    #     else:
    #         foo = lambda df: df.replace(regex=rx, value=rval, inplace=True)


class Dropna(BaseOp):
    name = "dropna"

    def func_apply(self, df: pd.DataFrame) -> NoReturnType:
        cols = self.op_args.split(",") if self.op_args else None
        df.dropna(subset=cols, inplace=True)


class Query(BaseOp):
    name = "query"

    def func_apply(self, df: pd.DataFrame) -> NoReturnType:
        df.query(expr=self.op_args, inplace=True)


class Sed(BaseOp):
    name = "sed"

    def func_apply(self, df: pd.DataFrame) -> NoReturnType:
        rx, rval, *cols = self.op_args.split("//")
        if cols:
            cols = cols[0].split(",")
            to_reps: dict = {cname: rx for cname in cols}
            to_vals: dict = {cname: rval for cname in cols}
            func = lambda df: df.replace(
                to_replace=to_reps, value=to_vals, regex=True, inplace=True
            )
        else:
            func = lambda df: df.replace(regex=rx, value=rval, inplace=True)

        func(df)


class Sortby(BaseOp):
    name = "sortby"

    def func_apply(self, df: pd.DataFrame) -> NoReturnType:
        cols = []
        ascs = []
        for arg in self.op_args.split(","):
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
