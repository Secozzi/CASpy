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

from .qt_assets.tabs.worker import BaseWorker

import typing as ty
import traceback
import click
import sys


class Cli(QObject):
    def __init__(
        self, command: str, params: list, copy: int, worker: ty.Type[BaseWorker]
    ) -> None:
        super(Cli, self).__init__()

        self.command = command
        self.params = params
        self.copy = copy

        self.Worker = worker

        self.threadpool = QThreadPool()

    def stop_thread(self) -> None:
        pass

    def call_worker(self) -> None:
        """
        Call worker, send command and params, and then start thread
        """
        worker = self.Worker(self.command, self.params, self.copy)
        worker.signals.output.connect(self.print_output)
        worker.signals.finished.connect(self.stop_thread)

        self.threadpool.start(worker)

    def print_output(self, input_dict: dict) -> None:
        """
        Prints output then exit program
        :param input_dict: dict
            Dict contaning exact answer and approximate anser or error message
        """
        if list(input_dict.keys())[0] == "error":
            print(list(input_dict.values())[0][0])
        else:
            print("Exact answer:")
            print(list(input_dict.values())[0][0])
            print("\nApproximate answer:")
            print(list(input_dict.values())[0][1])
        sys.exit()


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
    from .qt_gui import main

    main()


@main.command(cls=EncloseNegative)
@add_options(DEFAULT_FLAGS)
@add_options(DEFAULT_ARGUMENTS)
@click.argument("params", nargs=-1, metavar="EXPRESSION VARIABLE [ORDER] [AT_POINT]")
def deriv(params: list, **kwargs: dict) -> None:
    """Derive a function.

    \b
    Example(s):
    >>> caspy deriv x**x x
    >>> caspy deriv sin(1/x) x 3 pi
    """
    from .qt_assets.tabs.derivative import DerivativeWorker

    default_params = ["x", "x", "1", None]

    validate_input_dict = validate_inputs(kwargs, default_params, params, "deriv")
    if list(validate_input_dict.keys())[0] == "error":
        send_to_thread(validate_input_dict)
        return

    if kwargs["preview"]:
        prefix = "prev_"
        options = [kwargs["output_type"], kwargs["use_unicode"], kwargs["line_wrap"]]
    else:
        prefix = "calc_"
        options = [
            kwargs["output_type"],
            kwargs["use_unicode"],
            kwargs["line_wrap"],
            kwargs["use_scientific"],
            kwargs["accuracy"],
        ]

    params_to_send = list_merge(default_params, list(params))

    to_send = [prefix + "deriv", params_to_send + options, kwargs["copy"]]
    send_to_thread(to_send, DerivativeWorker)


@main.command(cls=EncloseNegative)
@add_options(DEFAULT_FLAGS)
@add_options(DEFAULT_ARGUMENTS)
@click.argument(
    "params",
    nargs=-1,
    metavar="EXPRESSION VARIABLE [LOWER_BOUND UPPER_BOUND] [APPROXIMATE]",
)
@click.option(
    "--approximate-integral",
    "-A",
    is_flag=True,
    default=False,
    help="Set flag to approximate integral. This overrides the normal calculation",
)
def integ(params: list, **kwargs: dict) -> None:
    """Calculate definite and indefinite integrals of expressions.

    \b
    Example(s):
    >>> caspy integ 1/sqrt(1-x**2) x -1 1
    >>> caspy integ x**x x -1 1 -A
    """
    from .qt_assets.tabs.integral import IntegralWorker

    default_params = ["x", "x", None, None]

    validate_input_dict = validate_inputs(kwargs, default_params, params, "integ")
    if list(validate_input_dict.keys())[0] == "error":
        send_to_thread(validate_input_dict)
        return

    if kwargs["preview"]:
        prefix = "prev_"
        options = [kwargs["output_type"], kwargs["use_unicode"], kwargs["line_wrap"]]
    else:
        prefix = "calc_"
        options = [
            kwargs["approximate_integral"],
            kwargs["output_type"],
            kwargs["use_unicode"],
            kwargs["line_wrap"],
            kwargs["use_scientific"],
            kwargs["accuracy"],
        ]

    params_to_send = list_merge(default_params, list(params))

    to_send = [prefix + "integ", params_to_send + options, kwargs["copy"]]
    send_to_thread(to_send, IntegralWorker)


