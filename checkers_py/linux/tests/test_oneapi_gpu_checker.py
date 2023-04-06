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

from checkers_py.linux import oneapi_gpu_checker  # noqa: E402
from modules.check import CheckSummary, CheckMetadataPy  # noqa: E402


class TestOneapiGpuCheckerApiTest(unittest.TestCase):

    @patch("checkers_py.linux.oneapi_gpu_checker.get_dpcpp_offload_info")
    @patch("checkers_py.linux.oneapi_gpu_checker.get_openmp_offload_info")
    @patch("checkers_py.linux.oneapi_gpu_checker.get_gpu_errors_info")
    @patch("checkers_py.linux.oneapi_gpu_checker.get_dmesg_i915_init_errors_info")
    @patch("checkers_py.linux.oneapi_gpu_checker.get_permissions_to_render_info")
    @patch("checkers_py.linux.oneapi_gpu_checker.get_permissions_to_card_info")
    @patch("checkers_py.linux.oneapi_gpu_checker.get_intel_device_is_available_info")
    @patch("checkers_py.linux.oneapi_gpu_checker.get_i915_driver_loaded_info")
    @patch("checkers_py.linux.oneapi_gpu_checker.intel_gpus_not_found_handler")
    @patch("checkers_py.linux.oneapi_gpu_checker.are_intel_gpus_found", return_value=False)
    def test_run_positive_without_gpu(
            self,
            mocked_are_intel_gpus_found,
            mocked_intel_gpus_not_found_handler,
            mocked_get_i915_driver_loaded_info,
            mocked_get_intel_device_is_available_info,
            mocked_get_permissions_to_card_info,
            mocked_get_permissions_to_render_info,
            mocked_get_dmesg_i915_init_errors_info,
            mocked_get_gpu_errors_info,
            mocked_get_openmp_offload_info,
            mocked_get_dpcpp_offload_info,):
        expected = CheckSummary

        mocked_intel_gpus_not_found_handler.side_effect = lambda node: node.update({
            "Warning": {
                "Value": "Value",
                "RetVal": "WARNING"
            }
        })
        mocked_get_i915_driver_loaded_info.side_effect = lambda node: node.update({
            "Check 1": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })
        mocked_get_intel_device_is_available_info.side_effect = lambda node: node.update({
            "Check 2": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })
        mocked_get_permissions_to_card_info.side_effect = lambda node: node.update({
            "Check 3": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })
        mocked_get_permissions_to_render_info.side_effect = lambda node: node.update({
            "Check 4": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })
        mocked_get_dmesg_i915_init_errors_info.side_effect = lambda node: node.update({
            "Check 5": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })
        mocked_get_gpu_errors_info.side_effect = lambda node: node.update({
            "Check 6": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })
        mocked_get_openmp_offload_info.side_effect = lambda node: node.update({
            "Check 7": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })
        mocked_get_dpcpp_offload_info.side_effect = lambda node: node.update({
            "Check 8": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })

        value = oneapi_gpu_checker.run_oneapi_gpu_check({})

        mocked_are_intel_gpus_found.assert_called_once()
        self.assertIsInstance(value, expected)

    @patch("checkers_py.linux.oneapi_gpu_checker.get_dpcpp_offload_info")
    @patch("checkers_py.linux.oneapi_gpu_checker.get_openmp_offload_info")
    @patch("checkers_py.linux.oneapi_gpu_checker.get_gpu_errors_info")
    @patch("checkers_py.linux.oneapi_gpu_checker.get_dmesg_i915_init_errors_info")
    @patch("checkers_py.linux.oneapi_gpu_checker.get_permissions_to_render_info")
    @patch("checkers_py.linux.oneapi_gpu_checker.get_permissions_to_card_info")
    @patch("checkers_py.linux.oneapi_gpu_checker.get_intel_device_is_available_info")
    @patch("checkers_py.linux.oneapi_gpu_checker.get_i915_driver_loaded_info")
    @patch("checkers_py.linux.oneapi_gpu_checker.are_intel_gpus_found", return_value=True)
    def test_run_positive_with_gpu(
            self,
            mocked_are_intel_gpus_found,
            mocked_get_i915_driver_loaded_info,
            mocked_get_intel_device_is_available_info,
            mocked_get_permissions_to_card_info,
            mocked_get_permissions_to_render_info,
            mocked_get_dmesg_i915_init_errors_info,
            mocked_get_gpu_errors_info,
            mocked_get_openmp_offload_info,
            mocked_get_dpcpp_offload_info,):
        expected = CheckSummary

        mocked_get_i915_driver_loaded_info.side_effect = lambda node: node.update({
            "Check 1": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })
        mocked_get_intel_device_is_available_info.side_effect = lambda node: node.update({
            "Check 2": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })
        mocked_get_permissions_to_card_info.side_effect = lambda node: node.update({
            "Check 3": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })
        mocked_get_permissions_to_render_info.side_effect = lambda node: node.update({
            "Check 4": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })
        mocked_get_dmesg_i915_init_errors_info.side_effect = lambda node: node.update({
            "Check 5": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })
        mocked_get_gpu_errors_info.side_effect = lambda node: node.update({
            "Check 6": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })
        mocked_get_openmp_offload_info.side_effect = lambda node: node.update({
            "Check 7": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })
        mocked_get_dpcpp_offload_info.side_effect = lambda node: node.update({
            "Check 8": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })

        value = oneapi_gpu_checker.run_oneapi_gpu_check({})

        mocked_are_intel_gpus_found.assert_called_once()
        self.assertIsInstance(value, expected)

    def test_get_api_version_returns_str(self):
        expected = str

        value = oneapi_gpu_checker.get_api_version()

        self.assertIsInstance(value, expected)

    def test_get_check_list_returns_list_metadata(self):
        expected = CheckMetadataPy

        value = oneapi_gpu_checker.get_check_list()

        for metadata in value:
            self.assertIsInstance(metadata, expected)


class TestGetI915DriverInfo(unittest.TestCase):

    @patch("subprocess.Popen")
    def test_get_i915_driver_loaded_info_positive(self, mocked_open):

        expected = {
            "Intel® Graphics Driver is loaded.": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "lsmod | grep i915"
            }
        }
        lsmod_mock = MagicMock()
        lsmod_mock.wait.return_value = 0

        grep_mock = MagicMock()
        grep_mock.communicate.return_value = (
            "i915_spi               24576  0\n"
            "mtd                    69632  6 i915_spi\n"
            "i915                 2949120  4\n"
            "i2c_algo_bit           16384  1 i915\n"
            "drm_kms_helper        245760  1 i915\n"
            "cec                    53248  2 drm_kms_helper,i915\n"
            "drm                   548864  3 drm_kms_helper,i915\n"
            "video                  49152  1 i915\n",
            None
        )
        grep_mock.returncode = 0

        mocked_open.side_effect = [lsmod_mock, grep_mock]

        value = {}
        oneapi_gpu_checker.get_i915_driver_loaded_info(value)

        self.assertEqual(expected, value)

    @patch("subprocess.Popen")
    def test_get_i915_driver_loaded_info_lsmod_return_code_is_not_zero(self, mocked_open):

        expected = {
            "Intel® Graphics Driver is loaded.": {
                "Value": "",
                "RetVal": "ERROR",
                "Command": "lsmod | grep i915",
                "Message": "Cannot get information about kernel modules that are currently loaded",
                "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."  # noqa E501
            }
        }
        lsmod_mock = MagicMock()
        lsmod_mock.wait.return_value = (None, None)
        lsmod_mock.returncode = 1

        mocked_open.return_value = lsmod_mock

        value = {}

        oneapi_gpu_checker.get_i915_driver_loaded_info(value)

        self.assertEqual(expected, value)

    @patch("subprocess.Popen")
    def test_get_i915_driver_loaded_info_grep_return_code_is_not_zero_or_one(self, mocked_open):
        expected = {
            "Intel® Graphics Driver is loaded.": {
                "Value": "",
                "RetVal": "ERROR",
                "Command": "lsmod | grep i915",
                "Message": "Cannot get information about whether the Intel® Graphics Driver is loaded.",
                "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."  # noqa E501
            }
        }

        lsmod_mock = MagicMock()
        lsmod_mock.wait.return_value = 0

        grep_mock = MagicMock()
        grep_mock.communicate.return_value = (None, None)
        grep_mock.returncode = 2

        mocked_open.side_effect = [lsmod_mock, grep_mock]

        value = {}
        oneapi_gpu_checker.get_i915_driver_loaded_info(value)

        self.assertEqual(expected, value)

    @patch("subprocess.Popen")
    def test_get_i915_driver_loaded_info_grep_return_empty_line(self, mocked_open):

        expected = {
            "Intel® Graphics Driver is loaded.": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "lsmod | grep i915",
                "Message": "Module i915 is not loaded.",
                "HowToFix": "Try to load the i915 module with the following command: modprobe i915.",
                "AutomationFix": "modprobe i915"
            }
        }
        lsmod_mock = MagicMock()
        lsmod_mock.wait.return_value = 0

        grep_mock = MagicMock()
        grep_mock.communicate.return_value = (
            "",
            None
        )
        grep_mock.returncode = 0

        mocked_open.side_effect = [lsmod_mock, grep_mock]

        value = {}
        oneapi_gpu_checker.get_i915_driver_loaded_info(value)

        self.assertEqual(expected, value)

    @patch("subprocess.Popen", side_effect=Exception("test message"))
    def test_get_i915_driver_loaded_info_subprocess_raise_exception(self, mocked_open):

        expected = {
            "Intel® Graphics Driver is loaded.": {
                "Value": "",
                "RetVal": "ERROR",
                "Command": "lsmod | grep i915",
                "Message": "test message",
                "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."  # noqa E501
            }
        }
        value = {}
        oneapi_gpu_checker.get_i915_driver_loaded_info(value)

        self.assertEqual(expected, value)


class TestGetIntelDeviceAvailableInfo(unittest.TestCase):

    @patch("checkers_py.linux.oneapi_gpu_checker.get_render_devices", return_value=["/dev/dri/renderD128"])
    def test_get_intel_device_available_info_positive(self, mocked_render_devices):
        expected = {
            "Intel Graphics Device is available": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "ls /dev/dri/ | grep renderD"
            }
        }

        value = {}
        oneapi_gpu_checker.get_intel_device_is_available_info(value)
        self.assertEqual(expected, value)

    @patch("checkers_py.linux.oneapi_gpu_checker.get_render_devices", return_value=[])
    def test_get_intel_device_available_info_negative(self, mocked_render_devices):
        expected = {
            "Intel Graphics Device is available": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "ls /dev/dri/ | grep renderD",
                "Message": "Intel Graphics Device is not detected.",
                "HowToFix": "Check if the graphics driver is installed."
            }
        }

        value = {}
        oneapi_gpu_checker.get_intel_device_is_available_info(value)
        self.assertEqual(expected, value)


