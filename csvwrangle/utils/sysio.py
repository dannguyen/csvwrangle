import click
import json
import sys
from typing import Any as AnyType, Mapping as MappingType, NoReturn as NoReturnType

from csvwrangle import __version__


def clout(*args, use_stderr: bool = False) -> NoReturnType:
    """top-level method that is used to output to stdout"""
    output = [
        json.dumps(a, indent=2) if isinstance(a, MappingType) else str(a) for a in args
    ]
    click.echo(" ".join(output), err=use_stderr)


def clerr(*args) -> NoReturnType:
    """top-level method that is used to output to stderr"""
    clout(*args, use_stderr=True)


def clexit(code: int, message: AnyType = None):
    """this function exists because I don't understand Click's wrapping of error handling"""
    if message:
        clerr(message)
    sys.exit(code)


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
