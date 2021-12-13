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

from modules.check.check_list import CheckList  # noqa: E402

c_metadata = Mock()
c_metadata.name = "c_example".encode()
c_metadata.type = "Data".encode()
c_metadata.tags = "cpu".encode()
c_metadata.descr = "This is example of c module".encode()
c_metadata.dataReq = "{}".encode()
c_metadata.rights = "".encode()
c_metadata.timeout = 1
c_metadata.version = "0.5".encode()

c_api_version = "0.1".encode()

c_run_output = Mock()
c_run_output.error_code = 0
c_run_output.result = """{"Value": {"C example check": {"Value": "C example value"}}}""".encode()


c_run = Mock()
c_run.return_value = c_run_output

c_check = Mock()
c_check.metadata = c_metadata
c_check.run = c_run


class TestClassCheckList(unittest.TestCase):

    @patch("modules.check.check_list.CheckList._load_c_checker_lib")
    def setUp(self, mock_load):
        mock_lib = Mock()
        mock_lib.get_api_version.return_value = c_api_version

        mock_pointer = Mock()
        mock_pointer.contents = c_check
        mock_pointer_list = [mock_pointer, None]
        mock_lib.get_check_list.return_value = mock_pointer_list

        mock_load.return_value = mock_lib

        self.check_list = CheckList("test.so")

    @patch("modules.check.check_list.ctypes.CDLL", return_value=Mock())
    def test_load_checker_lib_correct(self, mock_cdll):
        value = CheckList._load_c_checker_lib("test.so")

        self.assertTrue(hasattr(value, "get_check_list"))
        self.assertTrue(hasattr(value, "get_api_version"))

    @patch("logging.error")
    @patch("modules.check.check_list.ctypes.CDLL", side_effect=Exception)
    def test_load_checker_lib_negative(self, mock_log, mock_cdll):
        self.assertRaises(Exception, CheckList._load_c_checker_lib, "test.so")

    def test_get_check_list_from_pointers_correct(self):
        mock_pointer = Mock()
        mock_pointer.contents = c_check
        mock_pointer_list = [mock_pointer, None]

        expected = [c_check]

        value = CheckList._get_check_list_from_pointers(mock_pointer_list)

        self.assertEqual(expected, value)

    def test_len_correct(self):
        expected = 1

        value = len(self.check_list)

        self.assertEqual(expected, value)

    def test_str_correct(self):
        expected = "CheckList(test.so)"

        value = str(self.check_list)

        self.assertEqual(expected, value)

    def test_getitem_correct_get_one_value(self):
        expected = c_check

        value = self.check_list[0]

        self.assertEqual(expected, value)

    def test_getitem_not_supports_slices(self):
        with self.assertRaises(Exception):
            self.check_list[:]


if __name__ == '__main__':
    unittest.main()
