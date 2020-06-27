import os
import sys
import traceback
from pathlib import Path

import click
from pyperclip import copy
from PyQt5.QtCore import QObject, QThreadPool
from PyQt5.QtWidgets import QApplication

# need to set the correct cwd
CURRENT_DIR = Path(__file__).parent
sys.path.insert(0, str(CURRENT_DIR))
os.chdir(CURRENT_DIR)

from Worker import CASWorker

class Cli(QObject):
    def __init__(self, command, params, copy, parent=None):
        super(Cli, self).__init__(parent)

        self.command = command
        self.params = params
        self.copy = copy

    def stop_thread(self):
        pass

    def start_thread(self):
        self.threadpool = QThreadPool()

    def call_worker(self):
        """
        Call worker, send command and params, and then start thread
        """
        self.WorkerCAS = CASWorker(self.command, self.params, self.copy)
        self.WorkerCAS.signals.output.connect(self.print_output)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.threadpool.start(self.WorkerCAS)

    def print_output(self, input_dict):
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

# Default flags, these flags are added to a command by using the decorator '@add_options(DEFAULT_FLAGS)'.
DEFAULT_FLAGS = [
    click.option("--preview", "-p", is_flag=True, default=False, help="Preview instead of calculating"),
    click.option("--output-type", "-o", default = 1,type=click.IntRange(1,3), help="Select output type, 1 for pretty; 2 for latex and 3 for normal"),
    click.option("--use-unicode", "-u", is_flag=True, default=False, help="Use unicode for symbols"),
    click.option("--line-wrap", "-l", is_flag=True, default=False, help="Use line wrap on answer")
]

# Default argument(s), these argument(s) are added to a command by using the decorator '@add_options(DEFAULT_ARGUMENTS)'.
DEFAULT_ARGUMENTS = [
    click.option("--use-scientific", "-s", type=int, help="Notate approximate answer with scientific notation, argument is accuracy"),
    click.option("--accuracy", "-a", type=int, default=10, help="Accuracy of evaluation")
]

# Flag used only by equation, added to command by using the decorator '@add_options(EQ_FLAGS)'.
EQ_FLAGS = [
    click.option("--solve-type", "-st", is_flag=True, default=False, help="Solves an equation with either solve or solveset (see SymPy solve vs solveset). Default is solve, set flag to solve with solveset.")
]

def list_merge(default_params, input_params):
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
        if input_params[i] != None:
            output_list.append(input_params[i])
        else:
            output_list.append(default_params[i])

    return output_list

