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

from checkers_py import advisor_checker  # noqa: E402
from checkers_py.common import advisor_vtune_helper as common_advisor_vtune  # noqa: E402
from modules.check import CheckSummary, CheckMetadataPy  # noqa: E402


class TestAdvisorCheckerApiTest(unittest.TestCase):

    @patch("checkers_py.common.advisor_vtune_helper.get_OS", return_value=common_advisor_vtune.LINUX)
    @patch("checkers_py.advisor_checker.check_linux_kernel_version")
    @patch("checkers_py.common.advisor_vtune_helper.check_perf_stream_paranoid")
    def test_run_on_linux(
            self,
            mocked_check_perf_stream_paranoid,
            mocked_check_linux_kernel_version,
            mocked_get_OS):
        expected = CheckSummary

        mocked_check_perf_stream_paranoid.side_effect = lambda node: node.update({
            "Check": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })

        value = advisor_checker.run_advisor_check({})

        self.assertIsInstance(value, expected)

    @patch("checkers_py.common.advisor_vtune_helper.get_OS", return_value=common_advisor_vtune.WINDOWS)
    def test_run_on_windows(self, mocked_get_OS):
        expected = CheckSummary

        value = advisor_checker.run_advisor_check({})

        self.assertIsInstance(value, expected)

    def test_get_api_version_returns_str(self):
        expected = str

        value = advisor_checker.get_api_version()

        self.assertIsInstance(value, expected)

    def test_get_check_list_returns_list_metadata(self):
        expected = CheckMetadataPy

        value = advisor_checker.get_check_list()

        for metadata in value:
            self.assertIsInstance(metadata, expected)


class TestCheckLinuxKernelVersion(unittest.TestCase):

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
        advisor_checker.check_linux_kernel_version(value)

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
        advisor_checker.check_linux_kernel_version(value)

        self.assertEqual(expected, value)

    @patch("platform.uname")
    def test_check_linux_kernel_version_kernel_is_4_major_less_than_14(self, mocked_uname):
        expected = {
            "Linux kernel version": {
                "Value": "Not supported",
                "RetVal": "FAIL",
                "Command": "uname -r",
                "Message": "This Linux kernel version is not supported."
            }
        }

        mocked_uname.return_value = MagicMock()
        mocked_uname.return_value.release = "4.11.0"

        value = {}
        advisor_checker.check_linux_kernel_version(value)

        self.assertEqual(expected, value)


if __name__ == '__main__':
    unittest.main()
