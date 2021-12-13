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

from checkers_py import oneapi_gpu_checker  # noqa: E402
from modules.check import CheckSummary, CheckMetadataPy  # noqa: E402


class TestOneapiGpuCheckerApiTest(unittest.TestCase):

    @patch("checkers_py.oneapi_gpu_checker.get_dpcpp_offload_info")
    @patch("checkers_py.oneapi_gpu_checker.get_openmp_offload_info")
    @patch("checkers_py.oneapi_gpu_checker.get_gpu_errors_info")
    @patch("checkers_py.oneapi_gpu_checker.get_dmesg_i915_init_errors_info")
    @patch("checkers_py.oneapi_gpu_checker.get_permissions_to_render_info")
    @patch("checkers_py.oneapi_gpu_checker.get_permissions_to_card_info")
    @patch("checkers_py.oneapi_gpu_checker.get_intel_device_is_available_info")
    @patch("checkers_py.oneapi_gpu_checker.get_i915_driver_loaded_info")
    @patch("checkers_py.oneapi_gpu_checker.intel_gpus_not_found_handler")
    @patch("checkers_py.oneapi_gpu_checker.are_intel_gpus_found", return_value=False)
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

    @patch("checkers_py.oneapi_gpu_checker.get_dpcpp_offload_info")
    @patch("checkers_py.oneapi_gpu_checker.get_openmp_offload_info")
    @patch("checkers_py.oneapi_gpu_checker.get_gpu_errors_info")
    @patch("checkers_py.oneapi_gpu_checker.get_dmesg_i915_init_errors_info")
    @patch("checkers_py.oneapi_gpu_checker.get_permissions_to_render_info")
    @patch("checkers_py.oneapi_gpu_checker.get_permissions_to_card_info")
    @patch("checkers_py.oneapi_gpu_checker.get_intel_device_is_available_info")
    @patch("checkers_py.oneapi_gpu_checker.get_i915_driver_loaded_info")
    @patch("checkers_py.oneapi_gpu_checker.are_intel_gpus_found", return_value=True)
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


if __name__ == '__main__':
    unittest.main()
