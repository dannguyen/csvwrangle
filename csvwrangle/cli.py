import click

#  import pandas as pd  # TK: kill this after CFrame is implemented
from pathlib import Path
import re
import sys
from typing import (
    NoReturn as NoReturnType,
    List as ListType,
    Optional as OptionalType,
    Union as UnionType,
)


from csvwrangle.frame import CFrame
from csvwrangle.op import build_operation
from csvwrangle.utils.sysio import clout, clerr, print_version

OPS_PARAMS = []


class WrangleCommand(click.Command):
    def main(
        self,
        args=None,
        prog_name=None,
        complete_var=None,
        standalone_mode=True,
        **extra,
    ):

        if args is None:
            self.orgargs = sys.argv[1:]
        else:
            self.orgargs = list(args)
        return super().main(args, prog_name, complete_var, standalone_mode, **extra)


class OpThing(click.ParamType):
    pass
    # def convert(self, value, param, ctx):
    #     ctx.obj = ctx.obj or []
    #     ctx.obj.append((param, value))
    #     # OPS_LIST.append({
    #     #         'name': param.name, 'args': value
    #     #     })
    #     return value


@click.command(
    cls=WrangleCommand,
    epilog="the end...?",
    no_args_is_help=True,
)
@click.option(
    "--hello",
    metavar="hello",
    nargs=1,
    type=OpThing(),
    multiple=True,
    help="""nullfun""",
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
    "--replacex",
    metavar="replacex",
    type=OpThing(),
    multiple=True,
    nargs=3,
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
    type=click.File("r"),
    default=sys.stdin,
    required=True,
    # exists=True,
    # file_okay=True,
    # dir_okay=False,
)
@click.pass_context
def main(ctx, **kwargs):
    """
    csvwrangle (cvr) is a command-line tool for wrangling data with Pandas
    """
    # import IPython; IPython.embed()

    # click.secho(f'opening {kwargs["input_file"]}...', err=True, fg="red")
    cf = CFrame(kwargs["input_file"])
    # click.secho("Original data", fg="green", err=True)
    # click.secho(cf.to_csv(), fg="cyan", err=True)

    opslist = extract_ops_from_raw_args(ctx=ctx, raw_args=ctx.command.orgargs.copy())

    # click.secho(f"{len(opslist)} operations", fg="red", err=True)
    for x in opslist:
        op = build_operation(name=x["name"], op_args=x["op_args"])
        #        click.secho(str(op), fg="cyan", err=True)
        cf.execute(op)
        #  click.secho(cf.to_csv(), fg="cyan", err=True)

    # click.secho("Final", fg="green", err=True)
    click.echo(cf.to_csv(), nl=False)


def extract_ops_from_raw_args(ctx, raw_args: ListType) -> ListType[dict]:
    opslist = []
    cmd_options = [o for o in ctx.command.params if isinstance(o.type, OpThing)]

    for i, rawarg in enumerate(raw_args):
        the_param = next((c for c in cmd_options if rawarg in c.opts), None)
        if the_param:
            the_args = raw_args[i + 1 : i + 1 + the_param.nargs]
            d = {"name": the_param.name, "op_args": the_args, "index": i}
            opslist.append(d)

    return opslist


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
