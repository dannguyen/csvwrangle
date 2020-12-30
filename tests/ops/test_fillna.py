import pytest
from tests.tutils import runcli

# "code,region,costs",
# "01,east,10",
# ",west,20",
# "03,,42.5",
# "04,east,",


def test_fillna_mixed_42():
    """
    '42' should be treated as text in 'a' and as float in 'b'
    However, note that b is typecast into float automatically on import
    """
    data = "a,b\nhello,100\n,\nworld,300\n"
    res = runcli(["-", "--fillna", "42"], input=data)
    assert res.stdout.splitlines() == [
        "a,b",
        "hello,100.0",
        "42,42.0",
        "world,300.0",
    ]


def test_fillna_by_col():
    """
    note that even though column b has been 'objectified' thanks to 'bye',
    the existing values in b have already been typecasted as float64
    """
    data = "a,x,b\nhello,,100\n,foo,\nworld,,300\n"
    res = runcli(["-", "--fillna", "a:42,b:bye"], input=data)
    assert res.stdout.splitlines() == [
        "a,x,b",
        "hello,,100.0",
        "42,foo,bye",
        "world,,300.0",
    ]


# def test_fillna_all_nums():
#     """ '42' should be treated as text"""
#     data = "name,val\nhello,1\nbye,\n"
#     res = runcli(["-", "--fillna", 'foo'], input=data)

#     assert res.stdout.splitlines() == [
#         'name,val',
#         'hello,1.0',
#         'bye,foo',
#     ]


# def test_dropna_no_matches():
#     res = runcli(["--dropna", "name,amount", "examples/tings.csv"])
#     assert res.stdout.splitlines() == [
#         "name,amount",
#         "Alice,20",
#         "Bob,10",
#         "Carson,30",
#         "Dina,50",
#         "Ellie,42",
#     ]


# def test_dropna_any_star():
#     """with no column arg, any row in which ANY column is NA is dropped"""
#     args = [
#         "--dropna",
#         "*",
#         "examples/na.csv",
#     ]
#     res = runcli(args)
#     assert res.stdout.splitlines() == [
#         "code,region,costs",
#         "1.0,east,10.0",
#     ]


# def test_dropna_any_within_cols():
#     res = runcli(
#         [
#             "--dropna",
#             "costs,code",
#             "examples/na.csv",
#         ]
#     )
#     assert res.stdout.splitlines() == [
#         "code,region,costs",
#         "1.0,east,10.0",
#         "3.0,,42.5",
#     ]
