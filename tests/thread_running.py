from PyQt5.QtWidgets import QApplication
from base_tester import BaseTester


class ThreadRunningTester(BaseTester):
    def __init__(self):
        super().__init__()

    def test_running_thread(self):
        self.test_thread_is_running()

    @BaseTester.call_worker
    def test_thread_is_running(self):
        command = "is_running"
        params = ["does_run"]
        solution = {'running': 'does_run'}
        return command, params, solution

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    tester = ThreadRunningTester()
    tester.test_running_thread()
    sys.exit(app.exec_())
