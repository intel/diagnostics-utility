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
from unittest.mock import patch  # noqa: E402

from modules.printing.epilog_printer import print_epilog  # noqa: E402


class TestEpilogPrinter(unittest.TestCase):

    @patch("platform.node", return_value="hostname")
    def test_print_epilog_no_txt_positive(self, mocked_node):
        expected_stdout = "\n" + \
                          "JSON output file: output.json\n" + \
                          "\n" + \
                          "The report was generated for the machine: hostname\n" + \
                          "by the Diagnostics Utility for Intel® oneAPI Toolkits 1.0.0\n"
        with patch('sys.stdout', new=StringIO()) as stdout:
            print_epilog(None, Path("output.json"), "1.0.0")
            self.assertEqual(stdout.getvalue(), expected_stdout)

    @patch("platform.node", return_value="hostname")
    def test_print_epilog_no_json_positive(self, mocked_node):
        expected_stdout = "\n" + \
                          "Console output file: output.txt\n" + \
                          "\n" + \
                          "The report was generated for the machine: hostname\n" + \
                          "by the Diagnostics Utility for Intel® oneAPI Toolkits 1.0.0\n"
        with patch('sys.stdout', new=StringIO()) as stdout:
            print_epilog(Path("output.txt"), None, "1.0.0")
            self.assertEqual(stdout.getvalue(), expected_stdout)

    @patch("platform.node", return_value="hostname")
    def test_print_epilog_no_json_and_txt_positive(self, mocked_node):
        expected_stdout = "\n" + \
                          "\n" + \
                          "The report was generated for the machine: hostname\n" + \
                          "by the Diagnostics Utility for Intel® oneAPI Toolkits 1.0.0\n"
        with patch('sys.stdout', new=StringIO()) as stdout:
            print_epilog(None, None, "1.0.0")
            self.assertEqual(stdout.getvalue(), expected_stdout)

    @patch("platform.node", return_value="hostname")
    def test_print_epilog_positive(self, mocked_node):
        expected_stdout = "\n" + \
                          "Console output file: output.txt\n" + \
                          "JSON output file: output.json\n" + \
                          "\n" + \
                          "The report was generated for the machine: hostname\n" + \
                          "by the Diagnostics Utility for Intel® oneAPI Toolkits 1.0.0\n"
        with patch('sys.stdout', new=StringIO()) as stdout:
            print_epilog(Path("output.txt"), Path("output.json"), "1.0.0")
            self.assertEqual(stdout.getvalue(), expected_stdout)


if __name__ == '__main__':
    unittest.main()
