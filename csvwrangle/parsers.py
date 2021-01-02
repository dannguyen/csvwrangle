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
value: {valdef}
pair : [key (":" value)?]
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

        def value(self, s):
            return self.key(s)

        def pair(self, x):
            return tuple(x)


class SortbyParser(KeyvalParser):
    VALUE_DEF = "/asc|desc/"

    #     definition = (r"""
    # PROPER_NAME: /\w+/
    # column_name : ESCAPED_STRING | PROPER_NAME
    # direction :  /asc|desc/
    # pair : [column_name (":" direction)?]
    # start: [pair ("," pair)*]
    # %import common.ESCAPED_STRING
    # """)

    class Transformer(KeyvalParser.Transformer):
        # def value(self, s):
        #     return self.key(s)
        # def column_name(self, c):
        #     (c, ) = c
        #     if c.type == 'PROPER_NAME':
        #         return c.value
        #     else:
        #         return c[1:-1]

        # def direction(self, o):
        #     (o, ) = o
        #     return o.value

        def pair(self, x):
            if len(x) == 1:
                return tuple(
                    x
                    + [
                        "asc",
                    ]
                )
            else:
                return tuple(x)