class TestGetPermissionsToRenderInfo(unittest.TestCase):

    @patch("os.access", return_value=True)
    @patch("checkers_py.linux.oneapi_gpu_checker.get_render_devices", return_value=["/dev/dri/renderD128"])
    def test_get_permissions_to_render_info_positive(self, mocked_render_devices, mocked_access):
        expected = {
            "Render device accessible to current user.": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "ls -l /dev/dri/ | grep renderD"
            }
        }

        value = {}
        oneapi_gpu_checker.get_permissions_to_render_info(value)
        self.assertEqual(expected, value)

    @patch("os.access", return_value=False)
    @patch("checkers_py.linux.oneapi_gpu_checker.get_render_devices", return_value=["/dev/dri/renderD128"])
    def test_get_permissions_to_render_info_negative(self, mocked_render_devices, mocked_access):
        expected = {
            "Render device accessible to current user.": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "ls -l /dev/dri/ | grep renderD",
                "Message": "Current user does not have access to any render device.",
                "HowToFix": "Try to run the diagnostics with administrative privileges "
                            "or add user to render group.",
                "AutomationFix": "sudo gpasswd -a ${{USER}} render && newgrp render"
            }
        }

        value = {}
        oneapi_gpu_checker.get_permissions_to_render_info(value)
        self.assertEqual(expected, value)


class TestGetPermissionsToCardInfo(unittest.TestCase):

    @patch("os.access", return_value=True)
    @patch("checkers_py.linux.oneapi_gpu_checker.get_card_devices", return_value=["/dev/dri/card0"])
    def test_get_permissions_to_card_info_positive(self, mocked_render_devices, mocked_access):
        expected = {
            "Card device accessible to current user": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "ls -l /dev/dri/ | grep card"
            }
        }

        value = {}
        oneapi_gpu_checker.get_permissions_to_card_info(value)
        self.assertEqual(expected, value)

    @patch("os.access", return_value=False)
    @patch("checkers_py.linux.oneapi_gpu_checker.get_card_devices", return_value=["/dev/dri/card0"])
    def test_get_permissions_to_card_info_negative(self, mocked_render_devices, mocked_access):
        expected = {
            "Card device accessible to current user": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "ls -l /dev/dri/ | grep card",
                "Message": "Current user does not have access to any card device.",
                "HowToFix": "Try to run the diagnostics with administrative privileges "
                            "or check if the graphics driver is installed."
            }
        }

        value = {}
        oneapi_gpu_checker.get_permissions_to_card_info(value)
        self.assertEqual(expected, value)


class TestGetDmesgI915InitErrorsInfo(unittest.TestCase):

    @patch("subprocess.Popen")
    def test_get_dmesg_i915_init_errors_info_dmesg_return_code_is_not_zero(self, mocked_open):
        expected = {
            "dmesg doesn't contain i915 errors": {
                "Value": "",
                "RetVal": "ERROR",
                "Command": "dmesg -T | grep i915 | grep failed",
                "Message": "Cannot get information about timestamp from the kernel ring buffer.",
                "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."  # noqa E501
            }
        }
        dmesg_mock = MagicMock()
        dmesg_mock.wait.return_value = (None, None)
        dmesg_mock.returncode = 1

        mocked_open.return_value = dmesg_mock

        value = {}
        oneapi_gpu_checker.get_dmesg_i915_init_errors_info(value)

        self.assertEqual(expected, value)

    @patch("subprocess.Popen")
    def test_get_dmesg_i915_init_errors_info_grep_return_code_is_not_zero_or_one(self, mocked_open):
        expected = {
            "dmesg doesn't contain i915 errors": {
                "Value": "",
                "RetVal": "ERROR",
                "Command": "dmesg -T | grep i915 | grep failed",
                "Message": "Cannot get information about i915 initialization errors.",
                "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."  # noqa E501
            }
        }
        dmesg_mock = MagicMock()
        dmesg_mock.wait.return_value = 0

        grep_mock = MagicMock()
        grep_mock.communicate.return_value = (None, None)
        grep_mock.returncode = 2

        mocked_open.side_effect = [dmesg_mock, grep_mock]

        value = {}
        oneapi_gpu_checker.get_dmesg_i915_init_errors_info(value)

        self.assertEqual(expected, value)

    @patch("subprocess.Popen")
    def test_get_dmesg_i915_init_errors_info_with_initialization_errors(self, mocked_open):
        self.maxDiff = None
        expected = {
            "dmesg doesn't contain i915 errors": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "dmesg -T | grep i915 | grep failed",
                "Message": "Initialization errors seen in i915 driver.",
                "HowToFix": "Check related dmesg logs above for more details.",
                "Logs": [
                    " [    2.451145] i915 0000:03:00.0: Device initialization failed (-19)"
                ]
            }
        }
        dmesg_mock = MagicMock()
        dmesg_mock.wait.return_value = 0

        grep_mock = MagicMock()
        grep_mock.communicate.return_value = (
            " [    2.451138] i915 0000:03:00.0: [drm] *ERROR* LMEM not initialized by firmware\n"
            " [    2.451145] i915 0000:03:00.0: Device initialization failed (-19)",
            None)

        grep_mock.returncode = 0

        mocked_open.side_effect = [dmesg_mock, grep_mock]

        value = {}
        oneapi_gpu_checker.get_dmesg_i915_init_errors_info(value)

        self.assertEqual(expected, value)

    @patch("subprocess.Popen")
    def test_get_dmesg_i915_init_errors_info_without_initialization_errors(self, mocked_open):
        expected = {
            "dmesg doesn't contain i915 errors": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "dmesg -T | grep i915 | grep failed"
            }
        }

        dmesg_mock = MagicMock()
        dmesg_mock.wait.return_value = 0

        grep_mock = MagicMock()
        grep_mock.communicate.return_value = (
            " [    3.291005] [drm] Initialized i915 1.6.0 20201103 for 0000:03:00.0 on minor 0",
            None)

        grep_mock.returncode = 0

        mocked_open.side_effect = [dmesg_mock, grep_mock]

        value = {}
        oneapi_gpu_checker.get_dmesg_i915_init_errors_info(value)

        self.assertEqual(expected, value)


class TestGetGpuErrorsInfo(unittest.TestCase):

    @patch("subprocess.Popen")
    def test_get_gpu_errors_info_dmesg_return_code_is_not_zero(self, mocked_open):
        expected = {
            "dmesg doesn't contain user errors related to GPU operations": {
                "Value": "",
                "RetVal": "ERROR",
                "Command": "dmesg -T | grep -e HANG -e hang -e dump -e reassign -e blocked -e task: -e "
                           "Please -e segfault | tail -20",
                "Message": "Cannot get information about timestamp from the kernel ring buffer.",
                "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."  # noqa E501
            }
        }

        dmesg_mock = MagicMock()
        dmesg_mock.wait.return_value = (None, None)
        dmesg_mock.returncode = 1

        mocked_open.return_value = dmesg_mock

        value = {}
        oneapi_gpu_checker.get_gpu_errors_info(value)

        self.assertEqual(expected, value)

    @patch("subprocess.Popen")
    def test_get_gpu_errors_info_grep_return_code_is_not_zero_or_one(self, mocked_open):
        expected = {
            "dmesg doesn't contain user errors related to GPU operations": {
                "Value": "",
                "RetVal": "ERROR",
                "Command": "dmesg -T | grep -e HANG -e hang -e dump -e reassign -e blocked -e task: -e "
                           "Please -e segfault | tail -20",
                "Message": "Cannot get information about i915 usage errors.",
                "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."  # noqa E501
            }
        }

        dmesg_mock = MagicMock()
        dmesg_mock.wait.return_value = 0

        grep_mock = MagicMock()
        grep_mock.wait.return_value = 2

        tail_mock = MagicMock()
        tail_mock.communicate.return_value = (None, None)
        tail_mock.returncode = 1

        mocked_open.side_effect = [dmesg_mock, grep_mock, tail_mock]

        value = {}
        oneapi_gpu_checker.get_gpu_errors_info(value)

        self.assertEqual(expected, value)

    @patch("subprocess.Popen")
    def test_get_gpu_errors_info_tail_return_code_is_not_zero(self, mocked_open):
        expected = {
            "dmesg doesn't contain user errors related to GPU operations": {
                "Value": "",
                "RetVal": "ERROR",
                "Command": "dmesg -T | grep -e HANG -e hang -e dump -e reassign -e blocked -e task: -e "
                           "Please -e segfault | tail -20",
                "Message": "Cannot get information about the last i915 usage errors.",
                "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."  # noqa E501
            }
        }

        dmesg_mock = MagicMock()
        dmesg_mock.wait.return_value = 0

        grep_mock = MagicMock()
        grep_mock.wait.return_value = 0

        tail_mock = MagicMock()
        tail_mock.communicate.return_value = (None, None)
        tail_mock.returncode = 1

        mocked_open.side_effect = [dmesg_mock, grep_mock, tail_mock]

        value = {}
        oneapi_gpu_checker.get_gpu_errors_info(value)

        self.assertEqual(expected, value)

    @patch("subprocess.Popen")
    def test_get_gpu_errors_info_tail_with_errors(self, mocked_open):
        expected = {
            "dmesg doesn't contain user errors related to GPU operations": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "dmesg -T | grep -e HANG -e hang -e dump -e reassign -e blocked -e task: -e "
                           "Please -e segfault | tail -20",
                "Message": "Found i915 usage errors.",
                "HowToFix": "Check related dmesg logs above for more details.",
                "Logs": [
                    "[248947.306671] [drm] GPU HANG: ecode 9:1:0xeeffefa1, in Xorg [551],"
                    " reason: Hang on bcs0, action: reset"
                ]
            }
        }

        dmesg_mock = MagicMock()
        dmesg_mock.wait.return_value = 0

        grep_mock = MagicMock()
        grep_mock.wait.return_value = 0

        tail_mock = MagicMock()
        tail_mock.communicate.return_value = (
            "[248947.306671] [drm] GPU HANG: ecode 9:1:0xeeffefa1, in Xorg [551],"
            " reason: Hang on bcs0, action: reset",
            None)
        tail_mock.returncode = 0

        mocked_open.side_effect = [dmesg_mock, grep_mock, tail_mock]

        value = {}
        oneapi_gpu_checker.get_gpu_errors_info(value)

        self.assertEqual(expected, value)

    @patch("subprocess.Popen")
    def test_get_gpu_errors_info_tail_without_errors(self, mocked_open):
        expected = {
            "dmesg doesn't contain user errors related to GPU operations": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "dmesg -T | grep -e HANG -e hang -e dump -e reassign -e blocked -e task: -e "
                           "Please -e segfault | tail -20"
            }
        }

        dmesg_mock = MagicMock()
        dmesg_mock.wait.return_value = 0

        grep_mock = MagicMock()
        grep_mock.wait.return_value = 0

        tail_mock = MagicMock()
        tail_mock.communicate.return_value = (
            "",
            None)
        tail_mock.returncode = 0

        mocked_open.side_effect = [dmesg_mock, grep_mock, tail_mock]

        value = {}
        oneapi_gpu_checker.get_gpu_errors_info(value)

        self.assertEqual(expected, value)


