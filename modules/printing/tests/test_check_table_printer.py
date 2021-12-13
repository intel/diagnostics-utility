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
from typing import List  # noqa: E402
from os import terminal_size  # noqa: E402
from unittest.mock import patch  # noqa: E402

from modules.check import BaseCheck, CheckMetadataPy  # noqa: E402
from modules.printing.printer_helper import Colors  # noqa: E402
from modules.printing.check_table_printer import print_metadata  # noqa: E402


class TestPrintMetadata(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.check_list: List[BaseCheck] = [
            BaseCheck(
                metadata=CheckMetadataPy(
                    name="name_of_check",
                    type="type",
                    tags="tag1,tag2,tag3",
                    descr="description",
                    dataReq="{}",
                    rights="user",
                    timeout=10,
                    version="0",
                    run="run"
                )
            ),
            BaseCheck(
                metadata=CheckMetadataPy(
                    name="too_long_name_of_check",
                    type="type",
                    tags="tag1,tag2,tag3",
                    descr="description",
                    dataReq="{}",
                    rights="user",
                    timeout=10,
                    version="0",
                    run="run"
                )
            )
        ]

    @patch("shutil.get_terminal_size", return_value=terminal_size((60, 0)))
    def test_print_metadata_console_min_width_less_positive(self, mock_get_terminal_size):
        expected_stdout = "+---------------+----------+----------+--------------------+\n" + \
                          f"|{Colors.Yellow}  Check name   {Colors.Default}|{Colors.Yellow}   Tags   {Colors.Default}|{Colors.Yellow}  Rights  {Colors.Default}|{Colors.Yellow}    Description     {Colors.Default}|\n" + \
                          "+---------------+----------+----------+--------------------+\n" + \
                          "| name_of_check | tag1     | user     | description        |\n" + \
                          "|               | tag2     |          |                    |\n" + \
                          "|               | tag3     |          |                    |\n" + \
                          "+---------------+----------+----------+--------------------+\n"  # noqa: E501

        with patch('sys.stdout', new=StringIO()) as stdout:
            print_metadata(self.check_list[0:1], None)
            self.assertEqual(stdout.getvalue(), expected_stdout)

    @patch("shutil.get_terminal_size", return_value=terminal_size((60, 0)))
    def test_print_metadata_console_min_width_more_positive(self, mock_get_terminal_size):
        expected_stdout = "+--------------------+----------+----------+---------------+\n" + \
                          f"|{Colors.Yellow}     Check name     {Colors.Default}|{Colors.Yellow}   Tags   {Colors.Default}|{Colors.Yellow}  Rights  {Colors.Default}|{Colors.Yellow}  Description  {Colors.Default}|\n" + \
                          "+--------------------+----------+----------+---------------+\n" + \
                          "| too_long_name_of_c | tag1     | user     | description   |\n" + \
                          "| heck               | tag2     |          |               |\n" + \
                          "|                    | tag3     |          |               |\n" + \
                          "+--------------------+----------+----------+---------------+\n"  # noqa: E501

        with patch('sys.stdout', new=StringIO()) as stdout:
            print_metadata(self.check_list[1:2], None)
            self.assertEqual(stdout.getvalue(), expected_stdout)

    @patch("shutil.get_terminal_size", return_value=terminal_size((70, 0)))
    def test_print_metadata_console_width_more_positive(self, mock_get_terminal_size):
        expected_stdout = "+------------------------+----------+----------+---------------------+\n" + \
                          f"|{Colors.Yellow}       Check name       {Colors.Default}|{Colors.Yellow}   Tags   {Colors.Default}|{Colors.Yellow}  Rights  {Colors.Default}|{Colors.Yellow}     Description     {Colors.Default}|\n" + \
                          "+------------------------+----------+----------+---------------------+\n" + \
                          "| too_long_name_of_check | tag1     | user     | description         |\n" + \
                          "|                        | tag2     |          |                     |\n" + \
                          "|                        | tag3     |          |                     |\n" + \
                          "+------------------------+----------+----------+---------------------+\n"  # noqa: E501

        with patch('sys.stdout', new=StringIO()) as stdout:
            print_metadata(self.check_list[1:2], None)
            self.assertEqual(stdout.getvalue(), expected_stdout)


if __name__ == '__main__':
    unittest.main()
