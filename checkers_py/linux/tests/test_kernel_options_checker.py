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
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../"))

import unittest  # noqa: E402
from unittest.mock import MagicMock, patch  # noqa: E402

from checkers_py.linux import kernel_options_checker  # noqa: E402
from modules.check import CheckSummary, CheckMetadataPy  # noqa: E402


class TestKernelBootOptionsCheckerApiTest(unittest.TestCase):

    @patch("checkers_py.linux.kernel_options_checker.get_kernel_settings")
    @patch("checkers_py.linux.kernel_options_checker.get_kernel_boot_options")
    def test_run_positive(self, mocked_get_kernel_boot_options, mocked_get_kernel_settings):
        expected = CheckSummary

        mocked_get_kernel_settings.side_effect = lambda node: node.update({
            "Check 1": {
                "CheckResult": "some data",
                "CheckStatus": "INFO"
            }
        })
        mocked_get_kernel_boot_options.side_effect = lambda node: node.update({
            "Check 2": {
                "CheckResult": "some data",
                "CheckStatus": "INFO"
            }
        })

        actual = kernel_options_checker.run_kernel_check({})

        self.assertIsInstance(actual, expected)

    def test_get_api_version_returns_str(self):
        expected = str

        actual = kernel_options_checker.get_api_version()

        self.assertIsInstance(actual, expected)

    def test_get_check_list_returns_list_metadata(self):
        expected = CheckMetadataPy

        check_list = kernel_options_checker.get_check_list()

        for metadata in check_list:
            self.assertIsInstance(metadata, expected)


class TestCheckPerfStreamParanoid(unittest.TestCase):

    @patch("subprocess.Popen")
    def test_check_perf_stream_paranoid_positive(self, mocked_open):
        expected = {"Perf stream paranoid": {
            "Command": "sysctl -n dev.i915.perf_stream_paranoid",
            "CheckStatus": "INFO",
            "CheckResult": "0"
        }}

        process = MagicMock()
        process.communicate.return_value = ("0", None)
        process.returncode = 0

        mocked_open.return_value = process

        actual = {}
        kernel_options_checker._check_perf_stream_paranoid(actual)

        self.assertEqual(actual, expected)

    @patch("subprocess.Popen", side_effect=Exception("test message"))
    def test_check_perf_stream_paranoid_popen_raise_exception(self, mocked_open):
        expected = {"Perf stream paranoid": {
            "Command": "sysctl -n dev.i915.perf_stream_paranoid",
            "Message": "test message",
            "CheckStatus": "ERROR",
            "CheckResult": "Undefined",
            "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."  # noqa E501
        }}

        actual = {}
        kernel_options_checker._check_perf_stream_paranoid(actual)

        self.assertEqual(actual, expected)

    @patch("subprocess.Popen")
    def test_check_perf_stream_paranoid_return_code_1(self, mocked_open):
        expected = {"Perf stream paranoid": {
            "Command": "sysctl -n dev.i915.perf_stream_paranoid",
            "Message": "Cannot get information about operating sysctl option",
            "CheckStatus": "ERROR",
            "CheckResult": "Undefined",
            "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."  # noqa E501
        }}

        process = MagicMock()
        process.communicate.return_value = ("0", None)
        process.returncode = 1

        mocked_open.return_value = process

        actual = {}
        kernel_options_checker._check_perf_stream_paranoid(actual)

        self.assertEqual(actual, expected)


class TestGetKernelSettings(unittest.TestCase):

    @patch("checkers_py.linux.kernel_options_checker._check_perf_stream_paranoid")
    def test_get_kernel_settings_positive(self, mocked__check_perf_stream_paranoid):
        expected = {
            "Kernel settings": {
                "CheckResult": {
                    "Check 1": {"CheckResult": "some data", "CheckStatus": "INFO"}
                },
                "CheckStatus": "INFO"
            }
        }

        mocked__check_perf_stream_paranoid.side_effect = lambda node: node.update({
            "Check 1": {
                "CheckResult": "some data",
                "CheckStatus": "INFO"
            }
        })

        actual = {}
        kernel_options_checker.get_kernel_settings(actual)

        self.assertEqual(expected, actual)


class TestGetKernelBootOptions(unittest.TestCase):

    def setUp(self):
        self.proc_cmdline_output = \
            "BOOT_IMAGE=/boot/vmlinuz-5.11.0-34-generic " \
            "root=UUID=1bad49ce-1ba9-4855-a25d-2eb0713f51b8 " \
            "ro quiet splash vt.handoff=7"

    @patch("subprocess.Popen")
    def test_get_kernel_boot_options_positive(self, mocked_open):
        expected = {
            "Kernel boot options": {
                "CheckResult": {
                    "BOOT_IMAGE": {"CheckResult": "/boot/vmlinuz-5.11.0-34-generic", "CheckStatus": "INFO"},
                    "root": {"CheckResult": "UUID=1bad49ce-1ba9-4855-a25d-2eb0713f51b8", "CheckStatus": "INFO"},   # noqa: E501
                    "ro": {"CheckResult": "", "CheckStatus": "INFO"},
                    "quiet": {"CheckResult": "", "CheckStatus": "INFO"},
                    "splash": {"CheckResult": "", "CheckStatus": "INFO"},
                    "vt.handoff": {"CheckResult": "7", "CheckStatus": "INFO"}
                },
                "CheckStatus": "INFO",
                "Command": "cat /proc/cmdline"
            }
        }

        process = MagicMock()
        process.communicate.return_value = (self.proc_cmdline_output, None)
        process.returncode = 0

        mocked_open.return_value = process

        actual = {}
        kernel_options_checker.get_kernel_boot_options(actual)

        self.assertEqual(actual, expected)

    @patch("subprocess.Popen", side_effect=Exception("test message"))
    def test_get_kernel_boot_options_popen_raise_exception(self, mocked_open):
        expected = {
            "Kernel boot options": {
                "CheckResult": "Undefined",
                "Message": "test message",
                "CheckStatus": "ERROR",
                "Command": "cat /proc/cmdline",
                "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."  # noqa E501
            }
        }

        actual = {}
        kernel_options_checker.get_kernel_boot_options(actual)

        self.assertEqual(actual, expected)

    @patch("subprocess.Popen")
    def test_get_kernel_boot_options_return_code_is_not_zero(self, mocked_open):
        expected = {
            "Kernel boot options": {
                "CheckResult": "Undefined",
                "Message": "Cannot get information about kernel boot options",
                "CheckStatus": "ERROR",
                "Command": "cat /proc/cmdline",
                "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."  # noqa E501
            }
        }

        process = MagicMock()
        process.communicate.return_value = (self.proc_cmdline_output, None)
        process.returncode = 1

        mocked_open.return_value = process

        actual = {}
        kernel_options_checker.get_kernel_boot_options(actual)

        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.TestCase.maxDiff = None
    unittest.main()