@patch("checkers_py.linux.oneapi_gpu_checker.TMP_MATMUL_FILE", "matmul")
@patch("checkers_py.linux.oneapi_gpu_checker.PATH_TO_SOURCE_OFFLOAD", "../oneapi_check_offloads")
class TestCompileTestMatmul(unittest.TestCase):

    @patch("subprocess.Popen")
    def test__compile_test_matmul_positive(self, mocked_open):
        expected = {
            "Compile test matmul": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                           "../oneapi_check_offloads/matmul_offload.cpp -o matmul"
            }
        }
        expected_error_code = 0

        compile_mock = MagicMock()
        compile_mock.wait.return_value = 0

        mocked_open.return_value = compile_mock

        value = {}
        error_code = oneapi_gpu_checker._compile_test_matmul(value)
        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)

    @patch("subprocess.Popen")
    def test__compile_test_matmul_icpx_return_not_zero(self, mocked_open):
        expected = {
            "Compile test matmul": {
                    "Value": "",
                    "RetVal": "FAIL",
                    "Command": "icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                               "../oneapi_check_offloads/matmul_offload.cpp -o matmul",
                    "Message": "Non zero return code from command: "
                               "'icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                               "../oneapi_check_offloads/matmul_offload.cpp -o matmul'",
                    "HowToFix": "Check compiled source file for syntax errors."
            }
        }
        expected_error_code = 1

        compile_mock = MagicMock()
        compile_mock.wait.return_value = (None, None)
        compile_mock.returncode = 1

        mocked_open.return_value = compile_mock

        value = {}
        error_code = oneapi_gpu_checker._compile_test_matmul(value)
        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)

    @patch("subprocess.Popen", side_effect=Exception("test"))
    def test__compile_test_matmul_raised_exception(self, mocked_open):
        expected = {
            "Compile test matmul": {
                "Value": "",
                "RetVal": "ERROR",
                "Command": "icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                           "../oneapi_check_offloads/matmul_offload.cpp -o matmul",
                "Message": "Matmul compilation failed - icpx not found.",
                "HowToFix": "Try to: " \
                           "1) install Intel® C++ Compiler based on " \
                           "https://www.intel.com/content/www/us/en/developer/articles/tool/oneapi-standalone-components.html " \
                           "2) set required variable by running: source /opt/intel/oneapi/setvars.sh"  # noqa E501
                }
        }
        expected_error_code = 1

        value = {}
        error_code = oneapi_gpu_checker._compile_test_matmul(value)
        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)


@patch("checkers_py.linux.oneapi_gpu_checker.TMP_MATMUL_FILE", "matmul")
class TestRunTestMatmul(unittest.TestCase):

    @patch("subprocess.Popen")
    def test__run_test_matmul_positive(self, mocked_open):

        expected = {
            "Test simple matrix multiplication with Intel® oneAPI Level Zero.": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 matmul"
            },
            "Test simple matrix multiplication with OpenCL™.": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL matmul"
            }
        }
        expected_error_code = 0
        status = 0

        level_zero_mock = MagicMock()
        level_zero_mock.communicate.return_value = ("PASSED", None)
        level_zero_mock.returncode = 0

        opencl_mock = MagicMock()
        opencl_mock.communicate.return_value = ("PASSED", None)
        opencl_mock.returncode = 0

        mocked_open.side_effect = [level_zero_mock, opencl_mock]

        value = {}
        error_code = oneapi_gpu_checker._run_test_matmul(status, value)
        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)

    def test__run_test_matmul_status_is_not_zero(self):

        expected = {
            "Test simple matrix multiplication with Intel® oneAPI Level Zero.": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 matmul",
                "Message": "Check failed because compile test matmul failed.",
                "HowToFix": "Check compiled source file for syntax errors."
            },
            "Test simple matrix multiplication with OpenCL™.": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL matmul",
                "Message": "Check failed because compile test matmul failed.",
                "HowToFix": "Check compiled source file for syntax errors."
            }
        }
        expected_error_code = 1
        status = 1

        value = {}
        error_code = oneapi_gpu_checker._run_test_matmul(status, value)
        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)

    @patch("subprocess.Popen")
    def test__run_test_matmul_level_zero_return_code_is_not_zero(self, mocked_open):
        expected = {
            "Test simple matrix multiplication with Intel® oneAPI Level Zero.": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 matmul",
                "Message": "An error occurred while running matmul. ExitCode: 1",
                "HowToFix": "Look into output for more details: \n"
            },
            "Test simple matrix multiplication with OpenCL™.": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL matmul"
            }
        }

        expected_error_code = 1
        status = 0

        level_zero_mock = MagicMock()
        level_zero_mock.communicate.return_value = ("", None)
        level_zero_mock.returncode = 1

        opencl_mock = MagicMock()
        opencl_mock.communicate.return_value = ("PASSED", None)
        opencl_mock.returncode = 0

        mocked_open.side_effect = [level_zero_mock, opencl_mock]

        value = {}
        error_code = oneapi_gpu_checker._run_test_matmul(status, value)
        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)

    @patch("subprocess.Popen")
    def test__run_test_matmul_opencl_return_code_is_not_zero(self, mocked_open):
        expected = {
            "Test simple matrix multiplication with Intel® oneAPI Level Zero.": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 matmul"
            },
            "Test simple matrix multiplication with OpenCL™.": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL matmul",
                "Message": "An error occurred while running matmul. ExitCode: 1",
                "HowToFix": "Look into output for more details: \n"
            }
        }

        expected_error_code = 1
        status = 0

        level_zero_mock = MagicMock()
        level_zero_mock.communicate.return_value = ("PASSED", None)
        level_zero_mock.returncode = 0

        opencl_mock = MagicMock()
        opencl_mock.communicate.return_value = ("", None)
        opencl_mock.returncode = 1

        mocked_open.side_effect = [level_zero_mock, opencl_mock]

        value = {}
        error_code = oneapi_gpu_checker._run_test_matmul(status, value)
        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)

    @patch("subprocess.Popen")
    def test__run_test_matmul_level_zero_and_opencl_return_code_is_not_zero(self, mocked_open):
        expected = {
            "Test simple matrix multiplication with Intel® oneAPI Level Zero.": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 matmul",
                "Message": "An error occurred while running matmul. ExitCode: 1",
                "HowToFix": "Look into output for more details: \n"
            },
            "Test simple matrix multiplication with OpenCL™.": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL matmul",
                "Message": "An error occurred while running matmul. ExitCode: 1",
                "HowToFix": "Look into output for more details: \n"
            }
        }

        expected_error_code = 2
        status = 0

        level_zero_mock = MagicMock()
        level_zero_mock.communicate.return_value = ("", None)
        level_zero_mock.returncode = 1

        opencl_mock = MagicMock()
        opencl_mock.communicate.return_value = ("", None)
        opencl_mock.returncode = 1

        mocked_open.side_effect = [level_zero_mock, opencl_mock]

        value = {}
        error_code = oneapi_gpu_checker._run_test_matmul(status, value)
        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)


@patch("checkers_py.linux.oneapi_gpu_checker.TMP_BINOPTION_FILE", "binoption")
@patch("checkers_py.linux.oneapi_gpu_checker.PATH_TO_SOURCE_OFFLOAD", "../oneapi_check_offloads")
class TestCompileTestBinoption(unittest.TestCase):

    @patch("subprocess.Popen")
    def test__compile_test_binoption_positive(self, mocked_open):
        expected = {
            "Compile test binoption": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                           "../oneapi_check_offloads/binoption_standalone.cpp -o binoption"
            }
        }

        expected_error_code = 0

        compile_mock = MagicMock()
        compile_mock.wait.return_value = 0

        mocked_open.return_value = compile_mock

        value = {}
        error_code = oneapi_gpu_checker._compile_test_binoption(value)

        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)

    @patch("subprocess.Popen")
    def test__compile_test_binoption_icpx_return_not_zero(self, mocked_open):
        expected = {
            "Compile test binoption": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                           "../oneapi_check_offloads/binoption_standalone.cpp -o binoption",
                "Message": "Non zero return code from command: "
                           "'icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                           "../oneapi_check_offloads/binoption_standalone.cpp -o binoption'",
                "HowToFix": "Check compiled source file for syntax errors."
            }
        }
        expected_error_code = 1

        compile_mock = MagicMock()
        compile_mock.wait.return_value = (None, None)
        compile_mock.returncode = 1

        mocked_open.return_value = compile_mock

        value = {}
        error_code = oneapi_gpu_checker._compile_test_binoption(value)

        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)

    @patch("subprocess.Popen", side_effect=Exception("test"))
    def test__compile_test_binoption_raised_exception(self, mocked_open):
        expected = {
            "Compile test binoption": {
                "Value": "",
                "RetVal": "ERROR",
                "Command": "icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                           "../oneapi_check_offloads/binoption_standalone.cpp -o binoption",
                "Message": "Binoption compilation failed - icpx not found.",
                "HowToFix": "Try to: " \
                           "1) install Intel® C++ Compiler based on " \
                           "https://www.intel.com/content/www/us/en/developer/articles/tool/oneapi-standalone-components.html " \
                           "2) set required variable by running: source /opt/intel/oneapi/setvars.sh"  # noqa E501
                }
        }
        expected_error_code = 1

        value = {}
        error_code = oneapi_gpu_checker._compile_test_binoption(value)

        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)


