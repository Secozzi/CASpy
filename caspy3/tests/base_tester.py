from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QThreadPool

from colored import fg, attr
import time


class BaseTester(QWidget):
    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)
        self.passed_tests = 0
        self.failed_tests = 0
        self.counter_threads = 0
        self.start_time = time.time()

    @staticmethod
    def call_worker(worker):
        def call_wrapper(func):
            def wrapper(self):
                command, params, solution = func(self)

                self.current_time = time.time()
                self.counter_threads += 1
                self.qworker = worker(command, params)
                self.qworker.signals.output.connect(lambda output:
                                                    self.test_output(output, solution, [command, params], func.__name__))
                self.qworker.signals.finished.connect(self.stop_thread)
                self.threadpool.start(self.qworker)
            return wrapper
        return call_wrapper

    def stop_thread(self):
        pass

    def test_output(self, input_dict, solution, input_list, test_name):
        """
        Compares input_dict with solution and prints info if it fails
        :param input_dict: dict
            Dictionary returned by the worker thread
        :param solution: dict
            Expected solution
        :param input_list: list
            Contains called command and params. First element = command (str), second element = list of params
        :param test_name: str
            Name of current test. Gets printed if it Passes
        """
        self.counter_threads -= 1

        input_dict_error_val = list(input_dict.values())[0][0]
        execution_time = str(time.time() - self.current_time)[0:5]
        self.current_time = time.time()

        print(f"Test '{test_name}' ... ", end="")

        if list(input_dict.keys())[0] == "exec":
            self.print_result({"exec": input_dict["exec"]}, solution, execution_time, test_name, input_list)
        else:

            if type(input_dict_error_val) == str:
                if input_dict_error_val[:17] == "Error: \nTraceback" and list(solution.values())[0][0] == "Error: \nTraceback":
                    print(f"{fg(2)}ok{attr(0)} {execution_time}s")
                    self.passed_tests += 1
                else:
                    self.print_result(input_dict, solution, execution_time, test_name, input_list)
            else:
                self.print_result(input_dict, solution, execution_time, test_name, input_list)

    def print_result(self, input_dict, solution, execution_time, test_name, input_list):
        if input_dict == solution:
            print(f"{fg(2)}ok{attr(0)} {execution_time}s")
            self.passed_tests += 1
        else:
            print(f"{fg(1)}FAIL{attr(0)} {execution_time}s")
            print("\n" + "="*50)
            print(f"\n{fg(1)} Test '{test_name}' failed with command '{input_list[0]}' "
                  f"and with params '{input_list[1]}'\n "
                  f"Expected output : {solution} \n Output          : {input_dict}{attr(0)}\n")
            print("="*50 + "\n")
            self.failed_tests += 1

        if self.counter_threads == 0:
            print("\n" + "-" * 30)
            print(f"Testing finished in {str(time.time() - self.start_time)[0:5]}s")
            if self.failed_tests == 0:
                print(f"{fg(2)}Failed tests: {self.failed_tests}{attr(0)}")
            else:
                print(f"{fg(1)}Failed tests: {self.failed_tests}{attr(0)}")
            print(f"Passed tests: {self.passed_tests}")
            print(f"Number of tests: {self.failed_tests + self.passed_tests}")
            QApplication.quit()
