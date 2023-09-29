#!/usr/bin/env python3
# /*******************************************************************************
# Copyright Intel Corporation.
# This software and the related documents are Intel copyrighted materials, and your use of them
# is governed by the express license under which they were provided to you (License).
# Unless the License provides otherwise, you may not use, modify, copy, publish, distribute, disclose
# or transmit this software or the related documents without Intel's prior written permission.
# This software and the related documents are provided as is, with no express or implied warranties,
# other than those that are expressly stated in the License.
#
# *******************************************************************************/

# NOTE: workaround to import modules
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../'))

import importlib  # noqa: E402
import unittest  # noqa: E402
from unittest.mock import MagicMock, patch  # noqa: E402

from modules.check.check import CheckMetadataPy, CheckSummary  # noqa: E402
from modules.check import check_py  # noqa: E402


py_metadata = CheckMetadataPy(
    name='python_example',
    type='Data',
    groups='cpu',
    descr='This is example of python module',
    dataReq='{}',
    merit=0,
    timeout=1,
    version=2,
    run='run'
)

py_api_version = "0.2"

py_check_result = CheckSummary(
    result="""{"CheckResult":
      {"Python example check":
        {"CheckResult": "Python example value",
          "CheckStatus": "PASS"}}}"""
)

test_filename = "test.py"

mocked_module = MagicMock()
mocked_module.get_api_version.return_value = py_api_version
mocked_module.run.return_value = py_check_result
mocked_module.get_check_list.return_value = [py_metadata]


py_check_list = MagicMock()
py_check_list.__iter__.return_value = [py_metadata]
py_check_list.api_version = py_api_version
py_check_list.checker_module = mocked_module


class TestClassCheckPy(unittest.TestCase):

    def setUp(self):
        importlib.reload(check_py)
        self.check = check_py.CheckPy(metadata=py_metadata, check_list=py_check_list)

    def tearDown(self):
        importlib.reload(check_py)

    def test_class_init_correct(self):
        expected = py_metadata

        actual = self.check.get_metadata()

        self.assertEqual(expected.__dict__, actual.__dict__)

    def test_get_api_version_positive_correct(self):
        expected = py_api_version

        actual = self.check.get_api_version()

        self.assertEqual(expected, actual)

    def test_get_summury_positive_correct(self):
        expected = py_check_result

        actual = self.check.run({})

        self.assertEqual(expected.__dict__, actual.__dict__)


class TestGetCheckerPy(unittest.TestCase):

    @patch("builtins.__import__", return_value=mocked_module)
    def test_get_checks_py_correct_with_correct_argument(self, mock_import):
        expected = py_metadata
        mocked_file = MagicMock()
        mocked_file.__str__.return_value = test_filename
        mocked_file.exists.return_value = True

        actual = check_py.getChecksPy(mocked_file, "0.2")[0].get_metadata()

        self.assertEqual(expected.__dict__, actual.__dict__)

    @patch("logging.error")
    def test_get_checks_py_raise_error_if_file_not_exist(self, mock_log):
        mocked_file = MagicMock()
        mocked_file.__str__.return_value = test_filename
        mocked_file.exists.return_value = False

        self.assertRaises(OSError, check_py.getChecksPy, mocked_file, "0.2")
        mock_log.assert_called()

    @patch("builtins.__import__", return_value=mocked_module)
    @patch("logging.error")
    def test_get_checks_py_raise_error_if_version_not_compatible(self, mock_log, mock_import):
        mocked_file = MagicMock()
        mocked_file.__str__.return_value = test_filename
        mocked_file.exists.return_value = True

        self.assertRaises(ValueError, check_py.getChecksPy, mocked_file, "0.3")
        mock_log.assert_called()


if __name__ == '__main__':
    unittest.TestCase.maxDiff = None
    unittest.main()