@patch("checkers_py.linux.oneapi_gpu_checker.TMP_BINOPTION_FILE", "binoption")
class TestRunTestBinoption(unittest.TestCase):

    @patch("subprocess.Popen")
    def test__run_test_binoption_positive(self, mocked_open):

        expected = {
            "Test simple binary options program with Intel® oneAPI Level Zero.": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 binoption"
            },
            "Test simple binary options program with OpenCL™.": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL binoption"
            }
        }
        expected_error_code = 0
        status = 0

        level_zero_mock = MagicMock()
        level_zero_mock.communicate.return_value = ("PASSED", None)
        level_zero_mock.returncode = 0

        opencl_mock = MagicMock()
        opencl_mock.communicate.return_value = ("PASSED", None)
        opencl_mock.returncode = 0

        mocked_open.side_effect = [level_zero_mock, opencl_mock]

        value = {}
        error_code = oneapi_gpu_checker._run_test_binoption(status, value)

        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)

    def test__run_test_binoption_status_is_not_zero(self):

        expected = {
            "Test simple binary options program with Intel® oneAPI Level Zero.": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 binoption",
                "Message": "Check failed because compile test binoption failed.",
                "HowToFix": "Check compiled source file for syntax errors."

            },
            "Test simple binary options program with OpenCL™.": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL binoption",
                "Message": "Check failed because compile test binoption failed.",
                "HowToFix": "Check compiled source file for syntax errors."
            }
        }
        expected_error_code = 1
        status = 1

        value = {}
        error_code = oneapi_gpu_checker._run_test_binoption(status, value)

        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)

    @patch("subprocess.Popen")
    def test__run_test_binoption_level_zero_return_code_is_not_zero(self, mocked_open):
        expected = {
            "Test simple binary options program with Intel® oneAPI Level Zero.": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 binoption",
                "Message": "An error occurred while running binoption. ExitCode: 1",
                "HowToFix": "Look into output for more details: \n"
            },
            "Test simple binary options program with OpenCL™.": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL binoption"
            }
        }

        expected_error_code = 1
        status = 0

        level_zero_mock = MagicMock()
        level_zero_mock.communicate.return_value = ("", None)
        level_zero_mock.returncode = 1

        opencl_mock = MagicMock()
        opencl_mock.communicate.return_value = ("PASSED", None)
        opencl_mock.returncode = 0

        mocked_open.side_effect = [level_zero_mock, opencl_mock]

        value = {}
        error_code = oneapi_gpu_checker._run_test_binoption(status, value)

        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)

    @patch("subprocess.Popen")
    def test__run_test_binoption_opencl_return_code_is_not_zero(self, mocked_open):
        expected = {
            "Test simple binary options program with Intel® oneAPI Level Zero.": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 binoption"
            },
            "Test simple binary options program with OpenCL™.": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL binoption",
                "Message": "An error occurred while running binoption. ExitCode: 1",
                "HowToFix": "Look into output for more details: \n"
            }
        }

        expected_error_code = 1
        status = 0

        level_zero_mock = MagicMock()
        level_zero_mock.communicate.return_value = ("PASSED", None)
        level_zero_mock.returncode = 0

        opencl_mock = MagicMock()
        opencl_mock.communicate.return_value = ("", None)
        opencl_mock.returncode = 1

        mocked_open.side_effect = [level_zero_mock, opencl_mock]

        value = {}
        error_code = oneapi_gpu_checker._run_test_binoption(status, value)

        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)

    @patch("subprocess.Popen")
    def test__run_test_binoption_level_zero_and_opencl_return_code_is_not_zero(self, mocked_open):
        expected = {
            "Test simple binary options program with Intel® oneAPI Level Zero.": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 binoption",
                "Message": "An error occurred while running binoption. ExitCode: 1",
                "HowToFix": "Look into output for more details: \n"
            },
            "Test simple binary options program with OpenCL™.": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL binoption",
                "Message": "An error occurred while running binoption. ExitCode: 1",
                "HowToFix": "Look into output for more details: \n"
            }
        }

        expected_error_code = 2
        status = 0

        level_zero_mock = MagicMock()
        level_zero_mock.communicate.return_value = ("", None)
        level_zero_mock.returncode = 1

        opencl_mock = MagicMock()
        opencl_mock.communicate.return_value = ("", None)
        opencl_mock.returncode = 1

        mocked_open.side_effect = [level_zero_mock, opencl_mock]

        value = {}
        error_code = oneapi_gpu_checker._run_test_binoption(status, value)

        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)


