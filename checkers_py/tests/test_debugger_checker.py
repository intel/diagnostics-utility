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

import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../'))

import unittest  # noqa: E402
from unittest.mock import MagicMock, patch  # noqa: E402

from checkers_py import debugger_checker  # noqa: E402
from checkers_py.common import debugger_helper as common_debugger  # noqa: E402
from modules.check import CheckSummary, CheckMetadataPy  # noqa: E402


class TestDebuggerCheckerApiTest(unittest.TestCase):

    @patch("checkers_py.common.debugger_helper.get_OS", return_value="Windows")
    @patch("checkers_py.debugger_checker.check_linux_kernel_version")
    def test_run_on_windows(
            self,
            mocked_check_linux_kernel_version,
            mocked_get_OS,
    ):
        expected = CheckSummary

        value = debugger_checker.run_debugger_check({})

        self.assertIsInstance(value, expected)

    @patch("shutil.which")
    @patch("checkers_py.common.debugger_helper.os.path.exists", return_value=True)
    @patch("checkers_py.common.debugger_helper.get_OS", return_value="Linux")
    @patch("checkers_py.debugger_checker.check_linux_kernel_version")
    def test_run_on_linux(
            self,
            mocked_check_linux_kernel_version,
            mocked_get_OS,
            mocked_path_exists,
            mocked_which,
    ):
        expected = CheckSummary

        gdb_base_dir = "/example/oneapi/debugger/gdb_dir"
        mocked_which.return_value = os.path.join(gdb_base_dir, "bin", "gdb-oneapi")

        value = debugger_checker.run_debugger_check({})

        self.assertIsInstance(value, expected)

    @patch("shutil.which")
    @patch("checkers_py.common.debugger_helper.os.path.exists", return_value=False)
    @patch("checkers_py.common.debugger_helper.get_OS", return_value="Linux")
    @patch("checkers_py.debugger_checker.check_linux_kernel_version")
    def test_missing_paths(
            self,
            mocked_check_linux_kernel_version,
            mocked_get_OS,
            mocked_path_exists,
            mocked_which,
    ):
        expected = CheckSummary

        gdb_base_dir = "/example/oneapi/debugger/gdb_dir"
        mocked_which.return_value = os.path.join(gdb_base_dir, "bin", "gdb-oneapi")

        value = debugger_checker.run_debugger_check({})

        self.assertIsInstance(value, expected)

    @patch("checkers_py.common.debugger_helper.os.path.exists", side_effect=Exception("failure"))
    @patch("checkers_py.debugger_checker.check_linux_kernel_version")
    def test_exception_on_checks(
            self,
            mocked_check_linux_kernel_version,
            mocked_get_OS):
        expected = CheckSummary

        value = debugger_checker.run_debugger_check({})

        self.assertIsInstance(value, expected)

    def test_get_api_version_returns_str(self):
        expected = str

        value = debugger_checker.get_api_version()

        self.assertIsInstance(value, expected)

    def test_get_check_list_returns_list_metadata(self):
        expected = CheckMetadataPy

        value = debugger_checker.get_check_list()

        for metadata in value:
            self.assertIsInstance(metadata, expected)


