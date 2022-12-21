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

from modules.check.check import CheckSummary
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../'))

import json  # noqa: E402
import time  # noqa: E402
import unittest  # noqa: E402
from unittest.mock import MagicMock, patch, call  # noqa: E402

from modules.check.check_runner import run_checks, check_run, _get_dependency_checks_map,\
    create_dependency_order  # noqa: E402


class TestCheckRun(unittest.TestCase):

    def test_check_run_positive(self):
        mocked_check = MagicMock()
        mocked_check.get_metadata.return_value = MagicMock()
        mocked_check.get_metadata.return_value.name = "check"
        mocked_check.get_metadata.return_value.timeout = 1
        mocked_check.run.return_value = CheckSummary(result=json.dumps({
            "Value": {
                "Check": {
                    "Value": "Check Value",
                    "RetVal": "INFO"
                }
            }
        }))

        expected = CheckSummary(result=json.dumps({
            "Value": {
                "Check": {
                    "Value": "Check Value",
                    "RetVal": "INFO"
                }
            }
        }))
        value = check_run(mocked_check, {})

        self.assertEqual(expected.__dict__, value.__dict__)

    def test_check_run_timeout_positive(self):
        mocked_check = MagicMock()
        mocked_check.get_metadata.return_value = MagicMock()
        mocked_check.get_metadata.return_value.name = "check"
        mocked_check.get_metadata.return_value.timeout = 1
        mocked_check.run = lambda data: time.sleep(2)

        expected = CheckSummary(result=json.dumps({
            "RetVal": "ERROR",
            "Verbosity": 0,
            "Message": "",
            "Value": {
                "check": {
                    "Value": "Timeout was exceeded.",
                    "Verbosity": 0,
                    "Message": "",
                    "RetVal": "ERROR"
                }
            }
        }))
        value = check_run(mocked_check, {})

        self.assertEqual(expected.__dict__, value.__dict__)

    def test_check_run_check_crush_positive(self):
        mocked_check = MagicMock()
        mocked_check.get_metadata.return_value = MagicMock()
        mocked_check.get_metadata.return_value.name = "check"
        mocked_check.get_metadata.return_value.timeout = 1
        mocked_check.run.side_effect = Exception()

        expected = CheckSummary(result=json.dumps({
            "RetVal": "ERROR",
            "Verbosity": 0,
            "Message": "",
            "Value": {
                "check": {
                    "Value": "",
                    "Verbosity": 0,
                    "Message": "The check crashed at runtime. No data was received. "
                               "See call stack above.",
                    "RetVal": "ERROR"
                }
            }
        }))
        value = check_run(mocked_check, {})

        self.assertEqual(expected.__dict__, value.__dict__)


class TestGetDependencyChecksMap(unittest.TestCase):

    def test__get_dependency_checks_map_positive(self):
        mocked_check = MagicMock()
        mocked_check.get_metadata.return_value = MagicMock()
        mocked_check.get_metadata.return_value.name = "check"
        mocked_check.get_metadata.return_value.version = 1

        expected = {"check": mocked_check}

        value = _get_dependency_checks_map([mocked_check], {"check": 1})

        self.assertEqual(expected, value)

    def test__get_dependency_checks_map_no_dep_positive(self):
        mocked_check = MagicMock()
        mocked_check.get_metadata.return_value = MagicMock()
        mocked_check.get_metadata.return_value.name = "check"
        mocked_check.get_metadata.return_value.version = 1

        expected = {}

        value = _get_dependency_checks_map([mocked_check], {})

        self.assertEqual(expected, value)

    @patch("logging.error")
    def test__get_dependency_checks_map_another_version_negative(self, mocked_log):
        mocked_check = MagicMock()
        mocked_check.get_metadata.return_value = MagicMock()
        mocked_check.get_metadata.return_value.name = "check"
        mocked_check.get_metadata.return_value.version = 1

        expected = {}

        value = _get_dependency_checks_map([mocked_check], {"check": 3})

        self.assertEqual(expected, value)
        mocked_log.assert_called()

    @patch("logging.error")
    def test__get_dependency_checks_map_not_found_negative(self, mocked_log):
        mocked_check = MagicMock()
        mocked_check.get_metadata.return_value = MagicMock()
        mocked_check.get_metadata.return_value.name = "check_2"
        mocked_check.get_metadata.return_value.version = 1

        expected = {}

        value = _get_dependency_checks_map([mocked_check], {"check": 1})

        self.assertEqual(expected, value)
        mocked_log.assert_called_once()


