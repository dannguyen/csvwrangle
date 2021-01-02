from lark import Lark, Transformer as LarkTransformer
from pathlib import Path
from typing import List as ListType, Tuple as TupleType, Union as UnionType


class MyargParser:
    definition = """
start: "hello"
"""

    def __init__(self, definition: str):
        self.definition = definition
        self.parser = Lark(self.definition)

    def _parse(self, value: str):
        return self.parser.parse(value)

    def _transform(self, parsed):
        return self.Transformer().transform(parsed)

    def parse(self, value: str) -> ListType[TupleType[str, UnionType[str, TupleType]]]:
        return self._transform(self._parse(value))

    class Transformer(LarkTransformer):
        start = list


class KeyvalParser(MyargParser):
    DEF_TEMPLATE = r"""
PROPER_NAME: /\w+/
key : ESCAPED_STRING | PROPER_NAME
val : {valdef}
pair : [key (":" val)?]
start: [pair ("," pair)*]
%import common.ESCAPED_STRING
"""
    VALUE_DEF = "ESCAPED_STRING | PROPER_NAME"

    def __init__(self):
        super().__init__(definition=self.DEF_TEMPLATE.format(valdef=self.VALUE_DEF))

    class Transformer(MyargParser.Transformer):
        def key(self, s):
            (s,) = s
            if s.type == "ESCAPED_STRING":
                return s[1:-1]
            else:
                return s.value

        def val(self, s):
            return self.key(s)

        def pair(self, x):
            return tuple(x)


class SortbyParser(KeyvalParser):
    VALUE_DEF = "/asc|desc/"

    class Transformer(KeyvalParser.Transformer):
        def pair(self, x):
            t = tuple(x)
            if len(x) == 1:
                t = t + ("asc",)
            return t


class KeyintParser(KeyvalParser):
    """
    --round x,y
            x:0,y,z:2
    """

    DEF_TEMPLATE = r"""
PROPER_NAME: /\w+/
key : ESCAPED_STRING | PROPER_NAME
val : {valdef}
pair : [key (":" val)?]
start: val | [pair ("," pair)*]
%import common.ESCAPED_STRING
%import common.INT
"""
    VALUE_DEF = """INT"""
    # DEF_TEMPLATE = (
    #         KeyvalParser.DEF_TEMPLATE + '\n%import common.INT')

    class Transformer(KeyvalParser.Transformer):
        def pair(self, x):
            t = tuple(x)
            if len(x) == 1:
                t = t + (0,)
            return t

        def val(self, s) -> int:
            return int(super().val(s))
