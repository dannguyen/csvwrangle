import pytest
from click.testing import CliRunner
from csvwrangle.cli import main as maincli


def runcli(*args):
    return CliRunner(mix_stderr=False).invoke(maincli, *args)
