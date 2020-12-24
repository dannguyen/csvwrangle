import click
import pandas as pd  # TK: kill this after CFrame is implemented
from pathlib import Path
import re
import sys
from typing import (
    NoReturn as NoReturnType,
    List as ListType,
    Union as UnionType,
)


from csvwrangle.frame import CFrame
from csvwrangle.utils.sysio import clout, clerr, print_version


def collect_ops(ctx=None, param=None, values=None):
    """
    TK: this is just a placeholder until I figure out how to properly subclass Click stuff
    """
    if not ctx.obj:
        ctx.obj = []

    for v in values:
        ctx.obj.append({"name": v[0], "expr": v[1]})

    return values


@click.command(no_args_is_help=True, epilog="the end...?")
@click.option(
    "--version",
    callback=print_version,
    is_eager=True,
    is_flag=True,
    help="Print the version of csvwrangle",
)
@click.option(
    "-z",
    "--zed",
    multiple=True,
    nargs=2,  # TK this needs to be varidic by op type
    callback=collect_ops,
    help="a pandas.Dataframe function and expr, e.g. 'query' 'costs>5' ",
)
@click.argument(
    "input_file",
    type=click.File("r"),
    required=True,
)
@click.pass_context
def main(ctx, **kwargs):
    """
    csvwrangle (cvr) is a command-line tool for wrangling data with Pandas
    """
    click.secho(f'opening {kwargs["input_file"].name}...', err=True, fg="red")
    cf = CFrame(kwargs["input_file"])
    data: str = ""
    meta: str = ""

    ops_list = ctx.obj
    for i, result in enumerate(cf.process_pipes(ops_list)):
        if i > 0:
            click.secho(meta, fg="green", err=True)
            click.secho(data, fg="cyan", err=True)

        data, meta = result

    # at end of the loop, data is the final iteration of the data
    fin_meta = meta if meta else "No operations"
    fin_data = data if data else cf.to_csv()

    click.secho(fin_meta, fg="green", err=True)
    click.secho(fin_data, nl=False)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover


# OPS_LIST = []


# class OpsList(click.ParamType):
#     name = 'ops-list'

#     def __init__(self, stash:ListType):
#         self.stash = stash
#         super().__init__()

#     def convert(self, value, param, ctx):
#         self.stash.append({'op': param.name, 'expr': value})
#         return value

# @click.option(
#     "--sort",
#     "-s",
#     type=click.STRING,
#     # type=OpsList(OPS_LIST),
#     multiple=True,
#     help="""
#     Do a pandas.DataFrame.sort_values:
#     """,
# )
# @click.option(
#     "--query",
#     "-q",
#     type=click.STRING,
#     # type=OpsList(OPS_LIST),
#     multiple=True,
#     help="""
#     Do a pandas.DataFrame.query:
#     https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html
#     """,
# )
