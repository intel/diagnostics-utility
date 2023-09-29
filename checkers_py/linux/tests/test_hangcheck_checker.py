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
from unittest.mock import MagicMock, patch, mock_open  # noqa: E402

from checkers_py.linux import hangcheck_checker  # noqa: E402
from modules.check import CheckSummary, CheckMetadataPy  # noqa: E402


class TestHangcheckCheckerApiTest(unittest.TestCase):

    @patch("checkers_py.linux.hangcheck_checker.intel_gpus_not_found_handler")
    @patch("checkers_py.linux.hangcheck_checker.check_hangcheck_is_disabled")
    @patch("checkers_py.linux.hangcheck_checker.check_non_zero_pre_emption_timeouts")
    @patch("checkers_py.linux.hangcheck_checker.are_intel_gpus_found", return_value=False)
    def test_run_positive_without_gpu(
            self,
            mocked_are_intel_gpus_found,
            mocked_check_non_zero_pre_emption_timeouts,
            mocked_check_hangcheck_is_disabled,
            mocked_intel_gpus_not_found_handler):
        expected = CheckSummary

        mocked_intel_gpus_not_found_handler.side_effect = lambda node: node.update({
            "Warning": {
                "CheckResult": "some data",
                "CheckStatus": "WARNING"
            }
        })
        mocked_check_hangcheck_is_disabled.side_effect = lambda node: node.update({
            "Check 1": {
                "CheckResult": "some data",
                "CheckStatus": "INFO"
            }
        })
        mocked_check_non_zero_pre_emption_timeouts.side_effect = lambda node: node.update({
            "Check 2": {
                "CheckResult": "some data",
                "CheckStatus": "INFO"
            }
        })

        actual = hangcheck_checker.run_hangcheck_check({})

        mocked_are_intel_gpus_found.assert_called_once()
        self.assertIsInstance(actual, expected)

    @patch("checkers_py.linux.hangcheck_checker.check_hangcheck_is_disabled")
    @patch("checkers_py.linux.hangcheck_checker.check_non_zero_pre_emption_timeouts")
    @patch("checkers_py.linux.hangcheck_checker.are_intel_gpus_found", return_value=True)
    def test_run_positive_with_gpu(
            self,
            mocked_are_intel_gpus_found,
            mocked_check_non_zero_pre_emption_timeouts,
            mocked_check_hangcheck_is_disabled):
        expected = CheckSummary

        mocked_check_hangcheck_is_disabled.side_effect = lambda node: node.update({
            "Check 1": {
                "CheckResult": "some data",
                "CheckStatus": "INFO"
            }
        })
        mocked_check_non_zero_pre_emption_timeouts.side_effect = lambda node: node.update({
            "Check 2": {
                "CheckResult": "some data",
                "CheckStatus": "INFO"
            }
        })

        actual = hangcheck_checker.run_hangcheck_check({})

        mocked_are_intel_gpus_found.assert_called_once()
        self.assertIsInstance(actual, expected)

    def test_get_api_version_returns_str(self):
        expected = str

        actual = hangcheck_checker.get_api_version()

        self.assertIsInstance(actual, expected)

    def test_get_check_list_returns_list_metadata(self):
        expected = CheckMetadataPy

        check_list = hangcheck_checker.get_check_list()

        for metadata in check_list:
            self.assertIsInstance(metadata, expected)


