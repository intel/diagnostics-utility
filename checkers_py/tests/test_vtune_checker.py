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

from checkers_py import vtune_checker  # noqa: E402
from checkers_py.common import advisor_vtune_helper as common_advisor_vtune  # noqa: E402
from modules.check import CheckSummary, CheckMetadataPy  # noqa: E402


class TestVtuneCheckerApiTest(unittest.TestCase):

    @patch("checkers_py.common.advisor_vtune_helper.get_OS", return_value=common_advisor_vtune.LINUX)
    @patch("checkers_py.vtune_checker.check_metrics_discovery_API_lib")
    @patch("checkers_py.common.advisor_vtune_helper.check_perf_stream_paranoid")
    @patch("checkers_py.vtune_checker.check_debugFS_permissions")
    @patch("checkers_py.vtune_checker.check_kernel_config_options")
    def test_run_on_linux(
            self,
            mocked_check_kernel_config_options,
            mocked_check_debugFS_permissions,
            mocked_check_perf_stream_paranoid,
            mocked_check_metrics_discovery_API_lib,
            mocked_get_OS):
        expected = CheckSummary

        mocked_check_metrics_discovery_API_lib.side_effect = lambda node: node.update({
            "Check 1": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })
        mocked_check_perf_stream_paranoid.side_effect = lambda node: node.update({
            "Check 2": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })
        mocked_check_debugFS_permissions.side_effect = lambda node: node.update({
            "Check 3": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })
        mocked_check_kernel_config_options.side_effect = lambda node: node.update({
            "Check 4": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })

        value = vtune_checker.run_vtune_check({})

        self.assertIsInstance(value, expected)

    @patch("checkers_py.common.advisor_vtune_helper.get_OS", return_value=common_advisor_vtune.WINDOWS)
    def test_run_on_windows(self, mocked_get_OS):
        expected = CheckSummary

        value = vtune_checker.run_vtune_check({})

        self.assertIsInstance(value, expected)

    def test_get_api_version_returns_str(self):
        expected = str

        value = vtune_checker.get_api_version()

        self.assertIsInstance(value, expected)

    def test_get_check_list_returns_list_metadata(self):
        expected = CheckMetadataPy

        value = vtune_checker.get_check_list()

        for metadata in value:
            self.assertIsInstance(metadata, expected)


class TestCheckDebugFSPermissions(unittest.TestCase):

    @patch("os.access", return_value=True)
    def test_check_debugFS_permissions_positive(self, mocked_access):
        expected = {
            "debugFS permissions": {
                "Value": "Configured",
                "RetVal": "PASS",
                "Command": "ls -l /sys/kernel/debug"
            }
        }

        value = {}
        vtune_checker.check_debugFS_permissions(value)

        self.assertEqual(expected, value)

    @patch("os.access", return_value=False)
    def test_check_debugFS_permissions_negative(self, mocked_access):
        expected = {
            "debugFS permissions": {
                "Value": "Not configured",
                "RetVal": "FAIL",
                "Command": "ls -l /sys/kernel/debug",
                "Message": "Use the prepare_debugfs.sh script to set read/write permissions to debugFS."
            }
        }

        value = {}
        vtune_checker.check_debugFS_permissions(value)

        self.assertEqual(expected, value)


class TestCheckMetricsDiscoveryAPILib(unittest.TestCase):

    @patch("subprocess.Popen")
    def test_check_metrics_discovery_API_lib_lib_exists(self, mocked_open):
        expected = {
            "Metrics Library for Metrics Discovery API is installed": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "ls -l /usr/lib/x86_64-linux-gnu | grep libmd"
            }
        }

        ls_mock = MagicMock()
        ls_mock.wait.return_value = 0

        grep_mock = MagicMock()
        grep_mock.communicate.return_value = ("libmd", None)
        grep_mock.returncode = 0

        mocked_open.side_effect = [ls_mock, grep_mock]

        value = {}
        vtune_checker.check_metrics_discovery_API_lib(value)

        self.assertEqual(expected, value)

    @patch("subprocess.Popen")
    def test_check_metrics_discovery_API_lib_lib_does_not_exists(self, mocked_open):
        expected = {
            "Metrics Library for Metrics Discovery API is installed": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "ls -l /usr/lib/x86_64-linux-gnu | grep libmd",
                "Message": "Install Metrics Library for Metrics Discovery API."
            }
        }

        ls_mock = MagicMock()
        ls_mock.wait.return_value = 0

        grep_mock = MagicMock()
        grep_mock.communicate.return_value = ("", None)
        grep_mock.returncode = 1

        mocked_open.side_effect = [ls_mock, grep_mock]

        value = {}
        vtune_checker.check_metrics_discovery_API_lib(value)

        self.assertEqual(expected, value)

    @patch("subprocess.Popen")
    def test_check_metrics_discovery_API_lib_ls_return_code_is_not_zero(self, mocked_open):
        expected = {
            "Metrics Library for Metrics Discovery API is installed": {
                "Value": "",
                "RetVal": "ERROR",
                "Command": "ls -l /usr/lib/x86_64-linux-gnu | grep libmd",
                "Message": "Cannot get information about x86_64-bit libraries."
            }
        }

        ls_mock = MagicMock()
        ls_mock.wait.return_value = 1

        grep_mock = MagicMock()

        mocked_open.side_effect = [ls_mock, grep_mock]

        value = {}
        vtune_checker.check_metrics_discovery_API_lib(value)

        self.assertEqual(expected, value)

    @patch("subprocess.Popen")
    def test_check_metrics_discovery_API_lib_grep_return_code_is_not_zero_or_one(self, mocked_open):
        expected = {
            "Metrics Library for Metrics Discovery API is installed": {
                "Value": "",
                "RetVal": "ERROR",
                "Command": "ls -l /usr/lib/x86_64-linux-gnu | grep libmd",
                "Message": "Error from grep function"
            }
        }

        ls_mock = MagicMock()
        ls_mock.wait.return_value = 0

        grep_mock = MagicMock()
        grep_mock.communicate.return_value = ("", None)
        grep_mock.returncode = 3

        mocked_open.side_effect = [ls_mock, grep_mock]

        value = {}
        vtune_checker.check_metrics_discovery_API_lib(value)

        self.assertEqual(expected, value)


