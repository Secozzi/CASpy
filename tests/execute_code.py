from PyQt5.QtWidgets import QApplication
from base_tester import BaseTester


class ExecuteCodeTester(BaseTester):
    def __init__(self):
        super().__init__()

    def test_code_execute(self):
        self.test_execute_code()
        self.test_execute_code_namespace()
        self.test_execute_code_loop()

    @BaseTester.call_worker
    def test_execute_code(self):
        command = "execute_code"
        params = ['ok = 5;print(ok)', {}]
        solution = {'exec': ['5', 0]}
        return command, params, solution

    @BaseTester.call_worker
    def test_execute_code_namespace(self):
        command = "execute_code"
        params = ["ok", {"ok": 4}]
        solution = {'exec': ['4', 0]}
        return command, params, solution


    @BaseTester.call_worker
    def test_execute_code_loop(self):
        command = "execute_code"
        params = ['for i in range(5):\n\tprint(i**2)', {}]
        solution = {'exec': ['0\n1\n4\n9\n16', 0]}
        return command, params, solution

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    tester = ExecuteCodeTester()
    tester.test_code_execute()
    sys.exit(app.exec_())
