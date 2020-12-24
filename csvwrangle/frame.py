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

    @property
    def df(self) -> pd.DataFrame:
        return self._dataframe

    def to_csv(self) -> str:
        return self.df.to_csv(index=False)
