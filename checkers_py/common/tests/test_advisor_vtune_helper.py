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
from unittest.mock import patch, MagicMock  # noqa: E402

import advisor_vtune_helper  # noqa: E402


class TestAdvisorVtuneHelper(unittest.TestCase):

    def test_get_os_returns_str(self):
        expected = str

        value = advisor_vtune_helper.get_OS()

        self.assertIsInstance(value, expected)

    @patch("subprocess.Popen")
    def test_check_perf_stream_paranoid_positive(self, mocked_open):
        expected = {"Perf stream paranoid": {
            "Command": "sysctl -n dev.i915.perf_stream_paranoid",
            "RetVal": "PASS",
            "Value": "0"
        }}

        process = MagicMock()
        process.communicate.return_value = ("0", None)
        process.returncode = 0

        mocked_open.return_value = process

        value = {}
        advisor_vtune_helper.check_perf_stream_paranoid(value)

        self.assertEqual(value, expected)

    @patch("subprocess.Popen")
    def test_check_perf_stream_paranoid_perf_stream_is_1(self, mocked_open):
        expected = {"Perf stream paranoid": {
            "Command": "sysctl -n dev.i915.perf_stream_paranoid",
            "Message": "Set the value of the dev.i915.perf_stream_paranoid sysctl option to 0.",
            "RetVal": "FAIL",
            "Value": "1"
        }}

        process = MagicMock()
        process.communicate.return_value = ("1", None)
        process.returncode = 0

        mocked_open.return_value = process

        value = {}
        advisor_vtune_helper.check_perf_stream_paranoid(value)

        self.assertEqual(value, expected)

    @patch("subprocess.Popen", side_effect=Exception("test message"))
    def test_check_perf_stream_paranoid_popen_raise_exception(self, mocked_open):
        expected = {"Perf stream paranoid": {
            "Command": "sysctl -n dev.i915.perf_stream_paranoid",
            "Message": "test message",
            "RetVal": "ERROR",
            "Value": "Undefined"
        }}

        value = {}
        advisor_vtune_helper.check_perf_stream_paranoid(value)

        self.assertEqual(value, expected)

    @patch("subprocess.Popen")
    def test_check_perf_stream_paranoid_return_code_1(self, mocked_open):
        expected = {"Perf stream paranoid": {
            "Command": "sysctl -n dev.i915.perf_stream_paranoid",
            "Message": "Cannot get information about operating sysctl option",
            "RetVal": "ERROR",
            "Value": "Undefined"
        }}

        process = MagicMock()
        process.communicate.return_value = ("0", None)
        process.returncode = 1

        mocked_open.return_value = process

        value = {}
        advisor_vtune_helper.check_perf_stream_paranoid(value)

        self.assertEqual(value, expected)


if __name__ == '__main__':
    unittest.main()
