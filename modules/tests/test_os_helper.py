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
from unittest.mock import patch, mock_open  # noqa: E402

from modules.os_helper import _get_os, is_os_supported, check_that_os_is_supported, \
                            _get_linux_distribution  # noqa: E402


SUPPORTED_OS_RELEASE_CONTENT = """NAME="Ubuntu"\nVERSION_ID="20.04"\n"""


class TestGetLinuxDistribution(unittest.TestCase):

    @patch("builtins.open", mock_open(read_data=SUPPORTED_OS_RELEASE_CONTENT))
    def test__get_linux_distribution_positive(self):
        expected = ("Ubuntu", "20.04")

        value = _get_linux_distribution()

        self.assertEqual(expected, value)

    @patch("builtins.open", mock_open(read_data="""TEST="Test"\n"""))
    def test__get_linux_distribution_negative(self):
        self.assertRaises(Exception, _get_linux_distribution)


class TestGetOs(unittest.TestCase):

    @patch("platform.system", return_value="Windows")
    @patch("modules.os_helper._get_windows_version", return_value="10")
    def test__get_os_windows_os_positive(self, mocked__get_windows_version, mocked_system):
        expected = ("Windows", "10")

        value = _get_os()

        self.assertEqual(expected, value)

    @patch("platform.system", return_value="Linux")
    @patch("builtins.open", mock_open(read_data=SUPPORTED_OS_RELEASE_CONTENT))
    def test__get_os_linux_os_positive(self, mocked_system):
        expected = ("Ubuntu", "20.04")

        value = _get_os()

        self.assertEqual(expected, value)

    @patch("platform.system", return_value="Unsupported")
    def test__get_os_not_supported_os_negative(self, mocked_system):
        self.assertRaises(Exception, _get_os)


class TestIsOsSupported(unittest.TestCase):

    @patch("modules.os_helper._get_os", return_value=("Ubuntu", "20.04"))
    def test_os_is_supported(self, mock__get_os):
        expected = True

        value = is_os_supported()

        mock__get_os.assert_called_once()
        self.assertEqual(expected, value)

    @patch("modules.os_helper._get_os", return_value=("NOT_SUPPORTED", "NOT_SUPPORTED"))
    def test_os_is_not_supported_fully(self, mock__get_os):
        expected = False

        value = is_os_supported()

        mock__get_os.assert_called_once()
        self.assertEqual(expected, value)

    @patch("modules.os_helper._get_os", return_value=("Os", "1.1"))
    def test_os_is_not_supported_version(self, mock__get_os):
        expected = False

        value = is_os_supported()

        mock__get_os.assert_called_once()
        self.assertEqual(expected, value)

    @patch("modules.os_helper._get_os", side_effect=Exception())
    def test_get_os_raise_exception(self, mock__get_os):
        expected = False

        value = is_os_supported()

        mock__get_os.assert_called_once()
        self.assertEqual(expected, value)

    @patch("modules.os_helper.is_os_supported", return_value=True)
    def test_check_that_os_is_supported_positive(self, mock_is_os_supported):
        check_that_os_is_supported()

        mock_is_os_supported.assert_called_once()

    @patch("modules.os_helper.is_os_supported", return_value=False)
    @patch("builtins.exit")
    @patch("builtins.print")
    def test_check_that_os_is_supported_negative(self, mock_print, mock_exit, mock_is_os_supported):
        expected_output = "Your operating system is not supported by the Diagnostics Utility\n" \
                          "for Intel® oneAPI Toolkits. You can force the program to run using the " \
                          "--force flag."
        expected_exit_code = 1

        check_that_os_is_supported()

        mock_print.assert_called_with(expected_output)
        mock_exit.assert_called_once_with(expected_exit_code)
        mock_is_os_supported.assert_called_once()


if __name__ == '__main__':
    unittest.main()
