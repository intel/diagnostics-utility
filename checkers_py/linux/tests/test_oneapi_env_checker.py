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
from unittest.mock import patch  # noqa: E402

from checkers_py.linux import oneapi_env_checker  # noqa: E402
from modules.check import CheckSummary, CheckMetadataPy  # noqa: E402


class TestOneapiEnvCheckerApiTest(unittest.TestCase):

    @patch("checkers_py.linux.oneapi_env_checker.get_oneapi_env_versions")
    def test_run_positive(self, mocked_get_oneapi_env_versions):
        expected = CheckSummary

        mocked_get_oneapi_env_versions.side_effect = lambda node: node.update({
            "Check": {
                "CheckResult": "some data",
                "CheckStatus": "INFO"
            }
        })

        actual = oneapi_env_checker.run_oneapi_env_check({})

        self.assertIsInstance(actual, expected)

    def test_get_api_version_returns_str(self):
        expected = str

        actual = oneapi_env_checker.get_api_version()

        self.assertIsInstance(actual, expected)

    def test_get_check_list_returns_list_metadata(self):
        expected = CheckMetadataPy

        check_list = oneapi_env_checker.get_check_list()

        for metadata in check_list:
            self.assertIsInstance(metadata, expected)


class TestGetOneapiEnvVersions(unittest.TestCase):

    @patch("checkers_py.linux.oneapi_env_checker.get_json_content_from_file", return_value={})
    def test_get_oneapi_env_versions_empty_map_negative(self, mocked_get_json_content_from_file):
        expected_value = {
            "oneAPI products installed in the environment": {
                "CheckResult": {},
                "CheckStatus": "ERROR",
                "Message": "oneAPI product names map is empty.",
                "HowToFix": "This error is unexpected. Please report the issue to "
                            "Diagnostics Utility for Intel® oneAPI Toolkits repository: "
                            "https://github.com/intel/diagnostics-utility."
            }
        }

        real_value = {}
        oneapi_env_checker.get_oneapi_env_versions(real_value)

        self.assertEqual(real_value, expected_value)

    @patch("checkers_py.linux.oneapi_env_checker.get_json_content_from_file", side_effect=ValueError("Error"))
    def test_get_oneapi_env_versions_cannot_get_map_negative(self, mocked_get_json_content):
        expected_value = {
            "oneAPI products installed in the environment": {
                "CheckResult": {},
                "CheckStatus": "ERROR",
                "Message": "Error",
                "HowToFix": "This error is unexpected. Please report the issue to "
                            "Diagnostics Utility for Intel® oneAPI Toolkits repository: "
                            "https://github.com/intel/diagnostics-utility."
            }
        }

        real_value = {}
        oneapi_env_checker.get_oneapi_env_versions(real_value)

        self.assertEqual(real_value, expected_value)

    @patch("checkers_py.linux.oneapi_env_checker.get_json_content_from_file", return_value={"Long name": "Short name"})  # noqa: E501
    @patch("os.getenv", return_value=None)
    def test_get_oneapi_env_versions_cannot_get_env_negative(
            self,
            mocked_getenv,
            mocked_get_json_content):
        expected_value = {
            "oneAPI products installed in the environment": {
                "CheckResult": {},
                "CheckStatus": "WARNING",
                "Message": "There are no oneAPI products found in the current environment."
            }
        }

        real_value = {}
        oneapi_env_checker.get_oneapi_env_versions(real_value)

        self.assertEqual(real_value, expected_value)

    @patch("checkers_py.linux.oneapi_env_checker.get_json_content_from_file", return_value={"Long compiler name": "compiler"})  # noqa: E501
    @patch("os.getenv", return_value="/opt/intel/oneapi/compiler/2021.4.0/linux/lib")
    def test_get_oneapi_env_versions_positive(
            self,
            mocked_getenv,
            mocked_get_json_content):
        expected_value = {
            "oneAPI products installed in the environment": {
                "CheckResult": {
                    "Long compiler name": {
                        "CheckResult": {
                            "Version": {
                                "CheckResult": "2021.4.0",
                                "CheckStatus": "INFO"
                            }
                        },
                        "CheckStatus": "INFO"
                    }
                },
                "CheckStatus": "INFO"
            }
        }

        real_value = {}
        oneapi_env_checker.get_oneapi_env_versions(real_value)

        self.assertEqual(real_value, expected_value)

    @patch("checkers_py.linux.oneapi_env_checker.get_json_content_from_file", return_value={"Long compiler name": "compiler"})  # noqa: E501
    @patch("os.getenv", return_value="/opt/intel/oneapi/compiler/2021.4.0/linux/lib:/opt/intel/oneapi/compiler/2021.3.0/linux/lib")  # noqa: E501
    def test_get_oneapi_env_versions_several_versions_positive(
            self,
            mocked_getenv,
            mocked_get_json_content):
        expected_value = {
            "oneAPI products installed in the environment": {
                "CheckResult": {
                    "Long compiler name": {
                        "CheckResult": {
                            "Version": {
                                "CheckResult": "2021.3.0,2021.4.0",
                                "CheckStatus": "WARNING",
                                "Message": "Several versions of Long compiler name was found in the current environment."  # noqa: E501
                            }
                        },
                        "CheckStatus": "INFO"
                    }
                },
                "CheckStatus": "INFO"
            }
        }

        real_value = {}
        oneapi_env_checker.get_oneapi_env_versions(real_value)

        self.assertEqual(real_value, expected_value)

    @patch("checkers_py.linux.oneapi_env_checker.get_json_content_from_file", return_value={"Long compiler name": "compiler"})  # noqa: E501
    @patch("os.getenv", return_value="")
    def test_get_oneapi_env_versions_no_setuped_products_positive(
            self,
            mocked_getenv,
            mocked_get_json_content_from_file):
        expected_value = {
            "oneAPI products installed in the environment": {
                "CheckResult": {},
                "CheckStatus": "WARNING",
                "Message": "There are no oneAPI products found in the current environment."
            }
        }

        real_value = {}
        oneapi_env_checker.get_oneapi_env_versions(real_value)

        self.assertEqual(real_value, expected_value)


if __name__ == '__main__':
    unittest.TestCase.maxDiff = None
    unittest.main()
