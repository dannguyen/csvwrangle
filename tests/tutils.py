import pytest
from click.testing import CliRunner
from csvwrangle.cli import main as maincli


def runcli(*args, **kwargs):
    kwargs["catch_exceptions"] = (
        True if kwargs.get("catch_exceptions") == True else False
    )
    return CliRunner(mix_stderr=False).invoke(maincli, *args, **kwargs)
