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
from csvwrangle.op import build_operation
from csvwrangle.utils.sysio import clout, clerr, print_version

OPS_PARAMS = []


class OpThing(click.ParamType):
    def convert(self, value, param, ctx):
        ctx.obj = ctx.obj or []
        ctx.obj.append((param, value))
        # OPS_LIST.append({
        #         'name': param.name, 'args': value
        #     })
        return value


# def collect_ops(ctx=None, param=None, values=None):
#     """
#     TK: this is just a placeholder until I figure out how to properly subclass Click stuff
#     """
#     if not ctx.obj:
#         ctx.obj = []

#     for v in values:
#         ctx.obj.append({"name": v[0], "expr": v[1]})

#     return values


@click.command(
    epilog="the end...?",
    no_args_is_help=True,
)
@click.option(
    "--dropna",
    metavar="dropna",
    nargs=1,
    type=OpThing(),
    multiple=True,
    help="""Do a pandas.DataFrame.replace:""",
)
@click.option(
    "--sed",
    metavar="sed",
    type=OpThing(),
    multiple=True,
    help="""Do a pandas.DataFrame.replace:""",
)
@click.option(
    "--sortby",
    metavar="sortby",
    type=OpThing(),
    multiple=True,
    help="""Do a pandas.DataFrame.sort_values:""",
)
@click.option(
    "--query",
    "-q",
    metavar="query",
    type=OpThing(),
    multiple=True,
    help="""Do a pandas.DataFrame.query:""",
)
@click.option(
    "--version",
    callback=print_version,
    is_eager=True,
    is_flag=True,
    help="Print the version of csvwrangle",
)
@click.argument(
    "input_file",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    required=True,
)
@click.pass_context
def main(ctx, **kwargs):
    """
    csvwrangle (cvr) is a command-line tool for wrangling data with Pandas
    """
    ctx.obj = ctx.obj or []

    # click.secho(f'opening {kwargs["input_file"]}...', err=True, fg="red")
    cf = CFrame(kwargs["input_file"])
    # click.secho("Original data", fg="green", err=True)
    # click.secho(cf.to_csv(), fg="cyan", err=True)

    # get the ops
    opslist = extract_ops_from_raw_args(ops_params=ctx.obj, cargs=sys.argv.copy())
    # click.secho(f"{len(opslist)} operations", fg="red", err=True)

    for x in opslist:
        op = build_operation(name=x["name"], op_args=x["op_args"])
        #        click.secho(str(op), fg="cyan", err=True)
        cf.execute(op)
        #  click.secho(cf.to_csv(), fg="cyan", err=True)

    # click.secho("Final", fg="green", err=True)
    click.secho(cf.to_csv(), nl=False)


def extract_ops_from_raw_args(ops_params: list, cargs: str) -> ListType[dict]:
    opslist = []
    for o in ops_params:
        param, value = o
        # next(i for i, x in enumerate(raw_args) if raw_args[i] in param.opts and param.name == raw_args[i+1])
        for i, a in enumerate(cargs):
            if a in param.opts and value == cargs[i + 1]:
                d = {"name": param.name, "op_args": value, "index": i}
                opslist.append(d)
    opslist = sorted(opslist, key=lambda o: o["index"])

    return opslist


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover


# OPS_LIST = []
# @click.option(
#     "-z",
#     "--zed",
#     multiple=True,
#     nargs=2,  # TK this needs to be varidic by op type
#     callback=collect_ops,
#     help="a pandas.Dataframe function and expr, e.g. 'query' 'costs>5' ",
# )

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