class TestCreateDependencyOrder(unittest.TestCase):

    def test_create_dependency_order_positive(self):
        mocked_check_1 = MagicMock()
        mocked_check_1.get_metadata.return_value = MagicMock()
        mocked_check_1.get_metadata.return_value.name = "check_1"
        mocked_check_1.get_metadata.return_value.version = 1
        mocked_check_1.get_metadata.return_value.dataReq = """{"check_3": 1}"""
        mocked_check_1.get_metadata.return_value.tags = "default"

        mocked_check_2 = MagicMock()
        mocked_check_2.get_metadata.return_value = MagicMock()
        mocked_check_2.get_metadata.return_value.name = "check_2"
        mocked_check_2.get_metadata.return_value.version = 1
        mocked_check_2.get_metadata.return_value.dataReq = """{"check_1": 1}"""
        mocked_check_2.get_metadata.return_value.tags = "default"

        mocked_check_3 = MagicMock()
        mocked_check_3.get_metadata.return_value = MagicMock()
        mocked_check_3.get_metadata.return_value.name = "check_3"
        mocked_check_3.get_metadata.return_value.version = 1
        mocked_check_3.get_metadata.return_value.dataReq = "{}"
        mocked_check_3.get_metadata.return_value.tags = "default"

        expected = (["check_1", "check_2", "check_3"], [mocked_check_3, mocked_check_1, mocked_check_2])

        value = create_dependency_order([mocked_check_1, mocked_check_2, mocked_check_3], {"default"})

        self.assertEqual(expected, value)


class TestRunChecks(unittest.TestCase):

    @patch("builtins.exit")
    @patch("builtins.print")
    def test_run_checks_no_checks_to_run(self, mocked_print, mocked_exit):
        expected_exit_code = 1

        run_checks([])

        mocked_print.assert_called_once()
        mocked_exit.assert_called_once_with(expected_exit_code)

    @patch("logging.error")
    def test_run_checks_does_not_have_dependency(self, mocked_error):
        mocked_check = MagicMock()
        mocked_check.get_metadata.return_value = MagicMock()
        mocked_check.get_metadata.return_value.name = "check"
        mocked_check.get_metadata.return_value.dataReq = """{"data": "1"}"""
        mocked_check.get_summary.return_value = None

        run_checks([mocked_check])

        mocked_error.assert_called()

    @patch("modules.check.check_runner.check_run")
    def test_run_checks_run_check(self, mocked_check_run):
        mocked_summary = MagicMock()
        mocked_summary.result = "{}"
        mocked_check = MagicMock()
        mocked_check.get_metadata.return_value = MagicMock()
        mocked_check.get_metadata.return_value.name = "check"
        mocked_check.get_metadata.return_value.timeout = 1
        mocked_check.get_metadata.return_value.dataReq = "{}"
        mocked_check.get_summary.return_value = mocked_summary

        run_checks([mocked_check])

        mocked_check_run.assert_called_once_with(mocked_check, {})

    @patch("modules.check.check_runner.check_run")
    def test_run_checks_run_two_dependencies_checks(self, mocked_check_run):
        mocked_summary_1 = MagicMock()
        mocked_summary_1.result = "{}"
        mocked_check_1 = MagicMock()
        mocked_check_1.get_metadata.return_value = MagicMock()
        mocked_check_1.get_metadata.return_value.name = "check_1"
        mocked_check_1.get_metadata.return_value.timeout = 1
        mocked_check_1.get_metadata.return_value.dataReq = """{"check_2": "1"}"""
        mocked_check_1.get_summary.return_value = mocked_summary_1

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
        mocked_check_2.get_metadata.return_value.version = "1"
        mocked_check_2.get_metadata.return_value.timeout = 1
        mocked_check_2.get_metadata.return_value.dataReq = "{}"
        mocked_check_2.get_summary.return_value = mocked_summary_2

        run_checks([mocked_check_2, mocked_check_1])

        expected_calls = [
            call(mocked_check_2, {}),
            call(
                mocked_check_1,
                {"check_2": {"Value": {"Check 2": {"Value": "Check 2 Value", "RetVal": "INFO"}}}}
            )
        ]
        mocked_check_run.assert_has_calls(expected_calls)

    @patch("modules.check.check_runner.check_run")
    def test_run_checks_run_two_separate_checks(self, mocked_check_run):
        mocked_summary = MagicMock()
        mocked_summary.result = "{}"
        mocked_check_1 = MagicMock()
        mocked_check_1.get_metadata.return_value = MagicMock()
        mocked_check_1.get_metadata.return_value.name = "check_1"
        mocked_check_1.get_metadata.return_value.timeout = 1
        mocked_check_1.get_metadata.return_value.dataReq = "{}"
        mocked_check_1.get_summary.return_value = mocked_summary

        mocked_check_2 = MagicMock()
        mocked_check_2.get_metadata.return_value = MagicMock()
        mocked_check_2.get_metadata.return_value.name = "check_2"
        mocked_check_2.get_metadata.return_value.timeout = 1
        mocked_check_2.get_metadata.return_value.dataReq = "{}"
        mocked_check_2.get_summary.return_value = mocked_summary

        run_checks([mocked_check_1, mocked_check_2])

        expected_calls = [
            call(mocked_check_2, {}),
            call(mocked_check_1, {})
        ]
        mocked_check_run.assert_has_calls(expected_calls, any_order=True)


if __name__ == '__main__':
    unittest.main()
