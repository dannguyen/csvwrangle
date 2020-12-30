import pytest
from tests.tutils import runcli

"""
tings2 = [
 "name,alias",
 "Alice,Alpha D0g",
 "Bob,burgerman",
 "Carson,90-210-GUY",
 "Dina,Dinasaur",
 "Ellie,Elle",
 ]
"""


def test_replace_default():
    args = ["examples/tings2.csv", "--replace", "Dina", "XO", '*']
    res = runcli(args)
    assert res.stdout.splitlines()  == [
     "name,alias",
     "Alice,Alpha D0g",
     "Bob,burgerman",
     "Carson,90-210-GUY",
     "XO,Dinasaur",
     "Ellie,Elle",
 ]



def test_replace_by_col():
    args = ["-", "--replace", "A", "z", "alpha,gamma"]
    data = "alpha,beta,gamma\nA,A,A\na,A,A\n"

    res = runcli(args, input=data)
    assert res.stdout.splitlines()  == [
     "alpha,beta,gamma",
     "z,A,z",
     "a,A,z",
 ]
