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
from unittest.mock import patch  # noqa: E402

from checkers_py.windows import base_system_checker  # noqa: E402
from modules.check import CheckSummary, CheckMetadataPy  # noqa: E402


class TestBaseSystemCheckerApiTest(unittest.TestCase):

    @patch("checkers_py.windows.base_system_checker.get_hostname")
    @patch("checkers_py.windows.base_system_checker.get_cpu_info")
    @patch("checkers_py.windows.base_system_checker.get_bios_information")
    @patch("checkers_py.windows.base_system_checker.get_uname")
    def test_run_positive(
            self,
            mocked_get_uname,
            mocked_get_bios_information,
            mocked_get_cpu_info,
            mocked_get_hostname):
        expected = CheckSummary

        mocked_get_hostname.side_effect = lambda node: node.update({
            "Check 1": {
                "CheckResult": "some data",
                "CheckStatus": "INFO"
            }
        })
        mocked_get_cpu_info.side_effect = lambda node: node.update({
            "Check 2": {
                "CheckResult": "some data",
                "CheckStatus": "INFO"
            }
        })
        mocked_get_bios_information.side_effect = lambda node: node.update({
            "Check 3": {
                "CheckResult": "some data",
                "CheckStatus": "INFO"
            }
        })
        mocked_get_uname.side_effect = lambda node: node.update({
            "Check 4": {
                "CheckResult": "some data",
                "CheckStatus": "INFO"
            }
        })

        actual = base_system_checker.run_base_check({})

        self.assertIsInstance(actual, expected)

    def test_get_api_version_returns_str(self):
        expected = str

        actual = base_system_checker.get_api_version()

        self.assertIsInstance(actual, expected)

    def test_get_check_list_returns_list_metadata(self):
        expected = CheckMetadataPy

        actual = base_system_checker.get_check_list()

        for metadata in actual:
            self.assertIsInstance(metadata, expected)


if __name__ == "__main__":
    unittest.main()
