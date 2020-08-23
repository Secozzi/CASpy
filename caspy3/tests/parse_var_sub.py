from PyQt5.QtWidgets import QApplication
from base_tester import BaseTester


class ParseVarSubTester(BaseTester):
    def __init__(self):
        super().__init__()

    def test_var_sub_parse(self):
        self.test_parse_var_sub_no_colon()
        self.test_parse_var_sub_no_value()
        self.test_parse_var_sub_no_value_multiple()
        self.test_parse_var_sub()

    @BaseTester.call_worker
    def test_parse_var_sub_no_colon(self):
        command = "parse_var_sub"
        params = ["x"]
        solution = {'error': 'Colon missing'}
        return command, params, solution

    @BaseTester.call_worker
    def test_parse_var_sub_no_value(self):
        command = "parse_var_sub"
        params = ["x: "]
        solution = {'error': "Variable 'x' is missing a value"}
        return command, params, solution

    @BaseTester.call_worker
    def test_parse_var_sub_no_value_multiple(self):
        command = "parse_var_sub"
        params = ["x: 2 y: "]
        solution = {'error': "Variable 'y' is missing a value"}
        return command, params, solution

    @BaseTester.call_worker
    def test_parse_var_sub(self):
        command = "parse_var_sub"
        params = ["x: 3 y: 5"]
        solution = {'x': '3', 'y': '5'}
        return command, params, solution


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    tester = ParseVarSubTester()
    tester.test_var_sub_parse()
    sys.exit(app.exec_())