@main.command(cls=EncloseNegative)
@add_options(DEFAULT_FLAGS)
@add_options(DEFAULT_ARGUMENTS)
@click.argument("params", nargs=-1, metavar="EXPRESSION VARIABLE START END")
def sum(params: list, **kwargs: dict) -> None:
    """Calculate the summation of an expression.

    \b
    Example(s):
    >>> caspy sum x**k/factorial(k) k 0 oo
    >>> caspy sum k**2 k 1 m
    """
    from .qt_assets.tabs.summation import SummationWorker

    default_params = ["k", "k", 1, 2]

    validate_input_dict = validate_inputs(kwargs, default_params, params, "sum")
    if list(validate_input_dict.keys())[0] == "error":
        send_to_thread(validate_input_dict)
        return

    if kwargs["preview"]:
        prefix = "prev_"
        options = [kwargs["output_type"], kwargs["use_unicode"], kwargs["line_wrap"]]
    else:
        prefix = "calc_"
        options = [
            kwargs["output_type"],
            kwargs["use_unicode"],
            kwargs["line_wrap"],
            kwargs["use_scientific"],
            kwargs["accuracy"],
        ]

    params_to_send = list_merge(default_params, list(params))

    to_send = [prefix + "sum", params_to_send + options, kwargs["copy"]]
    send_to_thread(to_send, SummationWorker)


@main.command(cls=EncloseNegative)
@add_options(DEFAULT_FLAGS)
@add_options(DEFAULT_ARGUMENTS)
@click.argument(
    "params", nargs=-1, metavar="EXPRESSION VARIABLE AS_VARIABLE_IS_APPROACHING [SIDE]"
)
def limit(params: list, **kwargs: dict) -> None:
    """Calculate the limit of an expression.

    \b
    Example(s):
    >>> caspy limit (1+1/(a*n))**(b*n) n oo
    >>> caspy limit n!**(1/n) n 0 -
    """
    from .qt_assets.tabs.limit import LimitWorker

    default_params = ["x", "x", 0, "+-"]

    validate_input_dict = validate_inputs(kwargs, default_params, params, "limit")
    if list(validate_input_dict.keys())[0] == "error":
        send_to_thread(validate_input_dict)
        return

    if kwargs["preview"]:
        prefix = "prev_"
        options = [kwargs["output_type"], kwargs["use_unicode"], kwargs["line_wrap"]]
    else:
        prefix = "calc_"
        options = [
            kwargs["output_type"],
            kwargs["use_unicode"],
            kwargs["line_wrap"],
            kwargs["use_scientific"],
            kwargs["accuracy"],
        ]

    params_to_send = list_merge(default_params, list(params))

    to_send = [prefix + "limit", params_to_send + options, kwargs["copy"]]
    send_to_thread(to_send, LimitWorker)