class TestGetOpenmpOffloadInfo(unittest.TestCase):

    @patch("checkers_py.linux.oneapi_gpu_checker._run_test_binoption")
    @patch("checkers_py.linux.oneapi_gpu_checker._compile_test_binoption")
    @patch("checkers_py.linux.oneapi_gpu_checker._run_test_matmul")
    @patch("checkers_py.linux.oneapi_gpu_checker._compile_test_matmul")
    def test_get_openmp_offload_info_positive(self, mocked_compile_matmul, mocked_run_matmul,
                                              mocked_compile_binoption, mocked_run_binoption):
        expected = {
            "OpenMP GPU pipeline tests": {
                "Value": {
                    "Compile test matmul": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                                   "../oneapi_check_offloads/matmul_offload.cpp -o matmul"
                    },
                    "Test simple matrix multiplication with Intel® oneAPI Level Zero.": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 matmul"
                    },
                    "Test simple matrix multiplication with OpenCL™.": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL matmul"
                    },
                    "Compile test binoption": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                                   "../oneapi_check_offloads/binoption_standalone.cpp -o binoption"
                    },
                    "Test simple binary options program with Intel® oneAPI Level Zero.": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 binoption"
                    },
                    "Test simple binary options program with OpenCL™.": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL binoption"
                    }
                },
                "RetVal": "PASS"
            }
        }

        def side_effect_compile_matmul(node):
            node.update({
                "Compile test matmul": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                               "../oneapi_check_offloads/matmul_offload.cpp -o matmul"
                }
            })
            return 0

        mocked_compile_matmul.side_effect = side_effect_compile_matmul

        def side_effect_run_matmul(status, node):
            node.update({
                "Test simple matrix multiplication with Intel® oneAPI Level Zero.": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 matmul"
                },
                "Test simple matrix multiplication with OpenCL™.": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL matmul"
                }
            })
            return status

        mocked_run_matmul.side_effect = side_effect_run_matmul

        def side_effect_compile_binoption(node):
            node.update({
                "Compile test binoption": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                               "../oneapi_check_offloads/binoption_standalone.cpp -o binoption"
                }
            })
            return 0

        mocked_compile_binoption.side_effect = side_effect_compile_binoption

        def side_effect_run_binoption(status, node):
            node.update({
                "Test simple binary options program with Intel® oneAPI Level Zero.": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 binoption"
                },
                "Test simple binary options program with OpenCL™.": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL binoption"
                }
                })
            return status

        mocked_run_binoption.side_effect = side_effect_run_binoption

        value = {}
        oneapi_gpu_checker.get_openmp_offload_info(value)
        self.assertEqual(expected, value)

    @patch("checkers_py.linux.oneapi_gpu_checker._run_test_binoption")
    @patch("checkers_py.linux.oneapi_gpu_checker._compile_test_binoption")
    @patch("checkers_py.linux.oneapi_gpu_checker._run_test_matmul")
    @patch("checkers_py.linux.oneapi_gpu_checker._compile_test_matmul")
    def test_get_openmp_offload_info_compile_matmul_failed(self, mocked_compile_matmul, mocked_run_matmul,
                                                           mocked_compile_binoption, mocked_run_binoption):
        expected = {
            "OpenMP GPU pipeline tests": {
                "Value": {
                    "Compile test matmul": {
                        "Value": "",
                        "RetVal": "FAIL",
                        "Command": "icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                                   "../oneapi_check_offloads/matmul_offload.cpp -o matmul",
                        "Message": "Non zero return code from command: "
                                   "'icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                                   "../oneapi_check_offloads/matmul_offload.cpp -o matmul'"
                    },
                    "Test simple matrix multiplication with Intel® oneAPI Level Zero.": {
                        "Value": "",
                        "RetVal": "FAIL",
                        "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 matmul",
                        "Message": "Check failed because compile test matmul failed."
                    },
                    "Test simple matrix multiplication with OpenCL™.": {
                        "Value": "",
                        "RetVal": "FAIL",
                        "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL matmul",
                        "Message":  "Check failed because compile test matmul failed."
                    },
                    "Compile test binoption": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                                   "../oneapi_check_offloads/binoption_standalone.cpp -o binoption"
                    },
                    "Test simple binary options program with Intel® oneAPI Level Zero.": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 binoption"
                    },
                    "Test simple binary options program with OpenCL™.": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL binoption"
                    }
                },
                "RetVal": "FAIL",
                "Message": "Some checks below failed.",
                "HowToFix": "Review output of checks for more details."
            }
        }

        def side_effect_compile_matmul(node):
            node.update({
                "Compile test matmul": {
                    "Value": "",
                    "RetVal": "FAIL",
                    "Command": "icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                               "../oneapi_check_offloads/matmul_offload.cpp -o matmul",
                    "Message": "Non zero return code from command: "
                               "'icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                               "../oneapi_check_offloads/matmul_offload.cpp -o matmul'"
                    }
            })
            return 1

        mocked_compile_matmul.side_effect = side_effect_compile_matmul

        def side_effect_run_matmul(status, node):
            node.update({
                "Test simple matrix multiplication with Intel® oneAPI Level Zero.": {
                    "Value": "",
                    "RetVal": "FAIL",
                    "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 matmul",
                    "Message": "Check failed because compile test matmul failed."
                },
                "Test simple matrix multiplication with OpenCL™.": {
                    "Value": "",
                    "RetVal": "FAIL",
                    "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL matmul",
                    "Message": "Check failed because compile test matmul failed."
                }
            })
            return 2

        mocked_run_matmul.side_effect = side_effect_run_matmul

        def side_effect_compile_binoption(node):
            node.update({
                "Compile test binoption": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                               "../oneapi_check_offloads/binoption_standalone.cpp -o binoption"
                }
            })
            return 0

        mocked_compile_binoption.side_effect = side_effect_compile_binoption

        def side_effect_run_binoption(status, node):
            node.update({
                "Test simple binary options program with Intel® oneAPI Level Zero.": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 binoption"
                },
                "Test simple binary options program with OpenCL™.": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL binoption"
                }
                })
            return status

        mocked_run_binoption.side_effect = side_effect_run_binoption

        value = {}
        oneapi_gpu_checker.get_openmp_offload_info(value)
        self.assertEqual(expected, value)

    @patch("checkers_py.linux.oneapi_gpu_checker._run_test_binoption")
    @patch("checkers_py.linux.oneapi_gpu_checker._compile_test_binoption")
    @patch("checkers_py.linux.oneapi_gpu_checker._run_test_matmul")
    @patch("checkers_py.linux.oneapi_gpu_checker._compile_test_matmul")
    def test_get_openmp_offload_info_compile_matmul_raised_exception(self, mocked_compile_matmul,
                                                                     mocked_run_matmul,
                                                                     mocked_compile_binoption,
                                                                     mocked_run_binoption):
        expected = {
            "OpenMP GPU pipeline tests": {
                "Value": {
                    "Compile test matmul": {
                        "Value": "",
                        "RetVal": "ERROR",
                        "Command": "icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                                   "../oneapi_check_offloads/matmul_offload.cpp -o matmul",
                        "Message": "icpx not found"
                    },
                    "Test simple matrix multiplication with Intel® oneAPI Level Zero.": {
                        "Value": "",
                        "RetVal": "FAIL",
                        "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 matmul",
                        "Message":  "Check failed because compile test matmul failed."
                    },
                    "Test simple matrix multiplication with OpenCL™.": {
                        "Value": "",
                        "RetVal": "FAIL",
                        "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL matmul",
                        "Message":  "Check failed because compile test matmul failed."
                    },
                    "Compile test binoption": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                                   "../oneapi_check_offloads/binoption_standalone.cpp -o binoption"
                    },
                    "Test simple binary options program with Intel® oneAPI Level Zero.": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 binoption"
                    },
                    "Test simple binary options program with OpenCL™.": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL binoption"
                    }
                },
                "RetVal": "FAIL",
                "Message": "Some checks below failed.",
                "HowToFix": "Review output of checks for more details."
            }
        }

        def side_effect_compile_matmul(node):
            node.update({
                "Compile test matmul": {
                    "Value": "",
                    "RetVal": "ERROR",
                    "Command": "icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                               "../oneapi_check_offloads/matmul_offload.cpp -o matmul",
                    "Message": "icpx not found"
                    }
            })
            return 1

        mocked_compile_matmul.side_effect = side_effect_compile_matmul

        def side_effect_run_matmul(status, node):
            node.update({
                "Test simple matrix multiplication with Intel® oneAPI Level Zero.": {
                    "Value": "",
                    "RetVal": "FAIL",
                    "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 matmul",
                    "Message":  "Check failed because compile test matmul failed."
                },
                "Test simple matrix multiplication with OpenCL™.": {
                    "Value": "",
                    "RetVal": "FAIL",
                    "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL matmul",
                    "Message":  "Check failed because compile test matmul failed."
                }
            })
            return status

        mocked_run_matmul.side_effect = side_effect_run_matmul

        def side_effect_compile_binoption(node):
            node.update({
                "Compile test binoption": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                               "../oneapi_check_offloads/binoption_standalone.cpp -o binoption"
                }
            })
            return 0

        mocked_compile_binoption.side_effect = side_effect_compile_binoption

        def side_effect_run_binoption(status, node):
            node.update({
                "Test simple binary options program with Intel® oneAPI Level Zero.": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 binoption"
                },
                "Test simple binary options program with OpenCL™.": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL binoption"
                }
                })
            return status

        mocked_run_binoption.side_effect = side_effect_run_binoption

        value = {}
        oneapi_gpu_checker.get_openmp_offload_info(value)
        self.assertEqual(expected, value)

    @patch("checkers_py.linux.oneapi_gpu_checker._run_test_binoption")
    @patch("checkers_py.linux.oneapi_gpu_checker._compile_test_binoption")
    @patch("checkers_py.linux.oneapi_gpu_checker._run_test_matmul")
    @patch("checkers_py.linux.oneapi_gpu_checker._compile_test_matmul")
    def test_get_openmp_offload_info_compile_binoption_failed(self, mocked_compile_matmul, mocked_run_matmul,
                                                              mocked_compile_binoption, mocked_run_binoption):
        expected = {
            "OpenMP GPU pipeline tests": {
                "Value": {
                    "Compile test matmul": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                                   "../oneapi_check_offloads/matmul_offload.cpp -o matmul"
                    },
                    "Test simple matrix multiplication with Intel® oneAPI Level Zero.": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 matmul"
                    },
                    "Test simple matrix multiplication with OpenCL™.": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL matmul"
                    },
                    "Compile test binoption": {
                        "Value": "",
                        "RetVal": "FAIL",
                        "Command": "icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                                   "../oneapi_check_offloads/binoption_standalone.cpp -o binoption",
                        "Message": "Non zero return code from command: "
                                   "'icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                                   "../oneapi_check_offloads/binoption_standalone.cpp -o binoption'"
                    },
                    "Test simple binary options program with Intel® oneAPI Level Zero.": {
                        "Value": "",
                        "RetVal": "FAIL",
                        "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 binoption",
                        "Message": "Check failed because compile test binoption failed."
                    },
                    "Test simple binary options program with OpenCL™.": {
                        "Value": "",
                        "RetVal": "FAIL",
                        "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL binoption",
                        "Message": "Check failed because compile test binoption failed."
                    }
                },
                "RetVal": "FAIL",
                "Message": "Some checks below failed.",
                "HowToFix": "Review output of checks for more details."
            }
        }

        def side_effect_compile_matmul(node):
            node.update({
                "Compile test matmul": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                               "../oneapi_check_offloads/matmul_offload.cpp -o matmul"
                }
            })
            return 0

        mocked_compile_matmul.side_effect = side_effect_compile_matmul

        def side_effect_run_matmul(status, node):
            node.update({
                "Test simple matrix multiplication with Intel® oneAPI Level Zero.": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 matmul"
                },
                "Test simple matrix multiplication with OpenCL™.": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL matmul"
                }
            })
            return status

        mocked_run_matmul.side_effect = side_effect_run_matmul

        def side_effect_compile_binoption(node):
            node.update({
                "Compile test binoption": {
                    "Value": "",
                    "RetVal": "FAIL",
                    "Command": "icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                               "../oneapi_check_offloads/binoption_standalone.cpp -o binoption",
                    "Message": "Non zero return code from command: "
                               "'icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                               "../oneapi_check_offloads/binoption_standalone.cpp -o binoption'"
                }
            })
            return 1

        mocked_compile_binoption.side_effect = side_effect_compile_binoption

        def side_effect_run_binoption(status, node):
            node.update({
                "Test simple binary options program with Intel® oneAPI Level Zero.": {
                    "Value": "",
                    "RetVal": "FAIL",
                    "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 binoption",
                    "Message": "Check failed because compile test binoption failed."
                },
                "Test simple binary options program with OpenCL™.": {
                    "Value": "",
                    "RetVal": "FAIL",
                    "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL binoption",
                    "Message": "Check failed because compile test binoption failed."
                }
                })
            return status

        mocked_run_binoption.side_effect = side_effect_run_binoption

        value = {}
        oneapi_gpu_checker.get_openmp_offload_info(value)
        self.assertEqual(expected, value)

    @patch("checkers_py.linux.oneapi_gpu_checker._run_test_binoption")
    @patch("checkers_py.linux.oneapi_gpu_checker._compile_test_binoption")
    @patch("checkers_py.linux.oneapi_gpu_checker._run_test_matmul")
    @patch("checkers_py.linux.oneapi_gpu_checker._compile_test_matmul")
    def test_get_openmp_offload_info_compile_binoption_raised_exception(self, mocked_compile_matmul,
                                                                        mocked_run_matmul,
                                                                        mocked_compile_binoption,
                                                                        mocked_run_binoption):
        expected = {
            "OpenMP GPU pipeline tests": {
                "Value": {
                    "Compile test matmul": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                                   "../oneapi_check_offloads/matmul_offload.cpp -o matmul"
                    },
                    "Test simple matrix multiplication with Intel® oneAPI Level Zero.": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 matmul"
                    },
                    "Test simple matrix multiplication with OpenCL™.": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL matmul"
                    },
                    "Compile test binoption": {
                        "Value": "",
                        "RetVal": "ERROR",
                        "Command": "icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                                   "../oneapi_check_offloads/binoption_standalone.cpp -o binoption",
                        "Message": "icpx not found"
                    },
                    "Test simple binary options program with Intel® oneAPI Level Zero.": {
                        "Value": "",
                        "RetVal": "FAIL",
                        "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 binoption",
                        "Message": "Check failed because compile test binoption failed."
                    },
                    "Test simple binary options program with OpenCL™.": {
                        "Value": "",
                        "RetVal": "FAIL",
                        "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL binoption",
                        "Message": "Check failed because compile test binoption failed."
                    }
                },
                "RetVal": "FAIL",
                "Message": "Some checks below failed.",
                "HowToFix": "Review output of checks for more details."
            }
        }

        def side_effect_compile_matmul(node):
            node.update({
                "Compile test matmul": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                               "../oneapi_check_offloads/matmul_offload.cpp -o matmul"
                }
            })
            return 0

        mocked_compile_matmul.side_effect = side_effect_compile_matmul

        def side_effect_run_matmul(status, node):
            node.update({
                "Test simple matrix multiplication with Intel® oneAPI Level Zero.": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 matmul"
                },
                "Test simple matrix multiplication with OpenCL™.": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL matmul"
                }
            })
            return status

        mocked_run_matmul.side_effect = side_effect_run_matmul

        def side_effect_compile_binoption(node):
            node.update({
                "Compile test binoption": {
                    "Value": "",
                    "RetVal": "ERROR",
                    "Command": "icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                               "../oneapi_check_offloads/binoption_standalone.cpp -o binoption",
                    "Message": "icpx not found"
                }
            })
            return 1

        mocked_compile_binoption.side_effect = side_effect_compile_binoption

        def side_effect_run_binoption(status, node):
            node.update({
                "Test simple binary options program with Intel® oneAPI Level Zero.": {
                    "Value": "",
                    "RetVal": "FAIL",
                    "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 binoption",
                    "Message": "Check failed because compile test binoption failed."
                },
                "Test simple binary options program with OpenCL™.": {
                    "Value": "",
                    "RetVal": "FAIL",
                    "Command": "OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL binoption",
                    "Message": "Check failed because compile test binoption failed."
                }
                })
            return status

        mocked_run_binoption.side_effect = side_effect_run_binoption

        value = {}
        oneapi_gpu_checker.get_openmp_offload_info(value)
        self.assertEqual(expected, value)


@patch("checkers_py.linux.oneapi_gpu_checker.TMP_SIMPLE_SYCL_CODE_FILE", "simple-sycl-code")
@patch("checkers_py.linux.oneapi_gpu_checker.PATH_TO_SOURCE_OFFLOAD", "../oneapi_check_offloads")
class TestCompileSimpleSyclCode(unittest.TestCase):

    @patch("subprocess.Popen")
    def test__compile_simple_sycl_code_positive(self, mocked_open):
        expected = {
            "Compile simple SYCL code": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/simple-sycl-code.cpp "
                           "-o simple-sycl-code"
            }
        }
        expected_error_code = 0

        compile_mock = MagicMock()
        compile_mock.wait.return_value = 0

        mocked_open.return_value = compile_mock

        value = {}
        error_code = oneapi_gpu_checker._compile_simple_sycl_code(value)
        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)

    @patch("subprocess.Popen")
    def test__compile_simple_sycl_code_dpcpp_return_not_zero(self, mocked_open):
        expected = {
            "Compile simple SYCL code": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/simple-sycl-code.cpp "
                           "-o simple-sycl-code",
                "Message": "'dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/simple-sycl-code.cpp "
                           "-o simple-sycl-code'",
                "HowToFix": "Check compiled source file for syntax errors."
            }
        }

        expected_error_code = 1

        compile_mock = MagicMock()
        compile_mock.wait.return_value = (None, None)
        compile_mock.returncode = 1

        mocked_open.return_value = compile_mock

        value = {}
        error_code = oneapi_gpu_checker._compile_simple_sycl_code(value)
        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)

    @patch("subprocess.Popen", side_effect=Exception("test"))
    def test__compile_simple_sycl_code_raised_exception(self, mocked_open):
        expected = {
            "Compile simple SYCL code": {
                "Value": "",
                "RetVal": "ERROR",
                "Command": "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/simple-sycl-code.cpp "
                           "-o simple-sycl-code",
                "Message": "Sycl code compilation failed - DPC++ (dpcpp) not found.",
                "HowToFix": "Try to: " \
                            "1) install Intel® C++ Compiler based on " \
                            "https://www.intel.com/content/www/us/en/developer/articles/tool/oneapi-standalone-components.html " \
                            "2) set required variable by running: source /opt/intel/oneapi/setvars.sh"  # noqa E501
            }
        }

        expected_error_code = 1

        value = {}
        error_code = oneapi_gpu_checker._compile_simple_sycl_code(value)

        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)


