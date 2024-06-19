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

import platform

import unittest  # noqa: E402
from unittest.mock import patch  # noqa: E402

from checkers_py.windows import compiler_checker  # noqa: E402
from checkers_py.windows.common.termninal_helper import run_powershell_command
from modules.check import CheckSummary, CheckMetadataPy  # noqa: E402


@unittest.skipIf(platform.system(
) == "Linux", "run on windows only")
class TestCompilerCheckerApiTest(unittest.TestCase):

    @patch("checkers_py.windows.compiler_checker.get_msvc_compiler_info")
    def test_run_positive(self, mocked_get_msvc_compiler_info):
        expected = CheckSummary
        mocked_get_msvc_compiler_info.return_value = {
            "Check": {
                "CheckResult": "cl check data",
                "CheckStatus": "INFO"
            }
        }
        actual = compiler_checker.run_compiler_check({})
        self.assertIsInstance(actual, expected)

    def test_get_api_version_returns_str(self):
        expected = str
        actual = compiler_checker.get_api_version()
        self.assertIsInstance(actual, expected)

    def test_get_check_list_returns_list_metadata(self):
        expected = CheckMetadataPy
        check_list = compiler_checker.get_check_list()
        for metadata in check_list:
            self.assertIsInstance(metadata, expected)

    def test_run_powershell_command(self):
        expected = tuple
        check_list = run_powershell_command('cd')
        self.assertIsInstance(check_list, expected)


@unittest.skipIf(platform.system(
) == "Linux", "run on windows only")
class TestGetMsvcCompilerInfo(unittest.TestCase):

    @patch("checkers_py.windows.compiler_checker.get_msvc_compiler_version")
    def test_get_msvc_compiler_version_three_number_in_version(
            self, mocked_get_msvc_compiler_version):
        mocked_get_msvc_compiler_version.return_value = {
            "Version": {
                "CheckResult": "1.0.1",
                "CheckStatus": "INFO",
                "Command": "cl"}}
        expected = {
            "MSVC compiler": {
                "CheckResult": {
                    "Version": {
                        "CheckResult": "1.0.1",
                        "CheckStatus": "INFO",
                        "Command": "cl"}},
                "CheckStatus": "INFO"}}
        actual = compiler_checker.get_msvc_compiler_info()
        self.assertEqual(expected, actual)

    @patch("checkers_py.windows.compiler_checker.get_msvc_compiler_version")
    def test_get_msvc_compiler_version_four_number_in_version(
            self, mocked_get_msvc_compiler_version):
        mocked_get_msvc_compiler_version.return_value = {
            "Version": {
                "CheckResult": "1.0.1.0",
                "CheckStatus": "INFO",
                "Command": "cl"}}
        expected = {
            "MSVC compiler": {
                "CheckResult": {
                    "Version": {
                        "CheckResult": "1.0.1.0",
                        "CheckStatus": "INFO",
                        "Command": "cl"}},
                "CheckStatus": "INFO"}}
        actual = compiler_checker.get_msvc_compiler_info()
        self.assertEqual(expected, actual)


@unittest.skipIf(platform.system(
) == "Linux", "run on windows only")
class TestGetMsvcCompilerVersion(unittest.TestCase):

    @patch("checkers_py.windows.compiler_checker.run_powershell_command")
    def test_positive(self, mocked_run_powershell_command):
        mocked_run_powershell_command.return_value = ("йц^&*укеasdваda#$%^s  qweasd",
                                                      "bla bla bla 100.12.3 #$!@123zxc", 0)
        expected = {
            "Version": {
                "CheckResult": "100.12.3",
                "CheckStatus": "INFO",
                "Command": "cl"}
        }
        actual = compiler_checker.get_msvc_compiler_version()
        self.assertEqual(expected, actual)

    @patch("checkers_py.windows.compiler_checker.run_powershell_command")
    def test_run_powershell_command_return_code_not_zero(self, mocked_run_powershell_command):
        mocked_run_powershell_command.return_value = ("йц^&*укеasdваda#$%^s  qweasd",
                                                      "bla bla bla 100.12.3 #$!@123zxc", 1)
        expected = {
            "Version": {
                "CheckResult": "Undefined",
                "CheckStatus": "FAIL",
                "Command": "cl",
                "Message": "MSVC compiler not found.",
                "HowToFix": "Make sure the compiler is installed"
                " and present in the PATH environment variable"
            }
        }
        actual = compiler_checker.get_msvc_compiler_version()
        self.assertEqual(expected, actual)

    @patch("checkers_py.windows.compiler_checker.run_powershell_command")
    def test_run_powershell_command_throw_exception(self, mocked_run_powershell_command):
        mocked_run_powershell_command.side_effect = Exception("Oops")
        expected = {
            "Version": {
                "CheckResult": "Undefined",
                "CheckStatus": "ERROR",
                "Command": "cl",
                "Message": "Oops",
                "HowToFix": "This error is unexpected. Please report the issue to "
                "Diagnostics Utility for oneAPI repository: "
                "https://github.com/intel/diagnostics-utility."
            }
        }
        actual = compiler_checker.get_msvc_compiler_version()
        self.assertEqual(expected, actual)

    @patch("checkers_py.windows.compiler_checker.run_powershell_command")
    def test_failed_parse_version(self, mocked_run_powershell_command):
        mocked_run_powershell_command.return_value = ("йц^&*укеasdваda#$%^s  qweasd",
                                                      "bla bla bla#$!@123zxc", 0)
        expected = {
            "Version": {
                "CheckResult": "Undefined",
                "CheckStatus": "FAIL",
                "Command": "cl",
                "Message": "Failed to get compiler version."
            }
        }
        actual = compiler_checker.get_msvc_compiler_version()
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.TestCase.maxDiff = None
    unittest.main()