class TestCheckHangcheckInGrub(unittest.TestCase):

    @patch("builtins.open", mock_open(read_data=""))
    @patch("configparser.ConfigParser")
    def test__check_hangcheck_in_grub_positive(self, mocked_parser):
        expected = {
            "Command": "grep i915.enable_hangcheck=0 /etc/default/grub",
            "Message": "Kernel hangcheck is disabled. "
                       "If it is not working, reboot or run 'sudo update-grub' for it to take effect.",
            "CheckStatus": "PASS"
        }

        mocked_parser.return_value = MagicMock()
        mocked_parser.return_value.has_option.return_value = True
        mocked_parser.return_value.get.return_value = ["i915.enable_hangcheck=0"]

        actual = {}
        hangcheck_checker._check_hangcheck_in_grub(actual)

        self.assertEqual(expected, actual)

    @patch("builtins.open", mock_open(read_data=""))
    @patch("configparser.ConfigParser")
    def test__check_hangcheck_in_grub_confid_does_not_have_option(self, mocked_parser):
        expected = {
            "Command": "grep i915.enable_hangcheck=0 /etc/default/grub"
        }

        mocked_parser.return_value = MagicMock()
        mocked_parser.return_value.has_option.return_value = False

        actual = {}
        hangcheck_checker._check_hangcheck_in_grub(actual)

        self.assertEqual(expected, actual)

    @patch("builtins.open", mock_open(read_data=""))
    @patch("configparser.ConfigParser")
    def test__check_hangcheck_in_grub_option_is_not_in_config(self, mocked_parser):
        expected = {
            "Command": "grep i915.enable_hangcheck=0 /etc/default/grub"
        }

        mocked_parser.return_value = MagicMock()
        mocked_parser.return_value.has_option.return_value = True
        mocked_parser.return_value.get.return_value = [""]

        actual = {}
        hangcheck_checker._check_hangcheck_in_grub(actual)

        self.assertEqual(expected, actual)

    @patch("builtins.open", side_effect=Exception("test message"))
    @patch("configparser.ConfigParser")
    def test__check_hangcheck_in_grub_open_raise_exception(self, mocked_parser, mocked_open):
        expected = {
            "Command": "grep i915.enable_hangcheck=0 /etc/default/grub",
            "Message": "test message",
            "CheckStatus": "ERROR",
            "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."  # noqa: E501
        }

        actual = {}
        hangcheck_checker._check_hangcheck_in_grub(actual)

        self.assertEqual(expected, actual)


class TestCheckHangcheckInConfig(unittest.TestCase):

    @patch("builtins.open", mock_open(read_data="N"))
    def test__check_hangcheck_in_config_positive(self):
        expected = {
            "Command": "cat /sys/module/i915/parameters/enable_hangcheck",
            "CheckStatus": "PASS",
            "Message": "To disable GPU hangcheck across reboots, visit "
                       "https://www.intel.com/content/www/us/en/develop/documentation/get-started-with-intel-oneapi-hpc-linux/top/before-you-begin.html."  # noqa: E501
        }

        actual = {}
        hangcheck_checker._check_hangcheck_in_config(actual)

        self.assertEqual(expected, actual)

    @patch("builtins.open", mock_open(read_data="y"))
    def test__check_hangcheck_in_config_option_is_enabled(self):
        expected = {
            "Command": "cat /sys/module/i915/parameters/enable_hangcheck"
        }

        actual = {}
        hangcheck_checker._check_hangcheck_in_config(actual)

        self.assertEqual(expected, actual)

    @patch("builtins.open", side_effect=Exception("test message"))
    def test__check_hangcheck_in_config_open_raise_exception(self, mocked_open):
        expected = {
            "Command": "cat /sys/module/i915/parameters/enable_hangcheck",
            "CheckStatus": "ERROR",
            "Message": "test message",
            "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."  # noqa: E501
        }

        actual = {}
        hangcheck_checker._check_hangcheck_in_config(actual)

        self.assertEqual(expected, actual)