class TestDebuggerHelper(unittest.TestCase):

    gdb_base_dir = "/example/onepai/debugger/gdb_dir"

    @patch("platform.uname")
    def test_check_linux_kernel_version_positive(self, mocked_uname):
        expected = {
            "Linux kernel version": {
                "Value": "Supported",
                "RetVal": "PASS",
                "Command": "uname -r"
            }
        }

        mocked_uname.return_value = MagicMock()
        mocked_uname.return_value.release = "5.11.0"

        value = {}
        debugger_checker.check_linux_kernel_version(value)

        self.assertEqual(expected, value)

    @patch("platform.uname")
    def test_check_linux_kernel_version_kernel_less_than_4(self, mocked_uname):
        expected = {
            "Linux kernel version": {
                "Value": "Not supported",
                "RetVal": "FAIL",
                "Command": "uname -r",
                "Message": "This Linux kernel version is not supported."
            }
        }

        mocked_uname.return_value = MagicMock()
        mocked_uname.return_value.release = "3.11.0"

        value = {}
        debugger_checker.check_linux_kernel_version(value)

        self.assertEqual(expected, value)

    @patch("platform.uname")
    def test_check_linux_kernel_version_kernel_is_4_major_less_than_14(self, mocked_uname):
        expected = {
            "Linux kernel version": {
                "Value": "Not supported",
                "RetVal": "FAIL",
                "Command": "uname -r",
                "Message": "This Linux kernel version is not supported.",
            }
        }

        mocked_uname.return_value = MagicMock()
        mocked_uname.return_value.release = "4.11.0"

        value = {}
        debugger_checker.check_linux_kernel_version(value)

        self.assertEqual(expected, value)

    @patch("platform.uname")
    def test_check_linux_kernel_version_less_than_two_elements(self, mocked_uname):
        expected = {
            "Linux kernel version": {
                "Value": "Not supported",
                "RetVal": "FAIL",
                "Command": "uname -r",
                "Message": "This Linux kernel version is not supported.",
            }
        }

        mocked_uname.return_value = MagicMock()
        mocked_uname.return_value.release = "string"

        value = {}
        debugger_checker.check_linux_kernel_version(value)

        self.assertEqual(expected, value)

    @patch("platform.uname")
    def test_check_linux_kernel_version_string_not_int(self, mocked_uname):
        expected = {
            "Linux kernel version": {
                "Value": "Not supported",
                "RetVal": "FAIL",
                "Command": "uname -r",
                "Message": "This Linux kernel version is not supported.",
            }
        }

        mocked_uname.return_value = MagicMock()
        mocked_uname.return_value.release = "5.string"

        value = {}
        debugger_checker.check_linux_kernel_version(value)

        self.assertEqual(expected, value)

    @patch("shutil.which")
    def test_debugger_gdb_base_path(self, mocked_which):
        mocked_which.return_value = os.path.join(self.gdb_base_dir, "bin", "gdb-oneapi")
        gdb_base = common_debugger.get_gdb_base_dir()

        self.assertEqual(self.gdb_base_dir, gdb_base)

    @patch("shutil.which", return_value=None)
    def test_debugger_gdb_base_path_not_in_path(self, mocked_which):
        gdb_base = common_debugger.get_gdb_base_dir()

        self.assertEqual(None, gdb_base)

    @patch("os.path.exists", return_value=True)
    @patch("shutil.which")
    def test_check_file_does_exist(self, mocked_which, mocked_exists):
        mocked_which.return_value = os.path.join(self.gdb_base_dir, "bin", "gdb-oneapi")

        result = {}
        common_debugger.check_file_in_gdb_dir(result, "file_name", "component_name")
        result = result["component_name exist"]

        self.assertEqual("PASS", result["RetVal"])
        self.assertTrue("component_name" in result["Message"])
        mocked_exists.assert_called_with(os.path.join(self.gdb_base_dir, "file_name"))

    @patch("os.path.exists", return_value=False)
    @patch("shutil.which")
    def test_check_file_does_not_exist(self, mocked_which, mocked_exists):
        mocked_which.return_value = os.path.join(self.gdb_base_dir, "bin", "gdb-oneapi")

        result = {}
        common_debugger.check_file_in_gdb_dir(result, "file_name", "component_name")
        result = result["component_name exist"]

        self.assertEqual("FAIL", result["RetVal"])
        self.assertTrue("component_name" in result["Message"])
        mocked_exists.assert_called_with(os.path.join(self.gdb_base_dir, "file_name"))

    @patch("shutil.which", side_effect=Exception("test"))
    def test_check_file_does_throw(self, mocked_which):
        result = {}
        common_debugger.check_file_in_gdb_dir(result, "file_name", "component_name")
        result = result["component_name exist"]

        self.assertEqual("ERROR", result["RetVal"])
        self.assertTrue("component_name" in result["Message"])


if __name__ == '__main__':
    unittest.main()
