import pytest
from csvwrangle.parsers import SortbyParser

PK = SortbyParser()


def test_default_order():
    """
    e.g. --sortby 'colx'
    """
    assert PK.parse("colx") == [("colx", "asc")]
    assert PK.parse("x,y,x") == [("x", "asc"), ("y", "asc"), ("x", "asc")]


def test_set_order():
    """--sortby 'x:desc,y:asc'"""
    assert PK.parse("x:desc") == [("x", "desc")]
    assert PK.parse("x:desc,y,z:asc") == [("x", "desc"), ("y", "asc"), ("z", "asc")]


def test_messy_column_names():
    assert PK.parse('x,"y:asc":desc," 0 9  s:asc::",acol') == [
        ("x", "asc"),
        ("y:asc", "desc"),
        (" 0 9  s:asc::", "asc"),
        ("acol", "asc"),
    ]


def test_reject_non_asc_desc():
    pass


# def test_label_w_single_value():
#     """
#     --sortby 'colx:desc'
#     """
#     assert PK.parse('colx:desc') == [{'colx': ('desc',)}]

# def test_multi_labels():
#     """
#     --sortby 'x,y,z'
#     """
#     assert PK.parse('x,y,z') == [{'x': (), 'y': (), 'z': ()}]


# def test_multi_labels_w_single_value():
#     assert PK.parse('x:asc,y:desc,z:asc') == [{'x': ('asc',), 'y': ('desc',), 'z': ('asc',)}]

# def test_multi_labels_optional_values():
#     assert PK.parse('x,y:desc,z:asc') == [{'x': (), 'y': ('desc',), 'z': ('asc',)}]


# @pytest.mark.skip(reason="do simple pk first")
# def test_single_label_multi_args():
#     assert pk.parse('x:hello,42,world') == [('x', ('hello', '42', 'world',))]
