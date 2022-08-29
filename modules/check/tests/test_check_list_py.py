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

import unittest  # noqa: E402
from unittest.mock import Mock, patch  # noqa: E402
from pathlib import Path  # noqa: E402

from modules.check.check_list_py import CheckListPy  # noqa: E402
from modules.check.check import CheckMetadataPy  # noqa: E402


py_metadata = CheckMetadataPy(
    name='python_example',
    type='Data',
    tags='cpu',
    descr='This is example of python module',
    dataReq='{}',
    merit=0,
    timeout=1,
    version=1,
    run='run'
)

py_api_version = "0.1"


class TestClassCheckListPy(unittest.TestCase):

    @patch("builtins.__import__")
    def setUp(self, mock_load):
        mock_module = Mock()
        mock_module.get_api_version.return_value = py_api_version
        mock_module.get_check_list.return_value = [py_metadata]

        mock_load.return_value = mock_module

        self.check_list = CheckListPy(Path("test.py"))

    def test_len_correct(self):
        expected = 1

        value = len(self.check_list)

        self.assertEqual(expected, value)

    def test_str_correct(self):
        expected = "CheckListPy(test.py)"

        value = str(self.check_list)

        self.assertEqual(expected, value)

    def test_getitem_correct_get_one_value(self):
        expected = py_metadata

        value = self.check_list[0]

        self.assertEqual(expected, value)

    def test_getitem_not_supports_slices(self):
        with self.assertRaises(Exception):
            self.check_list[:]


if __name__ == '__main__':
    unittest.main()
