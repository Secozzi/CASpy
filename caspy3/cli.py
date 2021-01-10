#
#    CASPy - A program that provides both a GUI and a CLI to SymPy.
#    Copyright (C) 2021 Folke Ishii
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

# Standard Library
import typing as ty
import traceback
import sys

# PyQt5
from PyQt5.QtCore import QObject, QThreadPool
from PyQt5.QtWidgets import QApplication

# Third party
import click

#
#    CASPy - A program that provides both a GUI and a CLI to SymPy.
#    Copyright (C) 2020 Folke Ishii
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from PyQt5.QtCore import QObject, QThreadPool
from PyQt5.QtWidgets import QApplication

# from .qt_assets.tabs.worker import BaseWorker

import typing as ty
import traceback
import click
import sys


def suppress_qt_warnings() -> None:
    from os import environ

    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"


class EncloseNegative(click.Command):
    def __init__(self, *args, **kwargs) -> None:
        super(EncloseNegative, self).__init__(*args, **kwargs)
        self.params.insert(
            0,
            click.core.Option(
                ("--dont-suppress",),
                is_flag=True,
                default=False,
                help="Set flag to suppress setting envirmental "
                "varables in order to suppress the error "
                "message QT_DEVICE_PIXEL_RATIO.",
            ),
        )

    def parse_args(self, ctx: click.core.Context, args: list) -> list:
        """Enclose every negative number in parentheses so click doesn't think it's an option.
        Everything inside parentheses will concatenate following string until the parentheses matches.
        For example:
        args before:
            ["caspy", "sin(x**2", " + ", "x**(", " 1/3)", "-1", ")", "-1", "x"]
        args after:
            ["caspy", "sin(x**2 + x**( 1/3) -1)", "-1", "x"]
        """
        if "--dont-suppress" not in args:
            suppress_qt_warnings()

        # Throw error if parentheses doesn't match
        if ("".join(args).count(")") - "".join(args).count("(")) != 0:
            raise Exception("Parentheses not matching") from SyntaxError

        fixed = []
        i = 0
        while i < len(args):
            temp = args[i]
            temp_c = 0
            while (temp.count(")") - temp.count("(")) != 0:
                temp_c += 1
                temp += args[i + temp_c]
            i += temp_c + 1
            fixed.append(temp)

        args = fixed

        for arg in args:
            if len(arg) > 1:
                if arg[0] == "-" and arg[1] in "0123456789()":
                    args[args.index(arg)] = f"({arg})"

                if len(arg) == 3:  # '-oo' negative infinity
                    if arg == "-oo":
                        args[args.index(arg)] = f"({arg})"

        return super(EncloseNegative, self).parse_args(ctx, args)


# Default flags, these flags are added
# to a command by using the decorator '@add_options(DEFAULT_FLAGS)'.
DEFAULT_FLAGS = [
    click.option(
        "--preview",
        "-p",
        is_flag=True,
        default=False,
        help="Previews instead of evaluates",
    ),
    click.option(
        "--output-type",
        "-o",
        default=1,
        type=click.IntRange(1, 3),
        help="Select output type, 1 for pretty; 2 for latex and 3 for normal",
    ),
    click.option(
        "--use-unicode", "-u", is_flag=True, default=False, help="Use unicode"
    ),
    click.option(
        "--line-wrap", "-l", is_flag=True, default=False, help="Use line wrap"
    ),
    click.option(
        "--copy",
        "-c",
        type=click.IntRange(1, 3),
        help="Copies the answer. 1 for exact_ans, 2 for approx_ans, and 3 for a list of [exact_ans, "
        "approx_ans].",
    ),
]

# Default argument(s), these argument(s) are added
# to a command by using the decorator '@add_options(DEFAULT_ARGUMENTS)'.
DEFAULT_ARGUMENTS = [
    click.option(
        "--use-scientific",
        "-s",
        type=int,
        default=None,
        help="Notate approximate answer with scientific notation, argument is accuracy",
    ),
    click.option(
        "--accuracy", "-a", type=int, default=10, help="Accuracy of evaluation"
    ),
]

# Options used by equations (This includes formula),
# added to command by using the decorator '@add_options(EQ_FLAGS)'.
EQ_FLAGS = [
    click.option(
        "--domain", "-d", default="Complexes", help="Give domain to solve for"
    ),
    click.option(
        "--verify-domain",
        "-v",
        is_flag=True,
        default=False,
        help="Filter out any solutions that isn't in domain. Doesn't work with solveset. "
        "This flag must be set in order for domain to work if it solves with solve and not"
        "solveset. Needed for system of equations",
    ),
]


def list_merge(default_params: list, input_params: list) -> list:
    """
    Merges two lists, uses element from input_params if it is not None, else use element from default_params

    :param default_params: list
        list of default parameters
    :param input_params: list
        list of parameters entered by user, often shorter than default_params
    :return: list
        return merged list
    """

    output_list = []
    while len(input_params) < len(default_params):
        input_params.append(None)

    for i in range(len(default_params)):
        if input_params[i] is not None:
            output_list.append(input_params[i])
        else:
            output_list.append(default_params[i])

    return output_list


def validate_inputs(
    input_kwargs: dict, default_params: list, input_params: tuple, name: str
) -> dict:
    """
    Validates and restricts some of the inputs:
        1. 'output_type' must be integer between 1 and 3 inclusive
        2. The number of parameters typed in can't exceed the number of default parameters
        3. At least one parameter must be sent

    :param input_kwargs: dict
        Dict with all arguments
    :param default_params: list
        Default parameters
    :param input_params: tuple
        Params typed by user
    :param name: str
        Name of the command
    :return:
        Returns either error along with message if validation failed, or True along with 'pass' if validation passed
    """

    if len(input_params) > len(default_params):
        return {
            "error": f"'{name}' commad doesn't take more than {len(default_params)} parameters."
        }

    if len(input_params) == 0:
        return {"error": f"'{name}' command requires at least one parameter."}

    return {True: "pass"}


def add_options(options: list):
    """
    Adds flags and/or arguments to command via decorator: @add_options(list_of_flags_or_arguments)

    :param options: list
        List of all flags/arguments to add to command
    :return: function
        returns wrapper
    """

    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


@click.group()
def main(**kwargs: dict) -> None:
    pass


@main.command()
def start() -> None:
    """
    Start the GUI
    """
    from caspy3.qt_assets.app.start import main

    main()


if __name__ == "__main__":
    main()
