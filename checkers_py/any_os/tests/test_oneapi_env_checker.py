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
import platform
import sys

from checkers_py.any_os import oneapi_env_checker
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../'))

import unittest  # noqa: E402
from unittest.mock import patch  # noqa: E402

from modules.check import CheckSummary, CheckMetadataPy  # noqa: E402


class TestOneapiEnvCheckerApiTest(unittest.TestCase):

    @patch("checkers_py.any_os.oneapi_env_checker.get_versions_of_oneapi_products_installed_in_env")
    @patch("checkers_py.any_os.oneapi_env_checker.check_if_env_is_configured")
    def test_run_positive(self, mocked_check_if_env_is_configured,
                          mocked_get_versions_of_oneapi_products_installed_in_env):
        expected = CheckSummary
        mocked_check_if_env_is_configured.return_value = {
            "Presence of oneAPI environment": {
                "CheckResult": "",
                "CheckStatus": "PASS"
            }}
        mocked_get_versions_of_oneapi_products_installed_in_env.return_value = {
            "Check": {
                "CheckResult": "some data",
                "CheckStatus": "INFO"
            }
        }

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


class TestGetVersionsOfOneapiProductsInstalledInEnv(unittest.TestCase):

    @patch("checkers_py.any_os.oneapi_env_checker.get_json_content_from_file", return_value={})
    @patch("checkers_py.any_os.oneapi_env_checker.is_new_layout", return_value=False)
    def test_get_versions_of_oneapi_products_installed_in_env_empty_map_negative(self,
                                                                                 mocked_is_new_layout,
                                                                                 mocked_get_json_content_from_file):  # noqa:E501
        expected_value = {
            "oneAPI products installed in the environment": {
                "CheckResult": {},
                "CheckStatus": "ERROR",
                "Message": "oneAPI product names map is empty.",
                "HowToFix": "This error is unexpected. Please report the issue to "
                            "Diagnostics Utility for oneAPI repository: "
                            "https://github.com/intel/diagnostics-utility."
            }
        }

        real_value = oneapi_env_checker.get_versions_of_oneapi_products_installed_in_env()

        self.assertEqual(real_value, expected_value)

    @patch("checkers_py.any_os.oneapi_env_checker.get_json_content_from_file",
           side_effect=ValueError("Error"))
    @patch("checkers_py.any_os.oneapi_env_checker.is_new_layout", return_value=False)
    def test_get_versions_of_oneapi_products_installed_in_env_cannot_get_map_negative(self,
                                                                                      mocked_is_new_layout,
                                                                                      mocked_get_json_content):  # noqa:E501
        expected_value = {
            "oneAPI products installed in the environment": {
                "CheckResult": {},
                "CheckStatus": "ERROR",
                "Message": "Error",
                "HowToFix": "This error is unexpected. Please report the issue to "
                            "Diagnostics Utility for oneAPI repository: "
                            "https://github.com/intel/diagnostics-utility."
            }
        }

        real_value = oneapi_env_checker.get_versions_of_oneapi_products_installed_in_env()

        self.assertEqual(real_value, expected_value)

    @patch("checkers_py.any_os.oneapi_env_checker.get_json_content_from_file", return_value={"Long name": "Short name"})  # noqa: E501
    @patch("os.getenv", return_value=None)
    @patch("checkers_py.any_os.oneapi_env_checker.is_new_layout", return_value=False)
    def test_get_versions_of_oneapi_products_installed_in_env_cannot_get_env_negative(
            self,
            mocked_is_new_layout,
            mocked_getenv,
            mocked_get_json_content):
        expected_value = {
            "oneAPI products installed in the environment": {
                "CheckResult": {},
                "CheckStatus": "WARNING",
                "Message": "There are no oneAPI products found in the current environment."
            }
        }

        real_value = oneapi_env_checker.get_versions_of_oneapi_products_installed_in_env()

        self.assertEqual(real_value, expected_value)

    @patch("checkers_py.any_os.oneapi_env_checker.get_json_content_from_file", return_value={"Long compiler name": "compiler"})  # noqa: E501
    @patch("os.getenv", return_value="/opt/intel/oneapi/compiler/2021.4.0/linux/lib")
    @patch("checkers_py.any_os.oneapi_env_checker.is_new_layout", return_value=False)
    def test_get_versions_of_oneapi_products_installed_in_env_positive(
            self,
            mocked_is_new_layout,
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

        real_value = oneapi_env_checker.get_versions_of_oneapi_products_installed_in_env()

        self.assertEqual(real_value, expected_value)

    @patch("checkers_py.any_os.oneapi_env_checker.get_json_content_from_file", return_value={"Long compiler name": "compiler"})  # noqa: E501
    @patch("os.getenv")  # noqa: E501
    @patch("checkers_py.any_os.oneapi_env_checker.is_new_layout", return_value=False)
    def test_get_versions_of_oneapi_products_installed_in_env_several_versions_positive(
            self,
            mocked_is_new_layout,
            mocked_getenv,
            mocked_get_json_content):
        mocked_getenv.return_value = \
            "C:\\Program Files (x86)\\Intel\\oneAPI\\compiler\\2021.4.0\\windows\\lib" \
            ";C:\\Program Files (x86)\\Intel\\oneAPI\\compiler\\2021.3.0\\windows\\lib" if platform.system(
            ) == "Windows" else "/opt/intel/oneapi/compiler/2021.4.0/linux/lib:/opt/intel/oneapi/compiler/2021.3.0/linux/lib"  # noqa: E501
        expected_value = {
            "oneAPI products installed in the environment": {
                "CheckResult": {
                    "Long compiler name": {
                        "CheckResult": {
                            "Version": {
                                "CheckResult": "2021.3.0,2021.4.0",
                                "CheckStatus": "WARNING",
                                "Message": "Several versions of Long compiler name were found in the current environment."  # noqa: E501
                            }
                        },
                        "CheckStatus": "INFO"
                    }
                },
                "CheckStatus": "INFO"
            }
        }

        real_value = oneapi_env_checker.get_versions_of_oneapi_products_installed_in_env()

        self.assertEqual(real_value, expected_value)

    @patch("checkers_py.any_os.oneapi_env_checker.get_json_content_from_file", return_value={"Long compiler name": "compiler"})  # noqa: E501
    @patch("os.getenv", return_value="")
    @patch("checkers_py.any_os.oneapi_env_checker.is_new_layout", return_value=False)
    def test_get_versions_of_oneapi_products_installed_in_env_no_setuped_products_positive(
            self,
            mocked_is_new_layout,
            mocked_getenv,
            mocked_get_json_content_from_file):
        expected_value = {
            "oneAPI products installed in the environment": {
                "CheckResult": {},
                "CheckStatus": "WARNING",
                "Message": "There are no oneAPI products found in the current environment."
            }
        }

        real_value = oneapi_env_checker.get_versions_of_oneapi_products_installed_in_env()

        self.assertEqual(real_value, expected_value)

    @patch("checkers_py.any_os.oneapi_env_checker.is_new_layout", return_value=True)
    def test_get_versions_of_oneapi_products_installed_in_env_new_layout(self, mocked_is_new_layout):  # noqa:E501
        expected_value = {}
        real_value = oneapi_env_checker.get_versions_of_oneapi_products_installed_in_env()
        self.assertEqual(real_value, expected_value)


class TestCheckIfEnvIsConfigured(unittest.TestCase):
    @patch("os.getenv", return_value='1')
    def test_positive(self, mock):
        expected = {"Presence of oneAPI environment": {"CheckResult": "", "CheckStatus": "PASS"}}
        actual = oneapi_env_checker.check_if_env_is_configured()
        self.assertEqual(expected, actual)

    @patch("os.getenv", return_value=None)
    def test_negative(self, mock):
        default_setvars_location = "C:\\Program Files (x86)\\Intel\\oneAPI\\setvars.bat" if platform.system(
        ) == "Windows" else "/opt/intel/oneapi/setvars.sh"

        expected = {"Presence of oneAPI environment": {
            "CheckResult": "",
            "CheckStatus": "FAIL",
            "Message": "oneAPI environment not configured.",
            "HowToFix": f"Run the setvars script (default location is {default_setvars_location})"
        }}
        actual = oneapi_env_checker.check_if_env_is_configured()
        self.assertEqual(expected, actual)


class TestIsNewLayout(unittest.TestCase):

    @patch("os.path.exists", return_value=False)
    @patch("os.getenv", return_value='/opt/intel/oneapi/')
    def test_old_layout(self, mock_getenv, mock_path_exists):
        expected = False
        actual = oneapi_env_checker.is_new_layout()
        self.assertEqual(expected, actual)

    @patch("os.path.exists", return_value=True)
    @patch("os.getenv", return_value='/opt/intel/oneapi/')
    def test_new_layout(self, mock_getenv, mock_path_exists):
        expected = True
        actual = oneapi_env_checker.is_new_layout()
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.TestCase.maxDiff = None
    unittest.main()