class TestCheckHangcheckIsDisabled(unittest.TestCase):

    @patch("os.path.isfile", side_effect=[True, True])
    @patch("checkers_py.linux.hangcheck_checker._check_hangcheck_in_grub")
    @patch("checkers_py.linux.hangcheck_checker._check_hangcheck_in_config")
    def test_check_hangcheck_is_disabled_hangcheck_is_disabled_in_grub(
            self,
            mocked__check_hangcheck_in_config,
            mocked__check_hangcheck_in_grub,
            mocked_isfile):
        expected = {
            "GPU hangcheck is disabled": {
                "CheckResult": "",
                "CheckStatus": "PASS",
                "Message": ""
            }
        }

        mocked__check_hangcheck_in_grub.side_effect = lambda node: node.update({
            "CheckStatus": "PASS",
            "Message": ""
        })

        actual = {}
        hangcheck_checker.check_hangcheck_is_disabled(actual)

        mocked__check_hangcheck_in_grub.assert_called_once()
        mocked__check_hangcheck_in_config.assert_not_called()
        self.assertEqual(expected, actual)

    @patch("os.path.isfile", side_effect=[True, True])
    @patch("checkers_py.linux.hangcheck_checker._check_hangcheck_in_grub")
    @patch("checkers_py.linux.hangcheck_checker._check_hangcheck_in_config")
    def test_check_hangcheck_is_disabled_hangcheck_is_enabled_in_grub(
            self,
            mocked__check_hangcheck_in_config,
            mocked__check_hangcheck_in_grub,
            mocked_isfile):
        expected = {
            "GPU hangcheck is disabled": {
                "CheckResult": "",
                "CheckStatus": "PASS",
                "Message": ""
            }
        }

        mocked__check_hangcheck_in_config.side_effect = lambda node: node.update({
            "CheckStatus": "PASS",
            "Message": ""
        })

        actual = {}
        hangcheck_checker.check_hangcheck_is_disabled(actual)

        mocked__check_hangcheck_in_grub.assert_called_once()
        mocked__check_hangcheck_in_config.assert_called_once()
        self.assertEqual(expected, actual)

    @patch("os.path.isfile", side_effect=[False, True])
    @patch("checkers_py.linux.hangcheck_checker._check_hangcheck_in_grub")
    @patch("checkers_py.linux.hangcheck_checker._check_hangcheck_in_config")
    def test_check_hangcheck_is_disabled_grub_config_is_not_file(
            self,
            mocked__check_hangcheck_in_config,
            mocked__check_hangcheck_in_grub,
            mocked_isfile):
        expected = {
            "GPU hangcheck is disabled": {
                "CheckResult": "",
                "CheckStatus": "PASS",
                "Message": ""
            }
        }

        mocked__check_hangcheck_in_config.side_effect = lambda node: node.update({
            "CheckStatus": "PASS",
            "Message": ""
        })

        actual = {}
        hangcheck_checker.check_hangcheck_is_disabled(actual)

        mocked__check_hangcheck_in_grub.assert_not_called()
        mocked__check_hangcheck_in_config.assert_called_once()
        self.assertEqual(expected, actual)

    @patch("os.path.isfile", side_effect=[False, False])
    @patch("checkers_py.linux.hangcheck_checker._check_hangcheck_in_grub")
    @patch("checkers_py.linux.hangcheck_checker._check_hangcheck_in_config")
    def test_check_hangcheck_is_disabled_grub_config_and_config_are_not_files(
            self,
            mocked__check_hangcheck_in_config,
            mocked__check_hangcheck_in_grub,
            mocked_isfile):
        expected = {
            "GPU hangcheck is disabled": {
                "CheckResult": "",
                "CheckStatus": "FAIL",
                "Message": "To disable GPU hangcheck, visit "
                           "https://www.intel.com/content/www/us/en/develop/documentation/get-started-with-intel-oneapi-hpc-linux/top/before-you-begin.html.",  # noqa: E501
                "HowToFix": "Try disable GPU hangcheck, based on instructions from "
                            "https://www.intel.com/content/www/us/en/develop/documentation/get-started-with-intel-oneapi-hpc-linux/top/before-you-begin.html."  # noqa E501
            }
        }

        actual = {}
        hangcheck_checker.check_hangcheck_is_disabled(actual)

        mocked__check_hangcheck_in_grub.assert_not_called()
        mocked__check_hangcheck_in_config.assert_not_called()
        self.assertEqual(expected, actual)


