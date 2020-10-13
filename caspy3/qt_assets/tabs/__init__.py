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

import json
import sys
import pkg_resources

from .derivative import DerivativeTab
from .equations import EquationsTab
from .evaluate import EvaluateTab
from .expand import ExpandTab
from .formulas import FormulaTab
from .integral import IntegralTab
from .limit import LimitTab
from .pf import PfTab
from .shell.shell import ShellTab
from .simplify import SimplifyTab
from .summation import SummationTab
from .web import WebTab

TABS = []


def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)


settings_json = pkg_resources.resource_filename('caspy3', 'data/settings.json')
with open(settings_json, "r", encoding="utf8") as json_f:
    tab_file = json_f.read()
    tab_data = json.loads(tab_file)["tabs"]

for tab in list(tab_data.keys()):
    if tab_data[tab]:
        TABS.append(str_to_class(tab))
