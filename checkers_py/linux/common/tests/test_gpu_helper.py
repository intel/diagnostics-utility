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
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))

import unittest  # noqa: E402
from unittest.mock import MagicMock, call, patch  # noqa: E402

import gpu_helper  # noqa: E402


class TestGpuHelper(unittest.TestCase):

    def test_intel_gpus_not_found_handler_positive(self):
        expected = {
            "Warning message": {
                "Value": "",
                "RetVal": "WARNING",
                "Message": "The checker might show irrelevant information for your system because "
                           "the intel_gpu_detector_check failed."
            }
        }

        value = {}
        gpu_helper.intel_gpus_not_found_handler(value)

        self.assertEqual(expected, value)

    def test_are_intel_gpus_found_positive(self):
        expected = True

        input = {
            "intel_gpu_detector_check": {
                "Value": {
                    "GPU information": {
                        "Value": {
                            "Intel GPU(s) is present on the bus": {
                                "RetVal": "PASS"
                            }
                        }
                    }
                }
            }
        }

        value = gpu_helper.are_intel_gpus_found(input)

        self.assertEqual(expected, value)

    def test_are_intel_gpus_found_negative(self):
        expected = False

        input = {
            "intel_gpu_detector_check": {
                "Value": {
                    "GPU information": {
                        "Value": {
                            "Intel GPU(s) is present on the bus": {
                                "RetVal": "FAIL"
                            }
                        }
                    }
                }
            }
        }

        value = gpu_helper.are_intel_gpus_found(input)

        self.assertEqual(expected, value)

    @patch("os.listdir", return_value=["by-path", "card0", "card1", "renderD128", "renderD129"])
    @patch("gpu_helper.Path")
    def test_get_render_devices_positive(self, mocked_path, mocked_os):
        expected = [call("renderD128"), call("renderD129")]
        mocked_path.return_value = MagicMock()
        mocked_path.return_value.exists.return_value = True

        gpu_helper.get_render_devices()

        mocked_path.return_value.__truediv__.assert_has_calls(expected)

    @patch("gpu_helper.Path")
    def test_get_render_devices_path_does_not_exist(self, mocked_path):
        expected = []
        mocked_path.return_value = MagicMock()
        mocked_path.return_value.exists.return_value = False

        value = gpu_helper.get_render_devices()

        self.assertEqual(expected, value)

    @patch("os.listdir", return_value=["by-path", "card0", "card1", "renderD128", "renderD129"])
    @patch("gpu_helper.Path")
    def test_get_card_devices_positive(self, mocked_path, mocked_os):
        expected = [call("card0"), call("card1")]
        mocked_path.return_value = MagicMock()
        mocked_path.return_value.exists.return_value = True

        gpu_helper.get_card_devices()

        mocked_path.return_value.__truediv__.assert_has_calls(expected)

    @patch("gpu_helper.Path")
    def test_get_card_devices_path_does_not_exist(self, mocked_path):
        expected = []
        mocked_path.return_value = MagicMock()
        mocked_path.return_value.exists.return_value = False

        value = gpu_helper.get_card_devices()

        self.assertEqual(expected, value)


if __name__ == '__main__':
    unittest.main()
