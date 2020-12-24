import click
import pandas as pd  # TK: kill this after CFrame is implemented
from pathlib import Path
import re
import sys
from typing import NoReturn as NoReturnType, List as ListType

from csvwrangle import __version__
from csvwrangle.frame import CFrame
from csvwrangle.utils.sysio import clout, clerr


def print_version(ctx=None, param=None, value=None) -> NoReturnType:
    """
    https://click.palletsprojects.com/en/3.x/options/#callbacks-and-eager-options
    """
    if not ctx:
        clout(__version__)
    else:
        # this is being used as a callback
        if not value or ctx.resilient_parsing:
            return
        clout(__version__)
        ctx.exit()


def collect_ops(ctx=None, param=None, values=None) -> tuple:
    # values is a tuple of all params gathered for a given option
    if not ctx.obj:
        ctx.obj = []

    for v in values:
        ctx.obj.append({"name": v[0], "expr": v[1]})

    return values


@click.command(no_args_is_help=True)
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
    # TK: `df` should be a reference to a CFrame
    df = pd.read_csv(kwargs["input_file"])
    ops_list = ctx.obj
    # import IPython; IPython.embed()

    tx = df  # TK: `tx` should be a reference to a CFrame

    for i, op in enumerate(ops_list):
        if i == 0:
            click.secho("original", err=True, fg="green")
            click.secho(tx.to_csv(index=False), fg="cyan", err=True)

        op_name = op["name"]
        op_param = op["expr"]
        click.secho(f"""{op_name}: "{op_param}" """, fg="green", err=True)
        if op_name == "dropna":
            cols = op_param.split(",") if op_param else None
            foo = lambda _df: _df.dropna(subset=cols)
        elif op_name == "sed":
            rx, rval = op_param.split("//")
            foo = lambda _df: _df.replace(regex=rx, value=rval)

        elif op_name == "sortby":
            cols = []
            ords = []
            for x in op_param.split(","):
                _c, *_o = x.split(":", 1)
                cols.append(_c)
                _o = _o[0] if _o else "asc"
                ords.append(_o != "desc")
            foo = lambda _df: _df.sort_values(by=cols, ascending=ords)

        else:
            foo = lambda _df: getattr(_df, op_name)(op_param)

        tx = tx.pipe(foo)
        click.secho(tx.to_csv(index=False), fg="cyan", err=True)

    # sys.stderr.write(f'{ops_list=}\n')
    click.echo(tx.to_csv(index=False), nl=False)


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
