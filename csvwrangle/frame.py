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


class CFrame:
    def __init__(self, input_file: UnionType[str, Path], options: DictType = {}):
        self.input_file = input_file
        self._dataframe = pd.read_csv(self.input_file)

    def process_pipes(self, ops_list: ListType):
        tx = self.df  # TK: should be handled with a CFrame helper method

        for i, o in enumerate(ops_list):
            if i == 0:
                yield (self.to_csv(), "Original dataframe")

            pop = PipedOp(o["name"], o["expr"])
            # tx = tx.pipe(pop.func)
            # tx = pop.func(tx)   # not needed since we're doing inplace ops on each op
            pop.func(tx)
            yield (
                tx.to_csv(index=False),
                pop.metatext,
            )

    @property
    def df(self) -> pd.DataFrame:
        return self._dataframe

    def to_csv(self) -> str:
        return self.df.to_csv(index=False)


# TK: to be in its own file
class PipedOp:
    """
    This class should handle simple transformations, e.g. NOT groupby, join, pivot, etc
    """

    def __init__(self, name: str, args: str) -> CallableType:
        self.name = name
        self.args = args

    def __repr__(self):
        return self.metatext

    @property
    def func(self):
        if self.name == "dropna":
            cols = self.args.split(",") if self.args else None
            foo = lambda df: df.dropna(subset=cols, inplace=True)

        elif self.name == "query":
            foo = lambda df: df.query(expr=self.args, inplace=True)

        elif self.name == "sed":
            rx, rval, *cols = self.args.split("//")
            if cols:
                cols = cols[0].split(",")
                to_reps: dict = {cname: rx for cname in cols}
                to_vals: dict = {cname: rval for cname in cols}
                foo = lambda df: df.replace(
                    to_replace=to_reps, value=to_vals, regex=True, inplace=True
                )
            else:
                foo = lambda df: df.replace(regex=rx, value=rval, inplace=True)

        elif self.name == "sortby":
            cols = []
            ords = []
            for a in self.args.split(","):
                c, *x = a.split(":", 1)
                cols.append(c)
                x = x[0] if x else "asc"
                ords.append(x != "desc")
            foo = lambda df: df.sort_values(by=cols, ascending=ords, inplace=True)

        return foo

    @property
    def metatext(self) -> str:
        return f"{self.name}: {self.args}"