def validate_inputs(input_kwargs, default_params, input_params, name):
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
    :param name:
        Name of the command
    :return:
        Returns either error along with message if validation failed, or True along with 'pass' if validation passed
    """

    if input_kwargs["output_type"] not in range(1,4):
        return{"error": "Output type must be integer between 1 and 3 inclusive. 1 for pretty; 2 for latex and 3 for normal."}

    if len(input_params) > len(default_params):
        return{"error": f"'{name}' commad doesn't take more than {len(default_params)} parameters."}

    if len(input_params) == 0:
        return({"error": f"'{name}' command requires at least one parameter."})

    return({True: "pass"})

def add_options(options):
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
def main(**kwargs):
    pass

@main.command()
def start():
    """
    Start the GUI
    """
    from qt_gui import main
    main()

@main.command()
@add_options(DEFAULT_FLAGS)
@add_options(DEFAULT_ARGUMENTS)
@click.argument("params", nargs=-1)
@click.option("-c", "--copy", type=click.IntRange(1,3), help="Copies the answer. 0 for exact_ans and 1 for approx_ans and 2 for a list of [exact_ans, approx_ans].")
def deriv(params, **kwargs):
    """
    Calculate the derivative.

    Usage:
        deriv *expression *variable order at_point
        * = required
    Example:
        caspy deriv sin(1/ok) ok 3 pi
    """
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
        options = [kwargs["output_type"], kwargs["use_unicode"], kwargs["line_wrap"], kwargs["use_scientific"], kwargs["accuracy"]]

    params_to_send = list_merge(default_params, list(params))

    to_send = [prefix+"deriv", params_to_send+options, kwargs["copy"]]
    send_to_thread(to_send)

@main.command()
@add_options(DEFAULT_FLAGS)
@add_options(DEFAULT_ARGUMENTS)
@click.argument("params", nargs=-1)
@click.option("-c", "--copy", type=click.IntRange(1,3), help="Copies the answer. 0 for exact_ans and 1 for approx_ans and 2 for a list of [exact_ans, approx_ans].")
def integ(params, **kwargs):
    """
    Calculate the integral.

    Usage:
        integ *expression *variable lower_bound upper_bound
        * = required
    Example:
        integ 1/sqrt(1-x**2) x (-1) 1
    """
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
        options = [kwargs["output_type"], kwargs["use_unicode"], kwargs["line_wrap"], kwargs["use_scientific"], kwargs["accuracy"]]

    params_to_send = list_merge(default_params, list(params))

    to_send = [prefix + "integ", params_to_send + options, kwargs["copy"]]
    send_to_thread(to_send)

@main.command()
@add_options(DEFAULT_FLAGS)
@add_options(DEFAULT_ARGUMENTS)
@click.argument("params", nargs=-1)
@click.option("-c", "--copy", type=click.IntRange(1,3), help="Copies the answer. 0 for exact_ans and 1 for approx_ans and 2 for a list of [exact_ans, approx_ans].")
def limit(params, **kwargs):
    """
    Calculate the limit of an expression.

    Usage:
        limit *expression *variable *as_variable_is_approaching side
        * = required
        Both sides as default, + for right side and - for left side
    Example:
        limit u!**(1/u) u 0 -
    """
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
        options = [kwargs["output_type"], kwargs["use_unicode"], kwargs["line_wrap"], kwargs["use_scientific"], kwargs["accuracy"]]

    params_to_send = list_merge(default_params, list(params))

    to_send = [prefix + "limit", params_to_send + options, kwargs["copy"]]
    send_to_thread(to_send)

@main.command()
@add_options(DEFAULT_FLAGS)
@add_options(DEFAULT_ARGUMENTS)
@add_options(EQ_FLAGS)
@click.argument("params", nargs=-1)
@click.option("-c", "--copy", type=click.IntRange(1,3), help="Copies the answer. 0 for exact_ans and 1 for approx_ans and 2 for a list of [exact_ans, approx_ans].")
def eq(params, **kwargs):
    """
    Solve an equation.

    Usage:
        eq *left_expression *right_expression *variable_to_solve_for solve_type
        * = required
        Use '--solve-type' or '-st' flag to solve equation with SymPy solve, set flag for solveset
    Examples:
        eq x**x 2 x
        eq sin(x) 1 x -st
    """
    default_params = ["x", 0, "x"]

    validate_input_dict = validate_inputs(kwargs, default_params, params, "eq")
    if list(validate_input_dict.keys())[0] == "error":
        send_to_thread(validate_input_dict)
        return

    if kwargs["preview"]:
        prefix = "prev_"
        options = [None, kwargs["output_type"], kwargs["use_unicode"], kwargs["line_wrap"], True]
    else:
        prefix = "calc_"
        options = [kwargs["solve_type"], kwargs["output_type"], kwargs["use_unicode"], kwargs["line_wrap"], kwargs["use_scientific"], kwargs["accuracy"]]

    params_to_send = list_merge(default_params, list(params))

    to_send = [prefix + "eq", params_to_send + options, kwargs["copy"]]
    send_to_thread(to_send)

@main.command()
@add_options(DEFAULT_FLAGS)
@click.argument("expression")
@click.option("-c", "--copy", type=click.IntRange(1,3), help="Copies the answer. 0 for exact_ans and 1 for approx_ans and 2 for a list of [exact_ans, approx_ans].")
def simp(expression, **kwargs):
    """
    Simplifies an expression.

    Usage:
        simp *expression
        * = required
    Example:
        simp sin(x)**2+cos(x)**2
    """
    # validate_inputs() expects a tuple as input
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
    to_send = [prefix + "simp_eq", params_to_send + options, kwargs["copy"]]
    send_to_thread(to_send)

@main.command()
@add_options(DEFAULT_FLAGS)
@click.argument("expression")
@click.option("-c", "--copy", type=click.IntRange(1,3), help="Copies the answer. 0 for exact_ans and 1 for approx_ans and 2 for a list of [exact_ans, approx_ans].")
def exp(expression, **kwargs):
    """
    Expandes an expression.

    Usage:
        exp *expression
        * = required
    Example:
        exp (a+b-c)**3
    """
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
    to_send = [prefix + "exp_eq", params_to_send + options, kwargs["copy"]]
    send_to_thread(to_send)

@main.command()
@add_options(DEFAULT_FLAGS)
@add_options(DEFAULT_ARGUMENTS)
@click.argument("expression")
@click.argument("vars", required=False, nargs=-1)
@click.option("-c", "--copy", type=click.IntRange(1,3), help="Copies the answer. 0 for exact_ans and 1 for approx_ans and 2 for a list of [exact_ans, approx_ans].")
def eval(expression, vars, **kwargs):
    """
    Evaluates an expression.

    Usage:
        eval *expression
        * = required
    Example:
        eval exp(pi)+3/sin(6)
    """
    default_params = ["1+1"]
    expression = tuple([expression])
    validate_input_dict = validate_inputs(kwargs, default_params, expression, "eval")
    if list(validate_input_dict.keys())[0] == "error":
        send_to_thread(validate_input_dict)
        return

    if kwargs["preview"]:
        prefix = "prev_"
        options = [kwargs["output_type"], kwargs["use_unicode"], kwargs["line_wrap"]]
    else:
        prefix = ""
        options = [kwargs["output_type"], kwargs["use_unicode"], kwargs["line_wrap"], kwargs["use_scientific"], kwargs["accuracy"]]

    params_to_send = list_merge(default_params, list(expression))
    to_send = [prefix + "eval_exp", params_to_send + options, kwargs["copy"]]
    send_to_thread(to_send)

@main.command()
@click.argument("number")
@click.option("-c", "--copy", type=click.IntRange(1,3), help="Copies the answer. 0 for exact_ans and 1 for approx_ans and 2 for a list of [exact_ans, approx_ans].")
def pf(number, **kwargs):
    """
    Retreives the prime factors of an positive integer.

    Usage:
        pf *number
        * = required
    Example:
        pf 372

    Note: exact_ans stores factors as dict: '{2: 2, 3: 1, 31: 1}' while approx_ans stores factors as string: '(2**2)*(3**1)*(31**1)'
    """
    to_send = ["calc_pf", [number], kwargs["copy"]]
    send_to_thread(to_send)

    click.echo(f"calculating limit with {number}")

@main.command()
@click.argument("website_index", type=int, required=False)
@click.option("--list", "-l", is_flag=True)
def web(website_index, list):
    """
    Choose a number from a list of usable maths websites. type '-l' for a list of websites and enter a number. The website will be opened in the default browser.

    Usage:
        web number
    Example:
        web 4
        web -l
    """

    import json
    with open("../assets/formulas.json", "r", encoding="utf8") as json_f:
        json_data = json_f.read()
        web_list = json.loads(json_data)[2]

    if website_index:
        if website_index < 1 or website_index > len(web_list):
            print(f"Index of website must be between 1 and {len(web_list)}")
            return

    if list:
        for web, i in zip(web_list, range(len(web_list))):
            print(f"{i+1}. {next(iter(web))}")

    else:
        import webbrowser
        url = next(iter(web_list[website_index-1].values()))
        webbrowser.open(url)

def send_to_thread(input_list):
    def excepthook(exc_type, exc_value, exc_tb):
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        print("error catched!:")
        print("error message:\n", tb)
    sys.excepthook = excepthook
    app = QApplication(sys.argv)

    try:
        worker_thread = Cli(input_list[0], input_list[1], input_list[2])
        worker_thread.start_thread()
        worker_thread.call_worker()
    except KeyError:
        print("Invalid number of arguments")
        sys.exit()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    #app = QApplication(sys.argv)
    #
    #worker_thread = Cli('calc_deriv', ['x**x', 'x', '1', None, 2, False, False, None])
    #worker_thread.start_thread()
    #worker_thread.call_worker()
    #
    #sys.exit(app.exec())
