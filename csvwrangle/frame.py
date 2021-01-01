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

from csvwrangle.op import Operation


class CFrame:
    def __init__(self, input_file: UnionType[str, Path], options: DictType = {}):
        self.input_file = input_file
        if options.get("just_text"):
            self._dataframe = pd.read_csv(self.input_file, dtype=str)
        else:
            self._dataframe = pd.read_csv(self.input_file)

    def execute(self, op: Operation) -> NoReturnType:
        # operations are assumed to be inplace functions, but the exceptions have is_inplace=False
        if op.is_inplace:
            op.func_apply(self.df)
        else:
            self.df = op.func_apply(self.df)

    @property
    def df(self) -> pd.DataFrame:
        return self._dataframe

    @df.setter
    def df(self, new_df: pd.DataFrame) -> NoReturnType:
        self._dataframe = new_df

    def to_csv(self) -> str:
        return self.df.to_csv(index=False)

    # def process_pipes(self, ops_list: ListType):
    #     tx = self.df  # TK: should be handled with a CFrame helper method

    #     for i, o in enumerate(ops_list):
    #         if i == 0:
    #             yield (self.to_csv(), "Original dataframe")

    #         pop = PipedOp(o["name"], o["expr"])
    #         pop.func(tx)
    #         yield (
    #             tx.to_csv(index=False),
    #             pop.metatext,
    #         )