@main.command(cls=EncloseNegative)
@add_options(DEFAULT_FLAGS)
@add_options(DEFAULT_ARGUMENTS)
@add_options(EQ_FLAGS)
@click.argument(
    "params",
    nargs=-1,
    metavar="LEFT_EXPRESSION RIGHT_EXPRESSION VARIABLE_TO_SOLVE_FOR [SOLVE_TYPE]",
)
@click.option(
    "--approximate-equation", "-A", type=str,
    help="Approximate answer to equation. Argument is starting vector"
)
@click.option(
    "--solve-type",
    "-st",
    is_flag=True,
    default=False,
    help="Solves an equation with either solve or "
    "solveset (see SymPy solve vs solveset). "
    "Default is solve, set flag to solve with "
    "solveset.",
)
def eq(params: list, **kwargs: dict) -> None:
    """Solves a normal equation.

    Separate equation by either a space or a =, but not both.

    \b
    Example(s):
    >>> caspy eq x**x 2 x
    >>> caspy eq sin(x)=1 x -st
    """
    from .qt_assets.tabs.equations import EquationsWorker

    default_params = ["x", 0, "x"]

    if "=" in params[0]:
        if params[0].count("=") != 1:
            print("Enter only one '='")
            return
        params = params[0].split("=") + [params[1]]

    validate_input_dict = validate_inputs(kwargs, default_params, params, "eq")
    if list(validate_input_dict.keys())[0] == "error":
        send_to_thread(validate_input_dict)
        return

    if kwargs["preview"]:
        prefix = "prev_"
        options = [
            kwargs["domain"],
            kwargs["output_type"],
            kwargs["use_unicode"],
            kwargs["line_wrap"],
        ]
    else:
        prefix = "calc_"
        options = [
            kwargs["solve_type"],
            kwargs["domain"],
            kwargs["output_type"],
            kwargs["use_unicode"],
            kwargs["line_wrap"],
            kwargs["use_scientific"],
            kwargs["accuracy"],
            kwargs["verify_domain"],
            kwargs["approximate_equation"],
        ]

    params_to_send = list_merge(default_params, list(params))

    to_send = [prefix + "normal_eq", params_to_send + options, kwargs["copy"]]
    send_to_thread(to_send, EquationsWorker)


@main.command(cls=EncloseNegative)
@add_options(DEFAULT_FLAGS)
@add_options(DEFAULT_ARGUMENTS)
@click.option(
    "--hint", "-h", default="", help="The solving method that you want dsolve to use."
)
@click.argument(
    "params",
    nargs=-1,
    metavar="LEFT_EXPRESSION RIGHT_EXPRESSION FUNCTION_TO_SOLVE_FOR [HINT]",
)
def diff_eq(params: list, **kwargs: dict) -> None:
    """Solves a differential equation equation.
    Separate equation by either a space or a =, but not both.

    \b
    Example(s):
    >>> caspy diff-eq f'(x) 1/f(x) f(x)
    >>> caspy diff-eq f''(x)+3*f'(x)=x**2 f(x)
    """
    from .qt_assets.tabs.equations import EquationsWorker

    default_params = ["f(x)", "f(x)", "f(x)"]

    if "=" in params[0]:
        if params[0].count("=") != 1:
            print("Enter only one '='")
            return
        params = params[0].split("=") + [params[1]]

    validate_input_dict = validate_inputs(kwargs, default_params, params, "diff_eq")
    if list(validate_input_dict.keys())[0] == "error":
        send_to_thread(validate_input_dict)
        return

    if kwargs["preview"]:
        prefix = "prev_"
        options = [kwargs["output_type"], kwargs["use_unicode"], kwargs["line_wrap"]]
    else:
        prefix = "calc_"
        options = [
            kwargs["output_type"],
            kwargs["use_unicode"],
            kwargs["line_wrap"],
            kwargs["use_scientific"],
            kwargs["accuracy"],
        ]

    params_to_send = list_merge(default_params, list(params))

    if not kwargs["preview"]:
        params_to_send.insert(2, kwargs["hint"])

    to_send = [prefix + "diff_eq", params_to_send + options, kwargs["copy"]]

    send_to_thread(to_send, EquationsWorker)


