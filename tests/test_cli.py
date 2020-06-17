from click.testing import CliRunner
import os, sys
import src.cli

def test_deriv():
    runner = CliRunner()
    result = runner.invoke(src.cli.deriv, ["x**x", "x"])
    print(result.output)
    assert result.output == ""
    assert result.exit_code == 0

test_deriv()