@patch("checkers_py.linux.oneapi_gpu_checker.TMP_SIMPLE_SYCL_CODE_FILE", "simple-sycl-code")
class TestRunSimpleSyclCode(unittest.TestCase):

    @patch("subprocess.Popen")
    def test__run_simple_sycl_code_positive(self, mocked_open):

        expected = {
            "Test simple DPC++ program with Intel® oneAPI Level Zero.": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "SYCL_DEVICE_FILTER=level_zero:gpu simple-sycl-code"
            },
            "Test simple DPC++ program with OpenCL™.": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "SYCL_DEVICE_FILTER=opencl:gpu simple-sycl-code"
            }
        }
        expected_error_code = 0
        status = 0

        level_zero_mock = MagicMock()
        level_zero_mock.communicate.return_value = ("PASSED", None)
        level_zero_mock.returncode = 0

        opencl_mock = MagicMock()
        opencl_mock.communicate.return_value = ("PASSED", None)
        opencl_mock.returncode = 0

        mocked_open.side_effect = [level_zero_mock, opencl_mock]

        value = {}
        error_code = oneapi_gpu_checker._run_simple_sycl_code(status, value)

        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)

    def test__run_simple_sycl_code_status_is_not_zero(self):

        expected = {
            "Test simple DPC++ program with Intel® oneAPI Level Zero.": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "SYCL_DEVICE_FILTER=level_zero:gpu simple-sycl-code",
                "Message": "Check failed because compile simple SYCL code failed.",
                "HowToFix": "Check compiled source file for syntax errors."
            },
            "Test simple DPC++ program with OpenCL™.": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "SYCL_DEVICE_FILTER=opencl:gpu simple-sycl-code",
                "Message": "Check failed because compile simple SYCL code failed.",
                "HowToFix": "Check compiled source file for syntax errors."
            }
        }
        expected_error_code = 1
        status = 1

        value = {}
        error_code = oneapi_gpu_checker._run_simple_sycl_code(status, value)

        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)

    @patch("subprocess.Popen")
    def test__run_simple_sycl_code_level_zero_return_code_is_not_zero(self, mocked_open):
        expected = {
            "Test simple DPC++ program with Intel® oneAPI Level Zero.": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "SYCL_DEVICE_FILTER=level_zero:gpu simple-sycl-code",
                "Message": "An error occurred while running simple-sycl-code. ExitCode: 1",
                "HowToFix": "Look into output for more details: \n"
            },
            "Test simple DPC++ program with OpenCL™.": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "SYCL_DEVICE_FILTER=opencl:gpu simple-sycl-code"
            }
        }

        expected_error_code = 1
        status = 0

        level_zero_mock = MagicMock()
        level_zero_mock.communicate.return_value = ("", None)
        level_zero_mock.returncode = 1

        opencl_mock = MagicMock()
        opencl_mock.communicate.return_value = ("PASSED", None)
        opencl_mock.returncode = 0

        mocked_open.side_effect = [level_zero_mock, opencl_mock]

        value = {}
        error_code = oneapi_gpu_checker._run_simple_sycl_code(status, value)
        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)

    @patch("subprocess.Popen")
    def test__run_simple_sycl_code_opencl_return_code_is_not_zero(self, mocked_open):
        expected = {
            "Test simple DPC++ program with Intel® oneAPI Level Zero.": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "SYCL_DEVICE_FILTER=level_zero:gpu simple-sycl-code"
            },
            "Test simple DPC++ program with OpenCL™.": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "SYCL_DEVICE_FILTER=opencl:gpu simple-sycl-code",
                "Message": "An error occurred while running simple-sycl-code. ExitCode: 1",
                "HowToFix": "Look into output for more details: \n"
            }
        }

        expected_error_code = 1
        status = 0

        level_zero_mock = MagicMock()
        level_zero_mock.communicate.return_value = ("PASSED", None)
        level_zero_mock.returncode = 0

        opencl_mock = MagicMock()
        opencl_mock.communicate.return_value = ("", None)
        opencl_mock.returncode = 1

        mocked_open.side_effect = [level_zero_mock, opencl_mock]

        value = {}
        error_code = oneapi_gpu_checker._run_simple_sycl_code(status, value)

        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)

    @patch("subprocess.Popen")
    def test__run_simple_sycl_code_level_zero_and_opencl_return_code_is_not_zero(self, mocked_open):
        expected = {
            "Test simple DPC++ program with Intel® oneAPI Level Zero.": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "SYCL_DEVICE_FILTER=level_zero:gpu simple-sycl-code",
                "Message": "An error occurred while running simple-sycl-code. ExitCode: 1",
                "HowToFix": "Look into output for more details: \n"
            },
            "Test simple DPC++ program with OpenCL™.": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "SYCL_DEVICE_FILTER=opencl:gpu simple-sycl-code",
                "Message": "An error occurred while running simple-sycl-code. ExitCode: 1",
                "HowToFix": "Look into output for more details: \n"
            }
        }

        expected_error_code = 2
        status = 0

        level_zero_mock = MagicMock()
        level_zero_mock.communicate.return_value = ("", None)
        level_zero_mock.returncode = 1

        opencl_mock = MagicMock()
        opencl_mock.communicate.return_value = ("", None)
        opencl_mock.returncode = 1

        mocked_open.side_effect = [level_zero_mock, opencl_mock]

        value = {}
        error_code = oneapi_gpu_checker._run_simple_sycl_code(status, value)

        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)


@patch("checkers_py.linux.oneapi_gpu_checker.TMP_PARALLEL_FOR_1D_FILE", "parallel-for-1D")
@patch("checkers_py.linux.oneapi_gpu_checker.PATH_TO_SOURCE_OFFLOAD", "../oneapi_check_offloads")
class TestCompileParallelForProgram(unittest.TestCase):

    @patch("subprocess.Popen")
    def test__compile_parallel_for_program_positive(self, mocked_open):
        expected = {
            "Compile parallel for program": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/parallel-for-1D.cpp "
                           "-o parallel-for-1D"
            }
        }

        expected_error_code = 0

        compile_mock = MagicMock()
        compile_mock.wait.return_value = 0

        mocked_open.return_value = compile_mock

        value = {}
        error_code = oneapi_gpu_checker._compile_parallel_for_program(value)

        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)

    @patch("subprocess.Popen")
    def test__compile_parallel_for_program_dpcpp_return_not_zero(self, mocked_open):
        expected = {
            "Compile parallel for program": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/parallel-for-1D.cpp "
                           "-o parallel-for-1D",
                "Message": "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/parallel-for-1D.cpp "
                           "-o parallel-for-1D",
                "HowToFix": "Check compiled source file for syntax errors."
            }
        }
        expected_error_code = 1

        compile_mock = MagicMock()
        compile_mock.wait.return_value = (None, None)
        compile_mock.returncode = 1

        mocked_open.return_value = compile_mock

        value = {}
        error_code = oneapi_gpu_checker._compile_parallel_for_program(value)

        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)

    @patch("subprocess.Popen", side_effect=Exception("test"))
    def test__compile_parallel_for_program_raised_exception(self, mocked_open):
        expected = {
            "Compile parallel for program": {
                "Value": "",
                "RetVal": "ERROR",
                "Command": "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/parallel-for-1D.cpp "
                           "-o parallel-for-1D",
                "Message": "Parallel code compilation failed - DPC++ (dpcpp) not found.",
                "HowToFix": "Try to: " \
                            "1) install Intel® C++ Compiler based on " \
                            "https://www.intel.com/content/www/us/en/developer/articles/tool/oneapi-standalone-components.html " \
                            "2) set required variable by running: source /opt/intel/oneapi/setvars.sh"  # noqa E501
            }
        }
        expected_error_code = 1

        value = {}
        error_code = oneapi_gpu_checker._compile_parallel_for_program(value)

        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)


@patch("checkers_py.linux.oneapi_gpu_checker.TMP_PARALLEL_FOR_1D_FILE", "parallel-for-1D")
class TestRunParallelForProgram(unittest.TestCase):

    @patch("subprocess.Popen")
    def test__run_parallel_for_program_positive(self, mocked_open):

        expected = {
            "Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero.": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "SYCL_DEVICE_FILTER=level_zero:gpu parallel-for-1D"
            },
            "Test simple DPC++ parallel-for program with OpenCL™.": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "SYCL_DEVICE_FILTER=opencl:gpu parallel-for-1D"
            }
        }
        expected_error_code = 0
        status = 0

        level_zero_mock = MagicMock()
        level_zero_mock.communicate.return_value = ("PASSED", None)
        level_zero_mock.returncode = 0

        opencl_mock = MagicMock()
        opencl_mock.communicate.return_value = ("PASSED", None)
        opencl_mock.returncode = 0

        mocked_open.side_effect = [level_zero_mock, opencl_mock]

        value = {}
        error_code = oneapi_gpu_checker._run_parallel_for_program(status, value)

        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)

    def test__run_parallel_for_program_status_is_not_zero(self):

        expected = {
            "Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero.": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "SYCL_DEVICE_FILTER=level_zero:gpu parallel-for-1D",
                "Message": "Check failed because compile parallel for program failed.",
                "HowToFix": "Check compiled source file for syntax errors."
            },
            "Test simple DPC++ parallel-for program with OpenCL™.": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "SYCL_DEVICE_FILTER=opencl:gpu parallel-for-1D",
                "Message": "Check failed because compile parallel for program failed.",
                "HowToFix": "Check compiled source file for syntax errors."
            }
        }
        expected_error_code = 1
        status = 1

        value = {}
        error_code = oneapi_gpu_checker._run_parallel_for_program(status, value)

        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)

    @patch("subprocess.Popen")
    def test__run_parallel_for_program_level_zero_return_code_is_not_zero(self, mocked_open):
        expected = {
            "Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero.": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "SYCL_DEVICE_FILTER=level_zero:gpu parallel-for-1D",
                "Message": "An error occurred while running parallel-for-1D. "
                           "ExitCode: 1",
                "HowToFix":  "Look into output for more details: \n"
            },
            "Test simple DPC++ parallel-for program with OpenCL™.": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "SYCL_DEVICE_FILTER=opencl:gpu parallel-for-1D"
            }
        }

        expected_error_code = 1
        status = 0

        level_zero_mock = MagicMock()
        level_zero_mock.communicate.return_value = ("", None)
        level_zero_mock.returncode = 1

        opencl_mock = MagicMock()
        opencl_mock.communicate.return_value = ("PASSED", None)
        opencl_mock.returncode = 0

        mocked_open.side_effect = [level_zero_mock, opencl_mock]

        value = {}
        error_code = oneapi_gpu_checker._run_parallel_for_program(status, value)
        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)

    @patch("subprocess.Popen")
    def test__run_parallel_for_program_opencl_return_code_is_not_zero(self, mocked_open):
        expected = {
            "Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero.": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "SYCL_DEVICE_FILTER=level_zero:gpu parallel-for-1D"
            },
            "Test simple DPC++ parallel-for program with OpenCL™.": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "SYCL_DEVICE_FILTER=opencl:gpu parallel-for-1D",
                "Message": "An error occurred while running parallel-for-1D. "
                           "ExitCode: 1",
                "HowToFix":  "Look into output for more details: \n"
            }
        }

        expected_error_code = 1
        status = 0

        level_zero_mock = MagicMock()
        level_zero_mock.communicate.return_value = ("PASSED", None)
        level_zero_mock.returncode = 0

        opencl_mock = MagicMock()
        opencl_mock.communicate.return_value = ("", None)
        opencl_mock.returncode = 1

        mocked_open.side_effect = [level_zero_mock, opencl_mock]

        value = {}
        error_code = oneapi_gpu_checker._run_parallel_for_program(status, value)

        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)

    @patch("subprocess.Popen")
    def test__run_simple_sycl_code_level_zero_and_opencl_return_code_is_not_zero(self, mocked_open):
        expected = {
            "Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero.": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "SYCL_DEVICE_FILTER=level_zero:gpu parallel-for-1D",
                "Message": "An error occurred while running parallel-for-1D. "
                           "ExitCode: 1",
                "HowToFix":  "Look into output for more details: \n"
            },
            "Test simple DPC++ parallel-for program with OpenCL™.": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "SYCL_DEVICE_FILTER=opencl:gpu parallel-for-1D",
                "Message": "An error occurred while running parallel-for-1D. "
                           "ExitCode: 1",
                "HowToFix":  "Look into output for more details: \n"
            }
        }

        expected_error_code = 2
        status = 0

        level_zero_mock = MagicMock()
        level_zero_mock.communicate.return_value = ("", None)
        level_zero_mock.returncode = 1

        opencl_mock = MagicMock()
        opencl_mock.communicate.return_value = ("", None)
        opencl_mock.returncode = 1

        mocked_open.side_effect = [level_zero_mock, opencl_mock]

        value = {}
        error_code = oneapi_gpu_checker._run_parallel_for_program(status, value)

        self.assertEqual(expected, value)
        self.assertEqual(expected_error_code, error_code)


