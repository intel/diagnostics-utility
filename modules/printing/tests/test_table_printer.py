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
from unittest.mock import patch  # noqa: E402

from modules.printing.printer_helper import Aligment, Colors  # noqa: E402
from modules.printing.table_printer import draw_info_row, draw_line  # noqa: E402


class TestDrawLine(unittest.TestCase):

    def test_draw_line_default_positive(self):
        col_width = 7
        expected_stdout = "+-------+-------+-------+\n"
        with patch('sys.stdout', new=StringIO()) as stdout:
            draw_line([col_width] * 3, None)
            self.assertEqual(stdout.getvalue(), expected_stdout)

    def test_draw_line_empty_positive(self):
        expected_stdout = ""
        with patch('sys.stdout', new=StringIO()) as stdout:
            draw_line([], None)
            self.assertEqual(stdout.getvalue(), expected_stdout)


class TestDrawInfoRow(unittest.TestCase):

    def test_drow_info_row_default_positive(self):
        col_width = 7
        expected_stdout = "| col_1 | col_2 | col_3 |\n" + \
                          "+-------+-------+-------+\n"
        with patch('sys.stdout', new=StringIO()) as stdout:
            draw_info_row(
                [col_width] * 3,
                ["col_1", "col_2", "col_3"],
                None
            )
            self.assertEqual(stdout.getvalue(), expected_stdout)

    def test_drow_info_row_no_sep_line_positive(self):
        col_width = 7
        expected_stdout = "| col_1 | col_2 | col_3 |\n"
        with patch('sys.stdout', new=StringIO()) as stdout:
            draw_info_row(
                [col_width] * 3,
                ["col_1", "col_2", "col_3"],
                None,
                separator_line=False
            )
            self.assertEqual(stdout.getvalue(), expected_stdout)

    def test_drow_info_row_colored_positive(self):
        col_width = 7
        expected_stdout = f"|{Colors.Yellow} col_1 {Colors.Default}|{Colors.Yellow} col_2 {Colors.Default}|{Colors.Yellow} col_3 {Colors.Default}|\n"   # noqa: E501
        with patch('sys.stdout', new=StringIO()) as stdout:
            draw_info_row(
                [col_width] * 3,
                ["col_1", "col_2", "col_3"],
                None,
                column_colors=[Colors.Yellow] * 3,
                separator_line=False
            )
            self.assertEqual(stdout.getvalue(), expected_stdout)

    def test_drow_info_row_colored_different_len_positive(self):
        col_width = 7
        expected_stdout = f"|{Colors.Yellow} col_1 {Colors.Default}|{Colors.Yellow} col_2 {Colors.Default}| col_3 |\n"   # noqa: E501
        with patch('sys.stdout', new=StringIO()) as stdout:
            draw_info_row(
                [col_width] * 3,
                ["col_1", "col_2", "col_3"],
                None,
                column_colors=[Colors.Yellow] * 2,
                separator_line=False
            )
            self.assertEqual(stdout.getvalue(), expected_stdout)

    def test_drow_info_row_aligned_positive(self):
        col_width = 11
        expected_stdout = "|     col_1 |     col_2 |     col_3 |\n"
        with patch('sys.stdout', new=StringIO()) as stdout:
            draw_info_row(
                [col_width] * 3,
                ["col_1", "col_2", "col_3"],
                None,
                column_aligment=[Aligment.r] * 3,
                separator_line=False
            )
            self.assertEqual(stdout.getvalue(), expected_stdout)

    def test_drow_info_row_aligned_different_len_positive(self):
        col_width = 11
        expected_stdout = "|     col_1 |     col_2 | col_3     |\n"
        with patch('sys.stdout', new=StringIO()) as stdout:
            draw_info_row(
                [col_width] * 3,
                ["col_1", "col_2", "col_3"],
                None, column_aligment=[Aligment.r] * 2,
                separator_line=False
            )
            self.assertEqual(stdout.getvalue(), expected_stdout)

    def test_drow_info_row_too_long_string_positive(self):
        col_width = 6
        expected_stdout = "| colu | colu | colu |\n" + \
                          "| mn_1 | mn_2 | mn_3 |\n"
        with patch('sys.stdout', new=StringIO()) as stdout:
            draw_info_row(
                [col_width] * 3,
                ["column_1", "column_2", "column_3"],
                None,
                separator_line=False
            )
            self.assertEqual(stdout.getvalue(), expected_stdout)

    def test_drow_info_row_different_len_positive(self):
        col_width = 7
        expected_stdout = ""
        with patch('sys.stdout', new=StringIO()) as stdout:
            draw_info_row(
                [col_width] * 5,
                ["col_1", "col_2", "col_3"],
                None
            )
            self.assertEqual(stdout.getvalue(), expected_stdout)


if __name__ == '__main__':
    unittest.main()
