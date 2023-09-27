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

from checkers_py.linux import gcc_checker  # noqa: E402
from modules.check import CheckSummary, CheckMetadataPy  # noqa: E402


class TestGccCheckerApiTest(unittest.TestCase):

    @patch("checkers_py.linux.gcc_checker.gcc_check")
    def test_run_positive(self, mocked_gcc_check):
        expected = CheckSummary
        mocked_gcc_check.side_effect = lambda node: node.update({
            "Check": {
                "CheckResult": "gcc check data",
                "CheckStatus": "INFO"
            }
        })

        actual = gcc_checker.run_gcc_check({})

        self.assertIsInstance(actual, expected)

    def test_get_api_version_returns_str(self):
        expected = str

        actual = gcc_checker.get_api_version()

        self.assertIsInstance(actual, expected)

    def test_get_check_list_returns_list_metadata(self):
        expected = CheckMetadataPy

        check_list = gcc_checker.get_check_list()

        for metadata in check_list:
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
                "CheckStatus": "INFO",
                "CheckResult": "8.4.0"
            }
        }

        process = MagicMock()
        process.communicate.return_value = (self.gcc_output, None)
        process.returncode = 0

        mocked_open.return_value = process

        actual = {}
        gcc_checker.get_gcc_version(actual)

        self.assertEqual(actual, expected)

    @patch("subprocess.Popen", side_effect=Exception("test message"))
    def test_get_gcc_version_popen_raise_exception(self, mocked_open):
        expected = {
            "GCC compiler version": {
                "Command": "gcc --version",
                "Message": "test message",
                "CheckStatus": "ERROR",
                "CheckResult": "Undefined",
                "HowToFix": "This error is unexpected. Please report the issue to "
                            "Diagnostics Utility for Intel® oneAPI Toolkits repository: "
                            "https://github.com/intel/diagnostics-utility."
            }
        }

        actual = {}
        gcc_checker.get_gcc_version(actual)

        self.assertEqual(actual, expected)

    @patch("subprocess.Popen")
    def test_get_gcc_version_return_code_is_not_zero(self, mocked_open):
        expected = {
            "GCC compiler version": {
                "Command": "gcc --version",
                "Message": "Cannot get information about GCC compiler version.",
                "CheckStatus": "ERROR",
                "CheckResult": "Undefined",
                "HowToFix": "This error is unexpected. Please report the issue to "
                            "Diagnostics Utility for Intel® oneAPI Toolkits repository: "
                            "https://github.com/intel/diagnostics-utility."
            }
        }

        process = MagicMock()
        process.communicate.return_value = (self.gcc_output, None)
        process.returncode = 1

        mocked_open.return_value = process

        actual = {}
        gcc_checker.get_gcc_version(actual)

        self.assertEqual(actual, expected)


class TestGetGccLocation(unittest.TestCase):

    def setUp(self):
        self.gcc_output = "/usr/bin/gcc\n"

    @patch("subprocess.Popen")
    def test_get_gcc_location_positive(self, mocked_open):
        expected = {
            "GCC compiler location": {
                "Command": "which gcc",
                "CheckStatus": "INFO",
                "CheckResult": "/usr/bin/gcc"
            }
        }

        process = MagicMock()
        process.communicate.return_value = (self.gcc_output, None)
        process.returncode = 0

        mocked_open.return_value = process

        actual = {}
        gcc_checker.get_gcc_location(actual)

        self.assertEqual(actual, expected)

    @patch("subprocess.Popen", side_effect=Exception("test message"))
    def test_get_gcc_location_popen_raise_exception(self, mocked_open):
        expected = {
            "GCC compiler location": {
                "Command": "which gcc",
                "Message": "test message",
                "CheckStatus": "ERROR",
                "CheckResult": "Undefined",
                "HowToFix": "This error is unexpected. Please report the issue to "
                            "Diagnostics Utility for Intel® oneAPI Toolkits repository: "
                            "https://github.com/intel/diagnostics-utility."
            }
        }

        actual = {}
        gcc_checker.get_gcc_location(actual)

        self.assertEqual(actual, expected)

    @patch("subprocess.Popen")
    def test_get_gcc_location_return_code_is_not_zero(self, mocked_open):
        expected = {
            "GCC compiler location": {
                "Command": "which gcc",
                "Message": "Cannot get information about GCC compiler location",
                "CheckStatus": "ERROR",
                "CheckResult": "Undefined",
                "HowToFix": "This error is unexpected. Please report the issue to "
                            "Diagnostics Utility for Intel® oneAPI Toolkits repository: "
                            "https://github.com/intel/diagnostics-utility."
            }
        }

        process = MagicMock()
        process.communicate.return_value = (self.gcc_output, None)
        process.returncode = 1

        mocked_open.return_value = process

        actual = {}
        gcc_checker.get_gcc_location(actual)

        self.assertEqual(actual, expected)


class TestGetLibGccLocation(unittest.TestCase):

    def setUp(self):
        self.libgcc_output = "/usr/lib/gcc/x86_64-linux-gnu/9/libgcc.a\n"

    @patch("subprocess.Popen")
    def test_get_libgcc_location_positive(self, mocked_open):
        expected = {
            "GCC companion library location": {
                "Command": "gcc -print-libgcc-file-name",
                "CheckStatus": "INFO",
                "CheckResult": "/usr/lib/gcc/x86_64-linux-gnu/9/libgcc.a"
            }
        }

        process = MagicMock()
        process.communicate.return_value = (self.libgcc_output, None)
        process.returncode = 0

        mocked_open.return_value = process

        actual = {}
        gcc_checker.get_libgcc_location(actual)

        self.assertEqual(actual, expected)

    @patch("subprocess.Popen", side_effect=Exception("test message"))
    def test_get_gcc_location_popen_raise_exception(self, mocked_open):
        expected = {
            "GCC companion library location": {
                "Command": "gcc -print-libgcc-file-name",
                "Message": "test message",
                "CheckStatus": "ERROR",
                "CheckResult": "Undefined",
                "HowToFix": "This error is unexpected. Please report the issue to "
                            "Diagnostics Utility for Intel® oneAPI Toolkits repository: "
                            "https://github.com/intel/diagnostics-utility."
            }
        }

        actual = {}
        gcc_checker.get_libgcc_location(actual)

        self.assertEqual(actual, expected)

    @patch("subprocess.Popen")
    def test_get_libgcc_location_return_code_is_not_zero(self, mocked_open):
        expected = {
            "GCC companion library location": {
                "Command": "gcc -print-libgcc-file-name",
                "Message": "Cannot get information about the GCC companion library location",
                "CheckStatus": "ERROR",
                "CheckResult": "Undefined",
                "HowToFix": "This error is unexpected. Please report the issue to "
                            "Diagnostics Utility for Intel® oneAPI Toolkits repository: "
                            "https://github.com/intel/diagnostics-utility."
            }
        }

        process = MagicMock()
        process.communicate.return_value = (self.libgcc_output, None)
        process.returncode = 1

        mocked_open.return_value = process

        actual = {}
        gcc_checker.get_libgcc_location(actual)

        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.TestCase.maxDiff = None
    unittest.main()
