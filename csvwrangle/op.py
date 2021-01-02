import numpy as np
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

from csvwrangle.exceptions import *


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


class Fillna(BaseOp):
    """
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.fillna.html

    example:
        csvwrangle --fillna 0
                   --fillna col1:0,col2:9
    """

    name = "fillna"

    def func_apply(self, df: pd.DataFrame) -> NoReturnType:
        def _typecast(val: str, ctype: np.dtype) -> UnionType[str, int, float]:
            rval = None
            typename = ctype.name
            if "int" in typename:
                try:
                    rval = int(val)
                except ValueError:
                    try:
                        rval = float(val)
                    except ValueError:
                        rval = val
            elif "float" in typename:
                try:
                    rval = float(val)
                except ValueError:
                    rval = val
            else:
                rval = str(val)

            return rval

        cols = self.op_args[0].split(",")
        # TK: use more robust parsing for this
        fillvals = {}
        if len(cols) == 1 and ":" not in cols[0]:
            # user passed in single val, for filling all NA values
            val = cols[0]
            for cname in df.columns:
                ctype = df[cname].dtype
                fillvals[cname] = _typecast(val, ctype)
        else:
            for c in cols:
                # TK more robust parsing
                cname, val = c.split(":")
                ctype = df[cname].dtype
                fillvals[cname] = _typecast(val, ctype)

        df.fillna(value=fillvals, inplace=True)


class Eval(BaseOp):
    name = "eval"

    def func_apply(self, df: pd.DataFrame) -> NoReturnType:
        arg = self.op_args[0]
        try:
            df.eval(expr=arg, inplace=True)
        except ValueError as err:
            raise MissingAssignment(
                f"eval expects the expression to have an assignment, e.g.\n\t newcol = {arg}"
            )


class Head(BaseOp):
    name = "head"
    is_inplace = False

    def func_apply(self, df):
        n = self.op_args[0]
        return df.head(n)


class Tail(BaseOp):
    name = "tail"
    is_inplace = False

    def func_apply(self, df) -> pd.DataFrame:
        n = int(self.op_args[0])
        return df.tail(n)


class Query(BaseOp):
    name = "query"

    def func_apply(self, df: pd.DataFrame) -> NoReturnType:
        expr, *tkargs = self.op_args
        df.query(expr=expr, inplace=True)


class Replace(BaseOp):
    name = "replace"

    def build_args(self, df: pd.DataFrame) -> DictType:
        rx, rval, cx = self.op_args
        cols: ListType[str] = (
            df.columns if cx == "*" else cx.split(",")
        )  # TK more robust parsing
        reps: DictType = {cname: rx for cname in cols}
        vals: DictType = {cname: rval for cname in cols}
        return {
            "to_replace": reps,
            "value": vals,
            "inplace": True,
            "regex": False,
        }

    def func_apply(self, df: pd.DataFrame) -> NoReturnType:
        kargs = self.build_args(df)
        df.replace(**kargs)


class Replacex(Replace):
    name = "replacex"

    def func_apply(self, df: pd.DataFrame) -> NoReturnType:
        kargs = self.build_args(df)
        kargs["regex"] = True
        df.replace(**kargs)
        # rx, rval, cols = self.op_args
        # if cols == "*":
        #     func = lambda df: df.replace(regex=rx, value=rval, inplace=True)
        # else:
        #     cols = cols.split(",")
        #     to_reps: dict = {cname: rx for cname in cols}
        #     to_vals: dict = {cname: rval for cname in cols}
        #     func = lambda df: df.replace(
        #         to_replace=to_reps, value=to_vals, regex=True, inplace=True
        #     )

        # func(df)


class Round(BaseOp):
    """https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.round.html"""

    name = "round"
    is_inplace = False

    def func_apply(self, df: pd.DataFrame) -> pd.DataFrame:
        opargs = self.op_args[0]  # TK: make all op_args assume 1 narg
        if isinstance(opargs[0], int):
            # when user passes in a single int, we assume they want to round
            # all columns to int number of digits
            return df.round(opargs[0])
        else:
            # we assume user passed in key-value pairs of column_name:digits_to_round
            decs = {c: d for c, d in opargs}
            # for a in arg.split(","):
            #     name, *digits = a.split(":", 1)
            #     digits = int(digits[0]) if digits else 0
            #     decs[name] = digits

        return df.round(decimals=decs)


class Sortby(BaseOp):
    name = "sortby"

    def func_apply(self, df: pd.DataFrame) -> NoReturnType:
        # cols = []
        # ascs = []
        # for arg in self.op_args[0].split(","):
        #     c, *a = arg.split(":", 1)
        #     cols.append(c)
        #     a = a[0] if a else "asc"
        #     ascs.append(a != "desc")
        opargs = self.op_args[0]  # TK: make all op_args assume 1 narg
        cols = [o[0] for o in opargs]
        ascs = [o[1] != "desc" for o in opargs]

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
