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

from checkers_py import kernel_boot_options_checker  # noqa: E402
from modules.check import CheckSummary, CheckMetadataPy  # noqa: E402


class TestKernelBootOptionsCheckerApiTest(unittest.TestCase):

    @patch("checkers_py.kernel_boot_options_checker.get_kernel_boot_options")
    def test_run_positive(self, mocked_get_kernel_boot_options):
        expected = CheckSummary

        mocked_get_kernel_boot_options.side_effect = lambda node: node.update({
            "Check": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })

        value = kernel_boot_options_checker.run_kernel_boot_options_check({})

        self.assertIsInstance(value, expected)

    def test_get_api_version_returns_str(self):
        expected = str

        value = kernel_boot_options_checker.get_api_version()

        self.assertIsInstance(value, expected)

    def test_get_check_list_returns_list_metadata(self):
        expected = CheckMetadataPy

        value = kernel_boot_options_checker.get_check_list()

        for metadata in value:
            self.assertIsInstance(metadata, expected)


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
                "Value": {
                    "BOOT_IMAGE": {"Value": "/boot/vmlinuz-5.11.0-34-generic", "RetVal": "INFO"},
                    "root": {"Value": "UUID=1bad49ce-1ba9-4855-a25d-2eb0713f51b8", "RetVal": "INFO"},
                    "ro": {"Value": "", "RetVal": "INFO"},
                    "quiet": {"Value": "", "RetVal": "INFO"},
                    "splash": {"Value": "", "RetVal": "INFO"},
                    "vt.handoff": {"Value": "7", "RetVal": "INFO"}
                },
                "RetVal": "INFO",
                "Command": "cat /proc/cmdline"
            }
        }

        process = MagicMock()
        process.communicate.return_value = (self.proc_cmdline_output, None)
        process.returncode = 0

        mocked_open.return_value = process

        value = {}
        kernel_boot_options_checker.get_kernel_boot_options(value)

        self.assertEqual(value, expected)

    @patch("subprocess.Popen", side_effect=Exception("test message"))
    def test_get_kernel_boot_options_popen_raise_exception(self, mocked_open):
        expected = {
            "Kernel boot options": {
                "Value": "Undefined",
                "Message": "test message",
                "RetVal": "ERROR",
                "Command": "cat /proc/cmdline"
            }
        }

        value = {}
        kernel_boot_options_checker.get_kernel_boot_options(value)

        self.assertEqual(value, expected)

    @patch("subprocess.Popen")
    def test_get_kernel_boot_options_return_code_is_not_zero(self, mocked_open):
        expected = {
            "Kernel boot options": {
                "Value": "Undefined",
                "Message": "Cannot get information about kernel boot options",
                "RetVal": "ERROR",
                "Command": "cat /proc/cmdline"
            }
        }

        process = MagicMock()
        process.communicate.return_value = (self.proc_cmdline_output, None)
        process.returncode = 1

        mocked_open.return_value = process

        value = {}
        kernel_boot_options_checker.get_kernel_boot_options(value)

        self.assertEqual(value, expected)


if __name__ == '__main__':
    unittest.main()
