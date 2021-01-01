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
from csvwrangle import __version__


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

    def parse_args(self, ctx, args):
        if not args and self.no_args_is_help and not ctx.resilient_parsing:
            click.echo(ctx.get_help(), color=ctx.color)
            ctx.exit()

        self.wrangle_ops = self.extract_wrangle_ops(ctx, args.copy())
        return super().parse_args(ctx, args)

    def extract_wrangle_ops(self, ctx, raw_args: ListType) -> ListType[dict]:
        parsed_opts: DictType[str, str]
        leftovers: ListType
        ordered_params: ListType[UnionType[click.Argument, click.Option, WrangleOption]]
        ordered_ops: ListType[WrangleOption]

        parser = ctx.command.make_parser(ctx)
        parsed_opts, leftovers, ordered_params = parser.parse_args(args=raw_args.copy())
        ordered_operations = [p for p in ordered_params if isinstance(p, WrangleOption)]

        operations = []
        xopts = parsed_opts.copy()
        for i, op in enumerate(ordered_operations):
            opname = op.name
            params = parsed_opts[opname]
            argvals = params.pop(0)
            if op.nargs > 1:
                opargs = tuple(op.type(v) for v in argvals)
            else:
                opargs = (op.type(argvals),)

            d = {"name": opname, "op_args": opargs, "index": i}
            operations.append(d)

        return operations


class WrangleOption(click.Option):
    def __init__(self, *args, **kwargs):
        kwargs["multiple"] = True
        super().__init__(*args, **kwargs)
        self.opname = self.metavar


class Printer:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def debug(self, content, **kwargs):
        if self.is_verbose:
            kwargs["fg"] = kwargs.get("fg") or "cyan"
            kwargs["err"] = True
            self.outs(content, **kwargs)

    def info(self, content, **kwargs):
        if self.is_verbose:
            kwargs["fg"] = kwargs.get("fg") or "green"
            kwargs["err"] = True
            self.outs(content, **kwargs)

    def outs(self, content, **kwargs):
        list_mode = kwargs.pop("as_list", False)

        if list_mode and isinstance(content, (list, tuple)):
            for c in content:
                click.secho(str(c), **kwargs)

        else:
            click.secho(str(content), **kwargs)

    @property
    def is_verbose(self):
        return self.verbose is True


def print_version(ctx=None, param=None, value=None) -> NoReturnType:
    """
    https://click.palletsprojects.com/en/3.x/options/#callbacks-and-eager-options
    """
    if not ctx:
        click.echo(__version__)
    else:
        # this is being used as a callback
        if not value or ctx.resilient_parsing:
            return
        click.echo(__version__)
        ctx.exit()


@click.command(
    cls=WrangleCommand,
    # epilog="the epilog...?",
    no_args_is_help=True,
)
@click.option(
    "--hello",
    cls=WrangleOption,
    nargs=1,
    hidden=True,
    help="""nullfun""",
)
@click.option(
    "--dropna",
    cls=WrangleOption,
    nargs=1,
    help="""Drop rows that have NaN/NULL values. Pass in a comma-delimited list of column namesto check for NaN/NULL values, or pass in "*" to check all columns """,
)
@click.option(
    "--fillna",
    cls=WrangleOption,
    nargs=1,
    help="""Fill all NaN/NULL values. Pass in a single [STRING] value to apply to all columns. Else, pass in a comma-delimited list of column names, each with a colon and fill value.
            e.g. 'col1:0,col2:hello,col3:world'
            """,
)
@click.option(
    "--eval",
    cls=WrangleOption,
    nargs=1,
    help="""
    Create a new column from operations on the dataframe. Assignment is required, e.g. "newcol = col1 + col2"

    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.eval.html
    """,
)
@click.option(
    "--head",
    cls=WrangleOption,
    nargs=1,
    type=click.INT,
    help="""Return the first [INTEGER] rows""",
)
@click.option(
    "--replace",
    cls=WrangleOption,
    nargs=3,
    help="""Do a pandas.DataFrame.replace on complete and literal strings""",
)
@click.option(
    "--replacex",
    cls=WrangleOption,
    nargs=3,
    help="""Do a pandas.DataFrame.replace on regexes""",
)
@click.option(
    "--round",
    cls=WrangleOption,
    nargs=1,
    type=click.STRING,
    help="""Pass in a comma-delimited list of column names (or '*' for all) to round numerical values.
        Specify the number of decimal places per column with a colon, e.g. 'col1,col2:1,col3:4'  """,
)
@click.option(
    "--sortby",
    cls=WrangleOption,
    nargs=1,
    type=click.STRING,
    help="""Pass in comma-delimited list of column names to sort by. Specify sort direction per column with a colon followed by
            'asc' or 'desc', e.g. 'col1,col2:desc,col3:asc' """,
)
@click.option(
    "--query",
    "-q",
    cls=WrangleOption,
    type=click.STRING,
    help="""Pass in a conditional expression to filter rows by, e.g.  'col1 > col2 & col3 == "yes"' """,
)
@click.option(
    "--tail",
    cls=WrangleOption,
    nargs=1,
    type=click.INT,
    help="""Return the last [INTEGER] rows""",
)
@click.argument(
    "input_file",
    default=sys.stdin,
    required=True,
    type=click.File("r"),
    # exists=True,
    # file_okay=True,
    # dir_okay=False,
)
@click.option(
    "--just-text",
    metavar="just_text",
    is_flag=True,
    help="Import every data column as text",
)
@click.option(
    "--version",
    callback=print_version,
    is_eager=True,
    is_flag=True,
    help="Print the version of csvwrangle",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="be verbose or not",
)
@click.pass_context
def main(ctx, **kwargs):
    """
    csvwrangle (cvr) is a command-line tool for wrangling data with Pandas
    """
    # import IPython; IPython.embed()
    PRINT = Printer(verbose=kwargs["verbose"])

    PRINT.info(f'opening {kwargs["input_file"]}...')

    opts = {"just_text": kwargs.get("just_text")}
    cf = CFrame(kwargs["input_file"], options=opts)

    PRINT.info("Original data")
    PRINT.debug(cf.to_csv())

    wrangle_ops = ctx.command.wrangle_ops
    PRINT.debug(f"{len(wrangle_ops)} operations:")
    PRINT.debug(wrangle_ops, as_list=True)
    PRINT.debug("")

    for w in wrangle_ops:
        op = build_operation(name=w["name"], op_args=w["op_args"])
        PRINT.info(op)

        # modify dataframe
        cf.execute(op)
        PRINT.debug(cf.to_csv())

    PRINT.info("Final data", fg="green")
    PRINT.outs(cf.to_csv(), nl=False)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