@main.command(cls=EncloseNegative)
@add_options(DEFAULT_FLAGS)
@add_options(DEFAULT_ARGUMENTS)
@add_options(EQ_FLAGS)
@click.option(
    "--solve_type",
    "-st",
    is_flag=True,
    default=False,
    help="Solve either a system of normal equations or a system of differential equations. Defualt if normal,"
    " set flag to solve a system of differential equations.",
)
@click.argument("no_of_eq", type=int, metavar="sys-eq NO_OF_EQUATIONS [SOLVE_TYPE]")
def sys_eq(no_of_eq: int, **kwargs: dict) -> None:
    """Solves a system of either normal or differential equations.
    Takes number of equations as argument, then will prompt user for all equations

    \b
    Example(s):
    >>> caspy sys-eq 5
    >>> caspy sys-eq 3 -d Integers
    """
    from .qt_assets.tabs.equations import EquationsWorker

    if kwargs["solve_type"]:
        solve_type = 2
    else:
        solve_type = 1

    equations = []
    for i in range(no_of_eq):
        equation = input(f"Enter equation number {i + 1} of {no_of_eq}: ")
        equations.append(equation)

    variables = input(
        f"Enter variables to solve for separated by anything other than a-z, 0-9, (), and _: "
    )

    if kwargs["preview"]:
        prefix = "prev_"
        options = [
            kwargs["domain"],
            solve_type,
            kwargs["output_type"],
            kwargs["use_unicode"],
            kwargs["line_wrap"],
        ]
    else:
        prefix = "calc_"
        options = [
            kwargs["domain"],
            solve_type,
            kwargs["output_type"],
            kwargs["use_unicode"],
            kwargs["line_wrap"],
            kwargs["use_scientific"],
            kwargs["accuracy"],
            kwargs["verify_domain"],
        ]

    to_send = [
        prefix + "system_eq",
        [equations] + [variables] + options,
        kwargs["copy"],
    ]

    send_to_thread(to_send, EquationsWorker)


@main.command(cls=EncloseNegative)
@add_options(DEFAULT_FLAGS)
@click.argument("expression")
def simp(expression: str, **kwargs: dict) -> None:
    """Simplifies an expression.

    \b
    Example(s):
    >>> caspy simp sin(x)**2+cos(x)**2
    """
    from .qt_assets.tabs.simplify import SimpWorker

    expression = tuple([expression])

    default_params = ["x"]
    validate_input_dict = validate_inputs(kwargs, default_params, expression, "simp")
    if list(validate_input_dict.keys())[0] == "error":
        send_to_thread(validate_input_dict)
        return

    if kwargs["preview"]:
        prefix = "prev_"
        options = [kwargs["output_type"], kwargs["use_unicode"], kwargs["line_wrap"]]
    else:
        prefix = ""
        options = [kwargs["output_type"], kwargs["use_unicode"], kwargs["line_wrap"]]

    params_to_send = list_merge(default_params, list(expression))
    to_send = [prefix + "simp_exp", params_to_send + options, kwargs["copy"]]

    send_to_thread(to_send, SimpWorker)


@main.command(cls=EncloseNegative)
@add_options(DEFAULT_FLAGS)
@click.argument("expression")
def exp(expression: str, **kwargs: dict) -> None:
    """Expandes an expression.

    \b
    Example(s):
    >>> caspy exp (a+b-c)**3
    """
    from .qt_assets.tabs.expand import ExpandWorker

    default_params = ["x"]
    expression = tuple([expression])
    validate_input_dict = validate_inputs(kwargs, default_params, expression, "exp")
    if list(validate_input_dict.keys())[0] == "error":
        send_to_thread(validate_input_dict)
        return

    if kwargs["preview"]:
        prefix = "prev_"
        options = [kwargs["output_type"], kwargs["use_unicode"], kwargs["line_wrap"]]
    else:
        prefix = ""
        options = [kwargs["output_type"], kwargs["use_unicode"], kwargs["line_wrap"]]

    params_to_send = list_merge(default_params, list(expression))
    to_send = [prefix + "expand_exp", params_to_send + options, kwargs["copy"]]
    send_to_thread(to_send, ExpandWorker)


