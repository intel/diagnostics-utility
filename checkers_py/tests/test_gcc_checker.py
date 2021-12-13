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
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../'))

import unittest  # noqa: E402
from unittest.mock import MagicMock, patch  # noqa: E402

from checkers_py import gcc_checker  # noqa: E402
from modules.check import CheckSummary, CheckMetadataPy  # noqa: E402


class TestGccCheckerApiTest(unittest.TestCase):

    @patch("checkers_py.gcc_checker.get_gcc_version")
    def test_run_positive(self, mocked_get_gcc_version):
        expected = CheckSummary

        mocked_get_gcc_version.side_effect = lambda node: node.update({
            "Check": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })

        value = gcc_checker.run_gcc_check({})

        self.assertIsInstance(value, expected)

    def test_get_api_version_returns_str(self):
        expected = str

        value = gcc_checker.get_api_version()

        self.assertIsInstance(value, expected)

    def test_get_check_list_returns_list_metadata(self):
        expected = CheckMetadataPy

        value = gcc_checker.get_check_list()

        for metadata in value:
            self.assertIsInstance(metadata, expected)


class TestGetGccVersion(unittest.TestCase):

    def setUp(self):
        self.gcc_output = \
            "gcc (Ubuntu 8.4.0-3ubuntu2) 8.4.0\n" \
            "Copyright (C) 2018 Free Software Foundation, Inc.\n" \
            "This is free software; see the source for copying conditions.  There is NO\n" \
            "warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.\n"

    @patch("subprocess.Popen")
    def test_get_gcc_version_positive(self, mocked_open):
        expected = {
            "GCC compiler version": {
                "Command": "gcc --version",
                "RetVal": "INFO",
                "Value": "8.4.0"
            }
        }

        process = MagicMock()
        process.communicate.return_value = (self.gcc_output, None)
        process.returncode = 0

        mocked_open.return_value = process

        value = {}
        gcc_checker.get_gcc_version(value)

        self.assertEqual(value, expected)

    @patch("subprocess.Popen", side_effect=Exception("test message"))
    def test_get_gcc_version_popen_raise_exception(self, mocked_open):
        expected = {
            "GCC compiler version": {
                "Command": "gcc --version",
                "Message": "test message",
                "RetVal": "ERROR",
                "Value": "Undefined"
            }
        }

        value = {}
        gcc_checker.get_gcc_version(value)

        self.assertEqual(value, expected)

    @patch("subprocess.Popen")
    def test_get_gcc_version_return_code_is_not_zero(self, mocked_open):
        expected = {
            "GCC compiler version": {
                "Command": "gcc --version",
                "Message": "Cannot get information about GCC compiler version",
                "RetVal": "ERROR",
                "Value": "Undefined"
            }
        }

        process = MagicMock()
        process.communicate.return_value = (self.gcc_output, None)
        process.returncode = 1

        mocked_open.return_value = process

        value = {}
        gcc_checker.get_gcc_version(value)

        self.assertEqual(value, expected)


if __name__ == '__main__':
    unittest.main()