class TestGetDpcppOffloadInfo(unittest.TestCase):

    @patch("checkers_py.linux.oneapi_gpu_checker._run_parallel_for_program")
    @patch("checkers_py.linux.oneapi_gpu_checker._compile_parallel_for_program")
    @patch("checkers_py.linux.oneapi_gpu_checker._run_simple_sycl_code")
    @patch("checkers_py.linux.oneapi_gpu_checker._compile_simple_sycl_code")
    def test_get_dpcpp_offload_info_positive(self, mocked_compile_sycl, mocked_run_sycl,
                                             mocked_compile_parallel, mocked_run_parallel):

        expected = {
            "DPC++ GPU pipeline tests": {
                "Value": {
                    "Compile simple SYCL code": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/simple-sycl-code.cpp "
                                   "-o simple-sycl-code"
                    },
                    "Test simple DPC++ program with Intel® oneAPI Level Zero.": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "SYCL_DEVICE_FILTER=level_zero:gpu simple-sycl-code"
                    },
                    "Test simple DPC++ program with OpenCL™.": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "SYCL_DEVICE_FILTER=opencl:gpu simple-sycl-code"
                    },
                    "Compile parallel for program": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/parallel-for-1D.cpp "
                                   "-o parallel-for-1D"
                    },
                    "Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero.": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "SYCL_DEVICE_FILTER=level_zero:gpu parallel-for-1D"
                    },
                    "Test simple DPC++ parallel-for program with OpenCL™.": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "SYCL_DEVICE_FILTER=opencl:gpu parallel-for-1D"
                    }
                },
                "RetVal": "PASS"
            }
        }

        def side_effect_compile_sycl(node):
            node.update({
                "Compile simple SYCL code": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/simple-sycl-code.cpp "
                               "-o simple-sycl-code"
                }
            })
            return 0

        mocked_compile_sycl.side_effect = side_effect_compile_sycl

        def side_effect_run_sycl(status, node):
            node.update({
                "Test simple DPC++ program with Intel® oneAPI Level Zero.": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "SYCL_DEVICE_FILTER=level_zero:gpu simple-sycl-code"
                },
                "Test simple DPC++ program with OpenCL™.": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "SYCL_DEVICE_FILTER=opencl:gpu simple-sycl-code"
                }
            })
            return status

        mocked_run_sycl.side_effect = side_effect_run_sycl

        def side_effect_compile_parallel(node):
            node.update({
                "Compile parallel for program": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/parallel-for-1D.cpp "
                               "-o parallel-for-1D"
                }
            })
            return 0

        mocked_compile_parallel.side_effect = side_effect_compile_parallel

        def side_effect_run_parallel(status, node):
            node.update({
                "Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero.": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "SYCL_DEVICE_FILTER=level_zero:gpu parallel-for-1D"
                },
                "Test simple DPC++ parallel-for program with OpenCL™.": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "SYCL_DEVICE_FILTER=opencl:gpu parallel-for-1D"
                }
            })
            return status

        mocked_run_parallel.side_effect = side_effect_run_parallel

        value = {}
        oneapi_gpu_checker.get_dpcpp_offload_info(value)
        self.assertEqual(expected, value)

    @patch("checkers_py.linux.oneapi_gpu_checker._run_parallel_for_program")
    @patch("checkers_py.linux.oneapi_gpu_checker._compile_parallel_for_program")
    @patch("checkers_py.linux.oneapi_gpu_checker._run_simple_sycl_code")
    @patch("checkers_py.linux.oneapi_gpu_checker._compile_simple_sycl_code")
    def test_get_dpcpp_offload_info_sycl_failed(self, mocked_compile_sycl, mocked_run_sycl,
                                                mocked_compile_parallel, mocked_run_parallel):

        expected = {
            "DPC++ GPU pipeline tests": {
                "Value": {
                    "Compile simple SYCL code": {
                        "Value": "",
                        "RetVal": "FAIL",
                        "Command": "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/simple-sycl-code.cpp "
                                   "-o simple-sycl-code",
                        "Message": "'dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/simple-sycl-code.cpp "
                                   "-o simple-sycl-code'"
                    },
                    "Test simple DPC++ program with Intel® oneAPI Level Zero.": {
                        "Value": "",
                        "RetVal": "FAIL",
                        "Command": "SYCL_DEVICE_FILTER=level_zero:gpu simple-sycl-code",
                        "Message": "Check failed because compile simple SYCL code failed."
                    },
                    "Test simple DPC++ program with OpenCL™.": {
                        "Value": "",
                        "RetVal": "FAIL",
                        "Command": "SYCL_DEVICE_FILTER=opencl:gpu simple-sycl-code",
                        "Message": "Check failed because compile simple SYCL code failed."
                    },
                    "Compile parallel for program": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/parallel-for-1D.cpp "
                                   "-o parallel-for-1D"
                    },
                    "Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero.": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "SYCL_DEVICE_FILTER=level_zero:gpu parallel-for-1D"
                    },
                    "Test simple DPC++ parallel-for program with OpenCL™.": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "SYCL_DEVICE_FILTER=opencl:gpu parallel-for-1D"
                    }
                },
                "RetVal": "FAIL",
                "Message": "Some checks below failed.",
                "HowToFix": "Review output of checks for more details."

            }
        }

        def side_effect_compile_sycl(node):
            node.update({
                "Compile simple SYCL code": {
                    "Value": "",
                    "RetVal": "FAIL",
                    "Command": "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/simple-sycl-code.cpp "
                               "-o simple-sycl-code",
                    "Message": "'dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/simple-sycl-code.cpp "
                               "-o simple-sycl-code'"
                }
            })
            return 1

        mocked_compile_sycl.side_effect = side_effect_compile_sycl

        def side_effect_run_sycl(status, node):
            node.update({
                "Test simple DPC++ program with Intel® oneAPI Level Zero.": {
                    "Value": "",
                    "RetVal": "FAIL",
                    "Command": "SYCL_DEVICE_FILTER=level_zero:gpu simple-sycl-code",
                    "Message": "Check failed because compile simple SYCL code failed."
                },
                "Test simple DPC++ program with OpenCL™.": {
                    "Value": "",
                    "RetVal": "FAIL",
                    "Command": "SYCL_DEVICE_FILTER=opencl:gpu simple-sycl-code",
                    "Message": "Check failed because compile simple SYCL code failed."
                }
            })
            return status

        mocked_run_sycl.side_effect = side_effect_run_sycl

        def side_effect_compile_parallel(node):
            node.update({
                "Compile parallel for program": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/parallel-for-1D.cpp "
                               "-o parallel-for-1D"
                }
            })
            return 0

        mocked_compile_parallel.side_effect = side_effect_compile_parallel

        def side_effect_run_parallel(status, node):
            node.update({
                "Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero.": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "SYCL_DEVICE_FILTER=level_zero:gpu parallel-for-1D"
                },
                "Test simple DPC++ parallel-for program with OpenCL™.": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "SYCL_DEVICE_FILTER=opencl:gpu parallel-for-1D"
                }
            })
            return status

        mocked_run_parallel.side_effect = side_effect_run_parallel

        value = {}
        oneapi_gpu_checker.get_dpcpp_offload_info(value)
        self.assertEqual(expected, value)

    @patch("checkers_py.linux.oneapi_gpu_checker._run_parallel_for_program")
    @patch("checkers_py.linux.oneapi_gpu_checker._compile_parallel_for_program")
    @patch("checkers_py.linux.oneapi_gpu_checker._run_simple_sycl_code")
    @patch("checkers_py.linux.oneapi_gpu_checker._compile_simple_sycl_code")
    def test_get_dpcpp_offload_info_sycl_raised_exception(self, mocked_compile_sycl, mocked_run_sycl,
                                                          mocked_compile_parallel, mocked_run_parallel):

        expected = {
            "DPC++ GPU pipeline tests": {
                "Value": {
                    "Compile simple SYCL code": {
                        "Value": "",
                        "RetVal": "ERROR",
                        "Command": "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/simple-sycl-code.cpp "
                                   "-o simple-sycl-code",
                        "Message": "DPC++ (dpcpp) not found."
                    },
                    "Test simple DPC++ program with Intel® oneAPI Level Zero.": {
                        "Value": "",
                        "RetVal": "FAIL",
                        "Command": "SYCL_DEVICE_FILTER=level_zero:gpu simple-sycl-code",
                        "Message": "Check failed because compile simple SYCL code failed."
                    },
                    "Test simple DPC++ program with OpenCL™.": {
                        "Value": "",
                        "RetVal": "FAIL",
                        "Command": "SYCL_DEVICE_FILTER=opencl:gpu simple-sycl-code",
                        "Message": "Check failed because compile simple SYCL code failed."
                    },
                    "Compile parallel for program": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/parallel-for-1D.cpp "
                                   "-o parallel-for-1D"
                    },
                    "Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero.": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "SYCL_DEVICE_FILTER=level_zero:gpu parallel-for-1D"
                    },
                    "Test simple DPC++ parallel-for program with OpenCL™.": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "SYCL_DEVICE_FILTER=opencl:gpu parallel-for-1D"
                    }
                },
                "RetVal": "FAIL",
                "Message": "Some checks below failed.",
                "HowToFix": "Review output of checks for more details."

            }
        }

        def side_effect_compile_sycl(node):
            node.update({
                "Compile simple SYCL code": {
                    "Value": "",
                    "RetVal": "ERROR",
                    "Command": "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/simple-sycl-code.cpp "
                               "-o simple-sycl-code",
                    "Message": "DPC++ (dpcpp) not found."
                }
            })
            return 1

        mocked_compile_sycl.side_effect = side_effect_compile_sycl

        def side_effect_run_sycl(status, node):
            node.update({
                "Test simple DPC++ program with Intel® oneAPI Level Zero.": {
                    "Value": "",
                    "RetVal": "FAIL",
                    "Command": "SYCL_DEVICE_FILTER=level_zero:gpu simple-sycl-code",
                    "Message": "Check failed because compile simple SYCL code failed."
                },
                "Test simple DPC++ program with OpenCL™.": {
                    "Value": "",
                    "RetVal": "FAIL",
                    "Command": "SYCL_DEVICE_FILTER=opencl:gpu simple-sycl-code",
                    "Message": "Check failed because compile simple SYCL code failed."
                }
            })
            return status

        mocked_run_sycl.side_effect = side_effect_run_sycl

        def side_effect_compile_parallel(node):
            node.update({
                "Compile parallel for program": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/parallel-for-1D.cpp "
                               "-o parallel-for-1D"
                }
            })
            return 0

        mocked_compile_parallel.side_effect = side_effect_compile_parallel

        def side_effect_run_parallel(status, node):
            node.update({
                "Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero.": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "SYCL_DEVICE_FILTER=level_zero:gpu parallel-for-1D"
                },
                "Test simple DPC++ parallel-for program with OpenCL™.": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "SYCL_DEVICE_FILTER=opencl:gpu parallel-for-1D"
                }
            })
            return status

        mocked_run_parallel.side_effect = side_effect_run_parallel

        value = {}
        oneapi_gpu_checker.get_dpcpp_offload_info(value)
        self.assertEqual(expected, value)

    @patch("checkers_py.linux.oneapi_gpu_checker._run_parallel_for_program")
    @patch("checkers_py.linux.oneapi_gpu_checker._compile_parallel_for_program")
    @patch("checkers_py.linux.oneapi_gpu_checker._run_simple_sycl_code")
    @patch("checkers_py.linux.oneapi_gpu_checker._compile_simple_sycl_code")
    def test_get_dpcpp_offload_info_parallel_failed(self, mocked_compile_sycl, mocked_run_sycl,
                                                    mocked_compile_parallel, mocked_run_parallel):

        expected = {
            "DPC++ GPU pipeline tests": {
                "Value": {
                    "Compile simple SYCL code": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/simple-sycl-code.cpp "
                                   "-o simple-sycl-code"
                    },
                    "Test simple DPC++ program with Intel® oneAPI Level Zero.": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "SYCL_DEVICE_FILTER=level_zero:gpu simple-sycl-code"
                    },
                    "Test simple DPC++ program with OpenCL™.": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "SYCL_DEVICE_FILTER=opencl:gpu simple-sycl-code"
                    },
                    "Compile parallel for program": {
                        "Value": "",
                        "RetVal": "FAIL",
                        "Command": "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/parallel-for-1D.cpp "
                                   "-o parallel-for-1D",
                        "Message": "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/parallel-for-1D.cpp "
                                   "-o parallel-for-1D"
                    },
                    "Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero.": {
                        "Value": "",
                        "RetVal": "FAIL",
                        "Command": "SYCL_DEVICE_FILTER=level_zero:gpu parallel-for-1D",
                        "Message": "Check failed because compile parallel for program failed."
                    },
                    "Test simple DPC++ parallel-for program with OpenCL™.": {
                        "Value": "",
                        "RetVal": "FAIL",
                        "Command": "SYCL_DEVICE_FILTER=opencl:gpu parallel-for-1D",
                        "Message": "Check failed because compile parallel for program failed."
                    }
                },
                "RetVal": "FAIL",
                "Message": "Some checks below failed.",
                "HowToFix": "Review output of checks for more details."
            }
        }

        def side_effect_compile_sycl(node):
            node.update({
                "Compile simple SYCL code": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/simple-sycl-code.cpp "
                               "-o simple-sycl-code"
                }
            })
            return 0

        mocked_compile_sycl.side_effect = side_effect_compile_sycl

        def side_effect_run_sycl(status, node):
            node.update({
                "Test simple DPC++ program with Intel® oneAPI Level Zero.": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "SYCL_DEVICE_FILTER=level_zero:gpu simple-sycl-code"
                },
                "Test simple DPC++ program with OpenCL™.": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "SYCL_DEVICE_FILTER=opencl:gpu simple-sycl-code"
                }
            })
            return status

        mocked_run_sycl.side_effect = side_effect_run_sycl

        def side_effect_compile_parallel(node):
            node.update({
                "Compile parallel for program": {
                    "Value": "",
                    "RetVal": "FAIL",
                    "Command": "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/parallel-for-1D.cpp "
                               "-o parallel-for-1D",
                    "Message":  "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/parallel-for-1D.cpp "
                                "-o parallel-for-1D"
                }
            })
            return 1

        mocked_compile_parallel.side_effect = side_effect_compile_parallel

        def side_effect_run_parallel(status, node):
            node.update({
                "Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero.": {
                    "Value": "",
                    "RetVal": "FAIL",
                    "Command": "SYCL_DEVICE_FILTER=level_zero:gpu parallel-for-1D",
                    "Message": "Check failed because compile parallel for program failed."
                },
                "Test simple DPC++ parallel-for program with OpenCL™.": {
                    "Value": "",
                    "RetVal": "FAIL",
                    "Command": "SYCL_DEVICE_FILTER=opencl:gpu parallel-for-1D",
                    "Message": "Check failed because compile parallel for program failed."
                }
            })
            return status

        mocked_run_parallel.side_effect = side_effect_run_parallel

        value = {}
        oneapi_gpu_checker.get_dpcpp_offload_info(value)
        self.assertEqual(expected, value)

    @patch("checkers_py.linux.oneapi_gpu_checker._run_parallel_for_program")
    @patch("checkers_py.linux.oneapi_gpu_checker._compile_parallel_for_program")
    @patch("checkers_py.linux.oneapi_gpu_checker._run_simple_sycl_code")
    @patch("checkers_py.linux.oneapi_gpu_checker._compile_simple_sycl_code")
    def test_get_dpcpp_offload_info_parallel_raised_exception(self, mocked_compile_sycl, mocked_run_sycl,
                                                              mocked_compile_parallel, mocked_run_parallel):

        expected = {
            "DPC++ GPU pipeline tests": {
                "Value": {
                    "Compile simple SYCL code": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/simple-sycl-code.cpp "
                                   "-o simple-sycl-code"
                    },
                    "Test simple DPC++ program with Intel® oneAPI Level Zero.": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "SYCL_DEVICE_FILTER=level_zero:gpu simple-sycl-code"
                    },
                    "Test simple DPC++ program with OpenCL™.": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "SYCL_DEVICE_FILTER=opencl:gpu simple-sycl-code"
                    },
                    "Compile parallel for program": {
                        "Value": "",
                        "RetVal": "ERROR",
                        "Command": "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/parallel-for-1D.cpp "
                                   "-o parallel-for-1D",
                        "Message": "DPC++ (dpcpp) not found."
                    },
                    "Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero.": {
                        "Value": "",
                        "RetVal": "FAIL",
                        "Command": "SYCL_DEVICE_FILTER=level_zero:gpu parallel-for-1D",
                        "Message": "Check failed because compile parallel for program failed."
                    },
                    "Test simple DPC++ parallel-for program with OpenCL™.": {
                        "Value": "",
                        "RetVal": "FAIL",
                        "Command": "SYCL_DEVICE_FILTER=opencl:gpu parallel-for-1D",
                        "Message": "Check failed because compile parallel for program failed."
                    }
                },
                "RetVal": "FAIL",
                "Message": "Some checks below failed.",
                "HowToFix": "Review output of checks for more details."
            }
        }

        def side_effect_compile_sycl(node):
            node.update({
                "Compile simple SYCL code": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/simple-sycl-code.cpp "
                               "-o simple-sycl-code"
                }
            })
            return 0

        mocked_compile_sycl.side_effect = side_effect_compile_sycl

        def side_effect_run_sycl(status, node):
            node.update({
                "Test simple DPC++ program with Intel® oneAPI Level Zero.": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "SYCL_DEVICE_FILTER=level_zero:gpu simple-sycl-code"
                },
                "Test simple DPC++ program with OpenCL™.": {
                    "Value": "",
                    "RetVal": "PASS",
                    "Command": "SYCL_DEVICE_FILTER=opencl:gpu simple-sycl-code"
                }
            })
            return status

        mocked_run_sycl.side_effect = side_effect_run_sycl

        def side_effect_compile_parallel(node):
            node.update({
                "Compile parallel for program": {
                    "Value": "",
                    "RetVal": "ERROR",
                    "Command": "dpcpp -std=c++17 -fsycl ../oneapi_check_offloads/parallel-for-1D.cpp "
                               "-o parallel-for-1D",
                    "Message":  "DPC++ (dpcpp) not found."
                }
            })
            return 1

        mocked_compile_parallel.side_effect = side_effect_compile_parallel

        def side_effect_run_parallel(status, node):
            node.update({
                "Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero.": {
                    "Value": "",
                    "RetVal": "FAIL",
                    "Command": "SYCL_DEVICE_FILTER=level_zero:gpu parallel-for-1D",
                    "Message": "Check failed because compile parallel for program failed."
                },
                "Test simple DPC++ parallel-for program with OpenCL™.": {
                    "Value": "",
                    "RetVal": "FAIL",
                    "Command": "SYCL_DEVICE_FILTER=opencl:gpu parallel-for-1D",
                    "Message": "Check failed because compile parallel for program failed."
                }
            })
            return status

        mocked_run_parallel.side_effect = side_effect_run_parallel

        value = {}
        oneapi_gpu_checker.get_dpcpp_offload_info(value)
        self.assertEqual(expected, value)


if __name__ == '__main__':
    unittest.TestCase.maxDiff = None
    unittest.main()
