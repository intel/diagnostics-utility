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

import unittest  # noqa: E402

from io import StringIO  # noqa: E402
from pathlib import Path  # noqa: E402
from unittest.mock import patch, mock_open  # noqa: E402

from modules.printing.printer import print_ex  # noqa: E402
from modules.printing.printer_helper import Colors  # noqa: E402


class TestPrintEx(unittest.TestCase):

    def test_print_ex_console_only_default_positive(self):
        with patch('sys.stdout', new=StringIO()) as stdout:
            print_ex("Message", None)
            self.assertEqual(stdout.getvalue(), "Message\n")

    def test_print_ex_console_only_colored_positive(self):
        with patch('sys.stdout', new=StringIO()) as stdout:
            print_ex("Message", None, color=Colors.Green)
            self.assertEqual(stdout.getvalue(), f"{Colors.Green}Message{Colors.Default}\n")

    def test_print_ex_console_only_changed_end_positive(self):
        with patch('sys.stdout', new=StringIO()) as stdout:
            print_ex("Message", None, end="")
            self.assertEqual(stdout.getvalue(), "Message")

    def test_print_ex_console_only_colored_and_changed_end_positive(self):
        with patch('sys.stdout', new=StringIO()) as stdout:
            print_ex("Message", None, color=Colors.Green, end="")
            self.assertEqual(stdout.getvalue(), f"{Colors.Green}Message{Colors.Default}")

    @patch("sys.stdout")
    def test_print_ex_default_positive(self, mocked_stdout):
        with patch("builtins.open", mock_open()) as output_file:
            print_ex("Message", Path("path_to_the_output_file"))
            output_file().write.assert_called_once_with("Message\n")

    @patch("sys.stdout")
    def test_print_ex_colored_positive(self, mocked_stdout):
        with patch("builtins.open", mock_open()) as output_file:
            print_ex("Message", Path("path_to_the_output_file"), color=Colors.Red)
            output_file().write.assert_called_once_with("Message\n")

    @patch("sys.stdout")
    def test_print_ex_changed_end_positive(self, mocked_stdout):
        with patch("builtins.open", mock_open()) as output_file:
            print_ex("Message", Path("path_to_the_output_file"), end="")
            output_file().write.assert_called_once_with("Message")

    @patch("sys.stdout")
    def test_print_ex_colored_and_changed_end_positive(self, mocked_stdout):
        with patch("builtins.open", mock_open()) as output_file:
            print_ex("Message", Path("path_to_the_output_file"), color=Colors.Red, end="")
            output_file().write.assert_called_once_with("Message")


if __name__ == '__main__':
    unittest.main()
