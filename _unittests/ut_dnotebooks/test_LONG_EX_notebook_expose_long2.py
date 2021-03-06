# -*- coding: utf-8 -*-
"""
@brief      test log(time=702s)
"""

import sys
import os
import unittest
from pyquickhelper.loghelper import fLOG, noLOG
from pyquickhelper.pycode import get_temp_folder, add_missing_development_version


try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src


class TestNotebookRunnerExposeLong2(unittest.TestCase):

    def setUp(self):
        fLOG("add missing dependencies", OutputPrint=__name__ == "__main__")
        add_missing_development_version(["pymyinstall", "pyensae", "pymmails"],
                                        __file__, hide=True)

    def test_notebook_runner_exposelong2(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        from src.ensae_teaching_cs.automation.notebook_test_helper import ls_notebooks, execute_notebooks, clean_function_1a
        temp = get_temp_folder(__file__, "temp_notebookexposelong2_")
        keepnote = ls_notebooks("expose")
        execute_notebooks(temp, keepnote, (lambda i, n: "paris_parcours" in n),
                          fLOG=fLOG, deepfLOG=fLOG if __name__ == "__main__" else noLOG,
                          clean_function=clean_function_1a, dump=src.ensae_teaching_cs)


if __name__ == "__main__":
    unittest.main()
