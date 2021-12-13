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
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../'))

import json  # noqa: E402
import unittest  # noqa: E402
from unittest.mock import MagicMock, patch, call  # noqa: E402

from modules.check.check_runner import merge_dict, get_sub_dict, run_checks  # noqa: E402


class TestMergeDict(unittest.TestCase):

    def test_merge_checker_result_to_empty_dict(self):
        test_data = {"Value": {"Check": {"Value": "Data"}}}
        value = {}
        expected = test_data

        merge_dict(value, test_data)

        self.assertEqual(expected, value)

    def test_merge_checker_result_to_not_empty_dict(self):
        test_data = {"Value": {"OtherCheck": {"Value": "OtherData"}}}
        value = {"Value": {"Check": {"Value": "Data"}}}
        expected = {"Value": {"Check": {"Value": "Data"}, "OtherCheck": {"Value": "OtherData"}}}

        merge_dict(value, test_data)

        self.assertEqual(expected, value)

    @patch("logging.debug")
    def test_rewrite_exist_checker_info_in_dst_dict(self, mock_debug):
        test_data = {"Value": {"Check": {"Value": "NewData"}}}
        value = {"Value": {"Check": {"Value": "OldData"}}}
        expected = {"Value": {"Check": {"Value": "NewData"}}}

        merge_dict(value, test_data)

        self.assertEqual(expected, value)
        mock_debug.assert_called_once()


class TestGetSubDict(unittest.TestCase):

    def test_get_empty_subdict(self):
        test_data = {"Value": {"Check": {"Value": "Data"}}}
        test_subdict = {}
        expected = 0

        value = get_sub_dict(test_data, test_subdict)

        self.assertEqual(expected, value)

    def test_get_subdict_from_empty_dict(self):
        test_subdict = {"Check": {}}
        expected = 1

        value = get_sub_dict({}, test_subdict)

        self.assertEqual(expected, value)

    def test_get_subdict_from_first_try_one_value(self):
        test_data = {"Value": {"Check": {"Value": "Data"}}}
        test_subdict = {"Check": {}}
        expected_return_code = 0
        expected_value = {"Check": {"Value": "Data"}}

        value = get_sub_dict(test_data, test_subdict)

        self.assertEqual(expected_value, test_subdict)
        self.assertEqual(expected_return_code, value)

    def test_get_subdict_from_first_try_two_value(self):
        test_data = {"Value": {"Check1": {"Value": "Data1"},
                               "Check2": {"Value": "Data2"},
                               "Check3": {"Value": "Data3"}}}
        test_subdict = {"Check1": {}, "Check3": {}}
        expected_return_code = 0
        expected_value = {"Check1": {"Value": "Data1"}, "Check3": {"Value": "Data3"}}

        value = get_sub_dict(test_data, test_subdict)

        self.assertEqual(expected_value, test_subdict)
        self.assertEqual(expected_return_code, value)

    def test_get_subdict_from_second_try_one_value(self):
        test_data = {"Value": {"TopLevelCheck": {"Value": {"Check": {"Value": "Data"}}}}}
        test_subdict = {"TopLevelCheck": {"Check": {}}}
        expected_return_code = 0
        expected_value = {"TopLevelCheck": {"Check": {"Value": "Data"}}}

        value = get_sub_dict(test_data, test_subdict)

        self.assertEqual(expected_value, test_subdict)
        self.assertEqual(expected_return_code, value)

    def test_get_subdict_from_second_try_two_value(self):
        test_data = {"Value": {"TopLevelCheck": {"Value": {"Check1": {"Value": "Data1"},
                                                           "Check2": {"Value": "Data2"},
                                                           "Check3": {"Value": "Data3"}}}}}
        test_subdict = {"TopLevelCheck": {"Check1": {}, "Check3": {}}}
        expected_return_code = 0
        expected_value = {"TopLevelCheck": {"Check1": {"Value": "Data1"}, "Check3": {"Value": "Data3"}}}

        value = get_sub_dict(test_data, test_subdict)

        self.assertEqual(expected_value, test_subdict)
        self.assertEqual(expected_return_code, value)

    def test_get_wrong_subdict_returns_error_code(self):
        test_data = {"Value": {"Check": {"Value": "Data"}}}
        test_subdict = {"Check": "Value"}
        expected_return_code = 1

        value = get_sub_dict(test_data, test_subdict)

        self.assertEqual(expected_return_code, value)

    def test_get_subdict_from_wrong_dict_returns_error_code(self):
        test_data = {"Value": {"Check": "Value"}}
        test_subdict = {"Check": {}}
        expected_return_code = 1

        value = get_sub_dict(test_data, test_subdict)

        self.assertEqual(expected_return_code, value)