class TestCheckKernelConfigOptions(unittest.TestCase):

    @patch("platform.uname")
    @patch("subprocess.Popen")
    def test_check_kernel_config_options_positive(self, mocked_open, mocked_uname):
        expected = {
            "CONFIG_DRM_I915_LOW_LEVEL_TRACEPOINTS": {
                "Value": "Enable",
                "RetVal": "PASS",
                "Command": "grep CONFIG_DRM_I915_LOW_LEVEL_TRACEPOINTS /boot/config-5.11.0-34-generic"
            }
        }

        mocked_uname.return_value = MagicMock()
        mocked_uname.return_value.release = "5.11.0-34-generic"

        proc_mock = MagicMock()
        proc_mock.communicate.return_value = ("", None)
        proc_mock.returncode = 0

        mocked_open.return_value = proc_mock

        value = {}
        vtune_checker.check_kernel_config_options(value)

        self.assertEqual(expected, value)

    @patch("platform.uname")
    @patch("subprocess.Popen")
    def test_check_kernel_config_options_parameter_is_not_set(self, mocked_open, mocked_uname):
        expected = {
            "CONFIG_DRM_I915_LOW_LEVEL_TRACEPOINTS": {
                "Value": "Disable or not set",
                "RetVal": "FAIL",
                "Command": "grep CONFIG_DRM_I915_LOW_LEVEL_TRACEPOINTS /boot/config-5.11.0-34-generic",
                "Message": "Rebuild the i915 driver or kernel."
            }
        }

        mocked_uname.return_value = MagicMock()
        mocked_uname.return_value.release = "5.11.0-34-generic"

        proc_mock = MagicMock()
        proc_mock.communicate.return_value = ("# CONFIG_DRM_I915_LOW_LEVEL_TRACEPOINTS is not set", None)
        proc_mock.returncode = 0

        mocked_open.return_value = proc_mock

        value = {}
        vtune_checker.check_kernel_config_options(value)

        self.assertEqual(expected, value)

    @patch("platform.uname")
    @patch("subprocess.Popen")
    def test_check_kernel_config_options_parameter_is_disabled(self, mocked_open, mocked_uname):
        expected = {
            "CONFIG_DRM_I915_LOW_LEVEL_TRACEPOINTS": {
                "Value": "Disable or not set",
                "RetVal": "FAIL",
                "Command": "grep CONFIG_DRM_I915_LOW_LEVEL_TRACEPOINTS /boot/config-5.11.0-34-generic",
                "Message": "Rebuild the i915 driver or kernel."
            }
        }

        mocked_uname.return_value = MagicMock()
        mocked_uname.return_value.release = "5.11.0-34-generic"

        proc_mock = MagicMock()
        proc_mock.communicate.return_value = ("CONFIG_DRM_I915_LOW_LEVEL_TRACEPOINTS=n", None)
        proc_mock.returncode = 0

        mocked_open.return_value = proc_mock

        value = {}
        vtune_checker.check_kernel_config_options(value)

        self.assertEqual(expected, value)

    @patch("platform.uname")
    @patch("subprocess.Popen")
    def test_check_kernel_config_options_proc_return_value_is_not_zero(self, mocked_open, mocked_uname):
        expected = {
            "CONFIG_DRM_I915_LOW_LEVEL_TRACEPOINTS": {
                "Value": "Undefined",
                "RetVal": "ERROR",
                "Command": "grep CONFIG_DRM_I915_LOW_LEVEL_TRACEPOINTS /boot/config-5.11.0-34-generic",
                "Message": "Cannot get information about kernel config option."
            }
        }

        mocked_uname.return_value = MagicMock()
        mocked_uname.return_value.release = "5.11.0-34-generic"

        proc_mock = MagicMock()
        proc_mock.communicate.return_value = (None, None)
        proc_mock.returncode = 1

        mocked_open.return_value = proc_mock

        value = {}
        vtune_checker.check_kernel_config_options(value)

        self.assertEqual(expected, value)


if __name__ == '__main__':
    unittest.main()
