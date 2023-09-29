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

from checkers_py.linux import user_group_checker  # noqa: E402
from modules.check import CheckSummary, CheckMetadataPy  # noqa: E402


class TestUserGroupCheckerApiTest(unittest.TestCase):

    @patch("os.getuid", return_value=0)
    def test_run_positive_root_user(self, mocked_os_getuid):
        expected = CheckSummary

        actual = user_group_checker.run_user_group_check({})

        mocked_os_getuid.assert_called_once()
        self.assertIsInstance(actual, expected)

    @patch("os.getuid", return_value=1000)
    @patch("checkers_py.linux.user_group_checker.are_intel_gpus_found", return_value=False)
    def test_run_positive_without_gpu(self, mocked_are_intel_gpus_found, mocked_os_getuid):
        expected = CheckSummary

        actual = user_group_checker.run_user_group_check({})

        mocked_os_getuid.assert_called_once()
        mocked_are_intel_gpus_found.assert_called_once()
        self.assertIsInstance(actual, expected)

    @patch("os.getuid", return_value=1000)
    @patch("checkers_py.linux.user_group_checker.check_user_in_required_groups")
    @patch("checkers_py.linux.user_group_checker.are_intel_gpus_found", return_value=True)
    def test_run_positive_with_gpu(
            self,
            mocked_are_intel_gpus_found,
            mocked_check_user_in_required_groups,
            mocked_os_getuid):
        expected = CheckSummary

        mocked_check_user_in_required_groups.side_effect = lambda node: node.update({
            "Check": {
                "CheckResult": "some data",
                "CheckStatus": "INFO"
            }
        })

        actual = user_group_checker.run_user_group_check({})

        mocked_os_getuid.assert_called_once()
        mocked_are_intel_gpus_found.assert_called_once()
        self.assertIsInstance(actual, expected)

    def test_get_api_version_returns_str(self):
        expected = str

        actual = user_group_checker.get_api_version()

        self.assertIsInstance(actual, expected)

    def test_get_check_list_returns_list_metadata(self):
        expected = CheckMetadataPy

        actual = user_group_checker.get_check_list()

        for metadata in actual:
            self.assertIsInstance(metadata, expected)


class TestCheckUserInRequiredGroups(unittest.TestCase):

    def test__get_required_groups_positive(self):
        expected = set(["test1", "test2"])

        mock_path_1 = MagicMock()
        mock_path_1.group.return_value = "test1"
        mock_path_2 = MagicMock()
        mock_path_2.group.return_value = "test2"

        actual = user_group_checker._get_required_groups([mock_path_1, mock_path_2])

        self.assertEqual(expected, actual)

    @patch("grp.getgrall")
    def test__get_user_groups_positive(self, mocked_getgrall):
        expected = ["test_group"]
        mock_group_1 = MagicMock()
        mock_group_1.gr_name = "test_group"
        mock_group_1.gr_mem = ["test_user"]
        mock_group_2 = MagicMock()
        mock_group_2.gr_name = "another_test_group"
        mock_group_2.gr_mem = ["another_user"]
        mocked_getgrall.return_value = [mock_group_1, mock_group_2]

        actual = user_group_checker._get_user_groups("test_user")

        self.assertEqual(expected, actual)

    @patch("getpass.getuser", return_value="test_user")
    @patch("checkers_py.linux.user_group_checker.get_card_devices", return_value=["card"])
    @patch("checkers_py.linux.user_group_checker.get_render_devices", return_value=["render"])
    @patch("checkers_py.linux.user_group_checker._get_required_groups", return_value=["test1", "test2"])
    @patch("checkers_py.linux.user_group_checker._get_user_groups", return_value=["group", "test1", "test2"])
    def test_check_user_in_required_groups_user_is_in_required_groups(
            self,
            mocked__get_user_groups,
            mocked__get_required_groups,
            mocked_get_render_devices,
            mocked_get_card_devices,
            mocked_getuser):
        expected = {
            "Current user is in the test1 group": {
                "Command": "groups | grep test1",
                "CheckStatus": "PASS",
                "CheckResult": ""
            },
            "Current user is in the test2 group": {
                "Command": "groups | grep test2",
                "CheckStatus": "PASS",
                "CheckResult": ""
            },
        }

        actual = {}
        user_group_checker.check_user_in_required_groups(actual)

        self.assertEqual(expected, actual)

    @patch("getpass.getuser", return_value="test_user")
    @patch("checkers_py.linux.user_group_checker.get_card_devices", return_value=["card"])
    @patch("checkers_py.linux.user_group_checker.get_render_devices", return_value=["render"])
    @patch("checkers_py.linux.user_group_checker._get_required_groups", return_value=["test1", "test2"])
    @patch("checkers_py.linux.user_group_checker._get_user_groups", return_value=["group", "test1"])
    def test_check_user_in_required_groups_user_is_in_one_required_group_without_sudo(
            self,
            mocked__get_user_groups,
            mocked__get_required_groups,
            mocked_get_render_devices,
            mocked_get_card_devices,
            mocked_getuser):
        expected = {
            "Current user is in the test1 group": {
                "Command": "groups | grep test1",
                "CheckStatus": "PASS",
                "CheckResult": ""
            },
            "Current user is in the test2 group": {
                "Command": "groups | grep test2",
                "HowToFix": "Contact the system administrator to add current user to the test2 group.",
                "Message": "Current user is not part of the test2 group.",
                "CheckStatus": "FAIL",
                "CheckResult": ""
            },
        }

        actual = {}
        user_group_checker.check_user_in_required_groups(actual)

        self.assertEqual(expected, actual)

    @patch("getpass.getuser", return_value="test_user")
    @patch("checkers_py.linux.user_group_checker.get_card_devices", return_value=["card"])
    @patch("checkers_py.linux.user_group_checker.get_render_devices", return_value=["render"])
    @patch("checkers_py.linux.user_group_checker._get_required_groups", return_value=["test1", "test2"])
    @patch("checkers_py.linux.user_group_checker._get_user_groups", return_value=["group", "test1", "sudo"])
    def test_check_user_in_required_groups_user_is_in_one_required_group_with_sudo(
            self,
            mocked__get_user_groups,
            mocked__get_required_groups,
            mocked_get_render_devices,
            mocked_get_card_devices,
            mocked_getuser):
        expected = {
            "Current user is in the test1 group": {
                "Command": "groups | grep test1",
                "CheckStatus": "PASS",
                "CheckResult": ""
            },
            "Current user is in the test2 group": {
                "AutomationFix": "sudo usermod -a -G test2 test_user",
                "Command": "groups | grep test2",
                "HowToFix": "Add current user to the test2 group. "
                            "Then restart the terminal and try again.",
                "Message": "Current user is not part of the test2 group.",
                "CheckStatus": "FAIL",
                "CheckResult": ""
            },
        }

        actual = {}
        user_group_checker.check_user_in_required_groups(actual)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.TestCase.maxDiff = None
    unittest.main()