class TestRunChecks(unittest.TestCase):

    @patch("builtins.exit")
    @patch("builtins.print")
    def test_run_checks_no_checks_to_run(self, mocked_print, mocked_exit):
        expected_exit_code = 1

        run_checks([])

        mocked_print.assert_called_once()
        mocked_exit.assert_called_once_with(expected_exit_code)

    @patch("builtins.exit", side_effect=Exception())
    @patch("builtins.print")
    def test_run_checks_does_not_have_dependency(self, mocked_print, mocked_exit):
        expected_exit_code = 1

        mocked_check = MagicMock()
        mocked_check.get_metadata.return_value = MagicMock()
        mocked_check.get_metadata.return_value.name = "check"
        mocked_check.get_metadata.return_value.rights = "user"
        mocked_check.get_metadata.return_value.dataReq = """{"data": {}}"""
        mocked_check.get_summary.return_value = None

        self.assertRaises(Exception, run_checks, [mocked_check])

        mocked_exit.assert_called_once_with(expected_exit_code)
        mocked_print.assert_called_once()

    @patch("os.stat")
    @patch("os.getuid", return_value=1000)
    @patch("logging.warning")
    def test_run_checks_run_admin_check_without_root_rights(self, mocked_log, mocked_getuid, mocked_stat):
        mocked_stat.return_value = MagicMock()
        mocked_stat.return_value.st_mode = 16387
        mocked_summary = MagicMock()
        mocked_summary.result = "{}"
        mocked_check = MagicMock()
        mocked_check.get_metadata.return_value = MagicMock()
        mocked_check.get_metadata.return_value.name = "check"
        mocked_check.get_metadata.return_value.rights = "admin"
        mocked_check.get_metadata.return_value.dataReq = "{}"
        mocked_check.get_summary.side_effect = [None, mocked_summary]

        run_checks([mocked_check])

        mocked_getuid.assert_called_once()
        mocked_log.assert_called_once()

    @patch("os.stat")
    @patch("os.getuid", return_value=0)
    @patch("modules.check.check_runner.timeout_exit")
    def test_run_checks_run_user_check_with_root_rights(self, mocked_timeout, mocked_getuid, mocked_stat):
        mocked_stat.return_value = MagicMock()
        mocked_stat.return_value.st_mode = 16387
        mocked_summary = MagicMock()
        mocked_summary.result = "{}"
        mocked_check = MagicMock()
        mocked_check.get_metadata.return_value = MagicMock()
        mocked_check.get_metadata.return_value.name = "check"
        mocked_check.get_metadata.return_value.rights = "user"
        mocked_check.get_metadata.return_value.dataReq = "{}"
        mocked_check.get_summary.side_effect = [None, mocked_summary]

        run_checks([mocked_check])

        mocked_timeout.assert_called_once_with(mocked_check.run)

    @patch("os.stat")
    @patch("os.getuid", return_value=1000)
    @patch("modules.check.check_runner.timeout_exit")
    def test_run_checks_run_user_check_without_root_rights(self, mocked_timeout, mocked_getuid, mocked_stat):
        mocked_stat.return_value = MagicMock()
        mocked_stat.return_value.st_mode = 16387
        mocked_summary = MagicMock()
        mocked_summary.result = "{}"
        mocked_check = MagicMock()
        mocked_check.get_metadata.return_value = MagicMock()
        mocked_check.get_metadata.return_value.name = "check"
        mocked_check.get_metadata.return_value.rights = "user"
        mocked_check.get_metadata.return_value.dataReq = "{}"
        mocked_check.get_summary.side_effect = [None, mocked_summary]

        run_checks([mocked_check])

        mocked_timeout.assert_called_once_with(mocked_check.run)

    @patch("os.stat")
    @patch("os.getuid", return_value=1000)
    @patch("logging.warning")
    def test_run_checks_run_user_check_without_shm_access(self, mocked_log, mocked_getuid, mocked_stat):
        mocked_stat.return_value = MagicMock()
        mocked_stat.return_value.st_mode = 16388
        mocked_summary = MagicMock()
        mocked_summary.result = "{}"
        mocked_check = MagicMock()
        mocked_check.get_metadata.return_value = MagicMock()
        mocked_check.get_metadata.return_value.name = "check"
        mocked_check.get_metadata.return_value.rights = "user"
        mocked_check.get_metadata.return_value.dataReq = "{}"
        mocked_check.get_summary.side_effect = [None, mocked_summary]

        run_checks([mocked_check])

        mocked_check.run.assert_called_once_with({})
        mocked_log.assert_called_once()

    @patch("os.stat")
    @patch("os.getuid", return_value=1000)
    @patch("modules.check.check_runner.timeout_exit")
    def test_run_checks_run_two_dependencies_checks(self,  mocked_timeout, mocked_getuid, mocked_stat):
        mocked_stat.return_value = MagicMock()
        mocked_stat.return_value.st_mode = 16387
        mocked_summary_1 = MagicMock()
        mocked_summary_1.result = "{}"
        mocked_check_1 = MagicMock()
        mocked_check_1.get_metadata.return_value = MagicMock()
        mocked_check_1.get_metadata.return_value.name = "check_1"
        mocked_check_1.get_metadata.return_value.rights = "user"
        mocked_check_1.get_metadata.return_value.dataReq = """{"Check 2": {}}"""
        mocked_check_1.get_summary.side_effect = [None, None, mocked_summary_1]

        mocked_summary_2 = MagicMock()
        mocked_summary_2.result = json.dumps({
            "Value": {
                "Check 2": {
                    "Value": "Check 2 Value",
                    "RetVal": "INFO"
                }
            }
        })
        mocked_check_2 = MagicMock()
        mocked_check_2.get_metadata.return_value = MagicMock()
        mocked_check_2.get_metadata.return_value.name = "check_2"
        mocked_check_2.get_metadata.return_value.rights = "user"
        mocked_check_2.get_metadata.return_value.dataReq = "{}"
        mocked_check_2.get_summary.side_effect = [None, mocked_summary_2, mocked_summary_2]

        run_checks([mocked_check_1, mocked_check_2])

        expected_calls = [
            call(mocked_check_2.run),
            call()(mocked_check_2, {}),
            call(mocked_check_1.run),
            call()(mocked_check_1, {"Check 2": {"Value": "Check 2 Value", "RetVal": "INFO"}})
        ]
        mocked_timeout.assert_has_calls(expected_calls)

    @patch("os.stat")
    @patch("os.getuid", return_value=1000)
    @patch("modules.check.check_runner.timeout_exit")
    def test_run_checks_run_two_separate_checks(self, mocked_timeout, mocked_getuid, mocked_stat):
        mocked_stat.return_value = MagicMock()
        mocked_stat.return_value.st_mode = 16387
        mocked_summary = MagicMock()
        mocked_summary.result = "{}"
        mocked_check_1 = MagicMock()
        mocked_check_1.get_metadata.return_value = MagicMock()
        mocked_check_1.get_metadata.return_value.name = "check_1"
        mocked_check_1.get_metadata.return_value.rights = "user"
        mocked_check_1.get_metadata.return_value.dataReq = "{}"
        mocked_check_1.get_summary.side_effect = [None, mocked_summary]

        mocked_check_2 = MagicMock()
        mocked_check_2.get_metadata.return_value = MagicMock()
        mocked_check_2.get_metadata.return_value.name = "check_2"
        mocked_check_2.get_metadata.return_value.rights = "user"
        mocked_check_2.get_metadata.return_value.dataReq = "{}"
        mocked_check_2.get_summary.side_effect = [None, mocked_summary]

        run_checks([mocked_check_1, mocked_check_2])

        expected_calls = [
            call(mocked_check_1.run),
            call()(mocked_check_1, {}),
            call(mocked_check_2.run),
            call()(mocked_check_2, {})
        ]
        mocked_timeout.assert_has_calls(expected_calls)


if __name__ == '__main__':
    unittest.main()