class TestCheckNonZeroPreEmptionTimeouts(unittest.TestCase):

    @patch("subprocess.Popen")
    def test_check_non_zero_pre_emption_timeouts_positive(self, mocked_open):
        expected = {
            "Queried preempt_timeout_ms": {
                "CheckResult": {
                    "preempt_timeout_ms=0 to prevent long-running jobs from hanging": {
                        "CheckResult": "",
                        "CheckStatus": "PASS"
                    }
                },
                "CheckStatus": "PASS",
                "Command": "find /sys/devices -regex .*/drm/card[0-9]*/engine/[rc]cs[0-9]*/preempt_timeout_ms"
                           " -exec cat {} +"
            }
        }

        proc_mock = MagicMock()
        proc_mock.communicate.return_value = ("0", None)
        proc_mock.returncode = 0

        mocked_open.return_value = proc_mock

        actual = {}
        hangcheck_checker.check_non_zero_pre_emption_timeouts(actual)

        self.assertEqual(expected, actual)

    @patch("subprocess.Popen")
    def test_check_non_zero_pre_emption_timeouts_timeout_is_not_zero(self, mocked_open):
        expected = {
            "Queried preempt_timeout_ms": {
                "CheckResult": {
                    "preempt_timeout_ms=0 to prevent long-running jobs from hanging": {
                        "CheckResult": "",
                        "CheckStatus": "FAIL",
                        "Message": "preempt_timeout_ms=1 - long-running jobs may not run to completion.",
                        "HowToFix": "To disable preemption timeout, visit "
                            "https://www.intel.com/content/www/us/en/develop/documentation/installation-guide-for-intel-oneapi-toolkits-hpc-cluster/top/step-4-set-up-user-permissions.html#step-4-set-up-user-permissions-for-using-the-device-files-for-intel-gpus_disable-timeout" # noqa E501
                    }
                },
                "CheckStatus": "PASS",
                "Command": "find /sys/devices -regex .*/drm/card[0-9]*/engine/[rc]cs[0-9]*/preempt_timeout_ms"
                           " -exec cat {} +"
            }
        }

        proc_mock = MagicMock()
        proc_mock.communicate.return_value = ("1", None)
        proc_mock.returncode = 0

        mocked_open.return_value = proc_mock

        actual = {}
        hangcheck_checker.check_non_zero_pre_emption_timeouts(actual)

        self.assertEqual(expected, actual)

    @patch("subprocess.Popen")
    def test_check_non_zero_pre_emption_timeouts_max_timeout_is_not_zero(self, mocked_open):
        expected = {
            "Queried preempt_timeout_ms": {
                "CheckResult": {
                    "preempt_timeout_ms=0 to prevent long-running jobs from hanging": {
                        "CheckResult": "",
                        "CheckStatus": "FAIL",
                        "Message": "preempt_timeout_ms=1 - long-running jobs may not run to completion.",
                        "HowToFix": "To disable preemption timeout, visit "
                            "https://www.intel.com/content/www/us/en/develop/documentation/installation-guide-for-intel-oneapi-toolkits-hpc-cluster/top/step-4-set-up-user-permissions.html#step-4-set-up-user-permissions-for-using-the-device-files-for-intel-gpus_disable-timeout" # noqa E501
                    }
                },
                "CheckStatus": "PASS",
                "Command": "find /sys/devices -regex .*/drm/card[0-9]*/engine/[rc]cs[0-9]*/preempt_timeout_ms"
                           " -exec cat {} +"
            }
        }

        proc_mock = MagicMock()
        proc_mock.communicate.return_value = ("0\n0\n1", None)
        proc_mock.returncode = 0

        mocked_open.return_value = proc_mock

        actual = {}
        hangcheck_checker.check_non_zero_pre_emption_timeouts(actual)

        self.assertEqual(expected, actual)

    @patch("subprocess.Popen")
    def test_check_non_zero_pre_emption_timeouts_proc_return_code_is_not_none(self, mocked_open):
        expected = {
            "Queried preempt_timeout_ms": {
                "CheckResult": "",
                "CheckStatus": "ERROR",
                "Command": "find /sys/devices -regex .*/drm/card[0-9]*/engine/[rc]cs[0-9]*/preempt_timeout_ms"
                           " -exec cat {} +",
                "Message": "Cannot get information about preempt_timeout_ms",
                "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."  # noqa: E501
            }
        }

        proc_mock = MagicMock()
        proc_mock.communicate.return_value = (None, None)
        proc_mock.returncode = 1

        mocked_open.return_value = proc_mock

        actual = {}
        hangcheck_checker.check_non_zero_pre_emption_timeouts(actual)

        self.assertEqual(expected, actual)

    @patch("subprocess.Popen", side_effect=Exception("test message"))
    def test_check_non_zero_pre_emption_timeouts_popen_raise_exception(self, mocked_open):
        expected = {
            "Queried preempt_timeout_ms": {
                "CheckResult": "",
                "CheckStatus": "ERROR",
                "Command": "find /sys/devices -regex .*/drm/card[0-9]*/engine/[rc]cs[0-9]*/preempt_timeout_ms"
                           " -exec cat {} +",
                "Message": "test message",
                "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."  # noqa: E501
            }
        }

        actual = {}
        hangcheck_checker.check_non_zero_pre_emption_timeouts(actual)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.TestCase.maxDiff = None
    unittest.main()
