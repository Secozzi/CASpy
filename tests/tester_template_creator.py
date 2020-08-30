"""
A script to auto-generate templates for tester
"""

# Path of worker
WORKER_PATH = "summation import SummationWorker"

# Name of the class generated
CLASS_NAME = "PrevSumTester"

# Name of function that call each test, every test is a function
HEAD_TEST = "test_sum_prev"

# Base name of each test, such as SUB_TEST_invalid_expr
SUB_TEST = "test_prev_sum"

# What function executed by worker
COMMAND = "prev_sum"

# Path of outputfile
OUTPUT_PATH = "tester_template_output.py"

# All test functions, separated by a new line. Type _ to make it equal SUB_TEST
test_functions = """
no_expression
invalid_expression
one_start
invalid_varaible
invalid_start
_
latex
normal
var
unicode
"""

# ------------------ CODE -> only change variables above ------------------

head = f"""from PyQt5.QtWidgets import QApplication

from .base_tester import BaseTester
from caspy3.qt_assets.tabs.{WORKER_PATH}


class {CLASS_NAME}(BaseTester):
    def __init__(self):
        super().__init__()\n\n"""

functions = test_functions.strip().split("\n")

test_caller = f"    def {HEAD_TEST}(self):\n"
for f in functions:
    if f != "_":
        test_caller += f"        self.{SUB_TEST}_{f}()\n"
    else:
        test_caller += f"        self.{SUB_TEST}()\n"

middle = "\n"
worker_name = WORKER_PATH.split("import")[1][1:]
for func in functions:
    sub_name = f"{SUB_TEST}_{func}" if func != "_" else SUB_TEST

    middle += f"    @BaseTester.call_worker({worker_name})\n"
    middle += f"    def {sub_name}(self):\n"
    middle += f'        command = "{COMMAND}"\n'
    middle += "        params = 0\n"
    middle += "        solution = 0\n"
    middle += "        return command, params, solution\n\n"

end = f"""\nif __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    tester = {CLASS_NAME}()
    tester.{HEAD_TEST}()
    sys.exit(app.exec_())\n"""

with open(f"{OUTPUT_PATH}", "w") as f:
    f.write(head + test_caller + middle + end)