@main.command(cls=EncloseNegative)
@add_options(DEFAULT_FLAGS)
@add_options(DEFAULT_ARGUMENTS)
@click.argument("expression")
@click.argument("vars_sub", required=False, nargs=-1)
def eval(expression: str, vars_sub: list, **kwargs: dict) -> None:
    """Evaluates an expression.

    After expression you can also subtitute your variables with a value.
    To substitute, simply type the variable to substitute followed by the value separated by a space.

    \b
    For example:
    >>> 3**(x+y) x 3 y 5
    => 3**((3)+(5))
    => 6561

    \b
    Example(s):
    >>> caspy eval exp(pi)+3/sin(6)
    >>> caspy eval 3**x x 3
    """
    from .qt_assets.tabs.evaluate import EvaluateWorker

    default_params = ["1+1"]
    expression = tuple([expression])
    validate_input_dict = validate_inputs(kwargs, default_params, expression, "eval")
    if list(validate_input_dict.keys())[0] == "error":
        send_to_thread(validate_input_dict)
        return

    if len(vars_sub) % 2 != 0:
        print(
            "Variable substitution must consist of an even number of arguments, see 'eval --help' for more "
            "information"
        )
        return

    var_sub = ""
    for var, value in zip(vars_sub[::2], vars_sub[1::2]):
        var_sub += f"{var}: {value} "

    if kwargs["preview"]:
        prefix = "prev_"
        options = [kwargs["output_type"], kwargs["use_unicode"], kwargs["line_wrap"]]
    else:
        prefix = ""
        options = [
            kwargs["output_type"],
            kwargs["use_unicode"],
            kwargs["line_wrap"],
            kwargs["use_scientific"],
            kwargs["accuracy"],
        ]

    params_to_send = list_merge(default_params, list(expression))
    to_send = [
        prefix + "eval_exp",
        params_to_send + [var_sub] + options,
        kwargs["copy"],
    ]

    send_to_thread(to_send, EvaluateWorker)


@main.command(cls=EncloseNegative)
@click.argument("number", type=int)
@click.option(
    "-c",
    "--copy",
    type=click.IntRange(1, 3),
    help="Copies the answer. 1 for exact_ans, 2 for approx_ans, and 3 for a list of [exact_ans, "
    "approx_ans].",
)
def pf(number: int, **kwargs: dict) -> None:
    """Retreives the prime factors of an positive integer.

    Note: exact_ans stores factors as dict: '{2: 2, 3: 1, 31: 1}'
    while approx_ans stores factors as string: '(2**2)*(3**1)*(31**1)'

    \b
    Example(s):
    >>> caspy pf 372
    """
    from .qt_assets.tabs.pf import PfWorker

    to_send = ["calc_pf", [number], kwargs["copy"]]
    send_to_thread(to_send, PfWorker)


@main.command(cls=EncloseNegative)
@click.argument("website_index", type=int, required=False, metavar="{NUMBER | LIST}")
@click.option("--list-websites", "-l", is_flag=True, default=False)
def web(website_index: int, list_websites: bool, **kwargs: dict) -> None:
    """Choose a number from a list of usable maths websites and open it in default web browser or
    type '-l' for a list of websites and then enter a number. The website will be opened in the default browser.

    \b
    Example(s):
    >>> caspy web 4
    >>> caspy web -l
    """
    import json
    import pkg_resources

    with open(
        pkg_resources.resource_filename("caspy3", "data/websites.json"),
        "r",
        encoding="utf8",
    ) as json_f:
        json_data = json_f.read()
        web_list = json.loads(json_data)

    if website_index:
        if website_index < 1 or website_index > len(web_list):
            print(f"Index of website must be between 1 and {len(web_list)}")
            return

    if list_websites:
        for web, i in zip(web_list, range(len(web_list))):
            print(f"{i + 1}. {next(iter(web))}")

    else:
        import webbrowser

        url = next(iter(web_list[website_index - 1].values()))
        webbrowser.open(url)


def send_to_thread(input_list: list, worker: ty.Type[BaseWorker]) -> None:
    def excepthook(exc_type, exc_value, exc_tb) -> None:
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        print("error catched!:")
        print("error message:\n", tb)

    sys.excepthook = excepthook
    app = QApplication(sys.argv)

    try:
        worker_thread = Cli(input_list[0], input_list[1], input_list[2], worker)
        worker_thread.call_worker()
    except KeyError:
        print("Invalid number of arguments")
        sys.exit()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
