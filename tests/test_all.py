from PyQt5.QtWidgets import QApplication

from .calc_deriv import CalcDerivTester
from .calc_diff_eq import CalcDiffEqTester
from .calc_formula import CalcFormulaTester
from .calc_integ import CalcIntegTester
from .calc_limit import CalcLimitTester
from .calc_normal_eq import CalcNormalEqTester
from .calc_pf import CalcPfTester
from .calc_sum import CalcSumTester
from .calc_system_eq import CalcSystemEqTester
from .eval_exp import EvalExpTester
from .execute_code import ExecuteCodeTester
from .expand_exp import ExpandExpTester
from .parse_diff_text import ParseDiffTextTester
from .parse_var_sub import ParseVarSubTester
from .prev_deriv import PrevDerivTester
from .prev_diff_eq import PrevDiffEqTester
from .prev_eval_exp import PrevEvalExpTester
from .prev_expand_exp import PrevExpandExpTester
from .prev_formula import PrevFormulaTester
from .prev_integ import PrevIntegTester
from .prev_limit import PrevLimitTester
from .prev_normal_eq import PrevNormalEqTester
from .prev_simp_exp import PrevSimpExpTester
from .prev_sum import PrevSumTester
from .prev_system_eq import PrevSystemEqTester
from .scientific_notation import ScientificNotationTester
from .simp_exp import SimpExpTester
from .base_tester import BaseTester


class TestAll(
    CalcDerivTester,
    CalcDiffEqTester,
    CalcFormulaTester,
    CalcIntegTester,
    CalcLimitTester,
    CalcNormalEqTester,
    CalcPfTester,
    CalcSumTester,
    CalcSystemEqTester,
    EvalExpTester,
    ExecuteCodeTester,
    ExpandExpTester,
    ParseDiffTextTester,
    ParseVarSubTester,
    PrevDerivTester,
    PrevDiffEqTester,
    PrevEvalExpTester,
    PrevExpandExpTester,
    PrevFormulaTester,
    PrevIntegTester,
    PrevLimitTester,
    PrevNormalEqTester,
    PrevSimpExpTester,
    PrevSumTester,
    PrevSystemEqTester,
    ScientificNotationTester,
    SimpExpTester,
):
    def __init__(self):
        super(TestAll, self).__init__()

    def test_all(self):
        CalcDerivTester.test_deriv_calc(self)
        CalcDiffEqTester.test_diff_eq_calc(self)
        CalcFormulaTester.test_formula_calc(self)
        CalcIntegTester.test_integ_calc(self)
        CalcLimitTester.test_limit_calc(self)
        CalcNormalEqTester.test_normal_eq_calc(self)
        CalcPfTester.test_pf_calc(self)
        CalcSumTester.test_sum_calc(self)
        # CalcSystemEqTester.test_system_eq_calc(self)
        EvalExpTester.test_exp_eval(self)
        ExecuteCodeTester.test_code_execute(self)
        ExpandExpTester.test_exp_expand(self)
        ParseDiffTextTester.test_text_diff_parse(self)
        ParseVarSubTester.test_var_sub_parse(self)
        PrevDerivTester.test_deriv_prev(self)
        PrevDiffEqTester.test_diff_eq_prev(self)
        PrevEvalExpTester.test_exp_eval_prev(self)
        PrevExpandExpTester.test_exp_expand_prev(self)
        PrevFormulaTester.test_formula_prev(self)
        PrevIntegTester.test_integ_prev(self)
        PrevLimitTester.test_limit_prev(self)
        PrevNormalEqTester.test_normal_eq_prev(self)
        PrevSimpExpTester.test_exp_simp_prev(self)
        PrevSumTester.test_sum_prev(self)
        PrevSystemEqTester.test_system_eq_prev(self)
        ScientificNotationTester.test_scientific_notation(self)
        SimpExpTester.test_exp_simp(self)


if __name__ == "__main__":
    import sys

    sys._excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook

    app = QApplication(sys.argv)
    tester = TestAll()
    tester.test_all()
    sys.exit(app.exec_())
