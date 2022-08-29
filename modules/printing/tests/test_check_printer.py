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

from json import dumps  # noqa: E402
from copy import deepcopy  # noqa: E402
from io import StringIO  # noqa: E402
from os import terminal_size  # noqa: E402
from unittest.mock import patch  # noqa: E402

from modules.check.check import BaseCheck, CheckMetadataPy, \
    CheckSummary  # noqa: E402
from modules.printing.printer_helper import Colors  # noqa: E402
from modules.printing.check_printer import CheckSummaryPrinter, \
    _verbosity_processing, _get_status_message, \
    print_summary, print_short_summary, print_full_summary, \
    MAX_KEY_WIDTH, MIN_KEY_WIDTH  # noqa: E402
from modules.printing.tests.printing_test_helper import print_ex_mock  # noqa: E402

correct_result_dict_default = {
    "Value": {
        "Check": {
            "Value": "Data"
        }
    }
}

correct_result_dict_long_key = {
    "Value": {
        "CheckLongNameCheckLongName": {
            "Value": {
                "Subcheck1LongNameSubcheck1LongName": {
                    "Value": "SubcheckValue1",
                },
                "Subcheck2": {
                    "Value": "SubcheckValue1",
                }
            }
        }
    }
}

correct_result_dict_too_long_key = {
    "Value": {
        f"{'CheckLongName' * 10}": {
            "Value": "Data"
        }
    }
}

correct_result_dict = {
    "Value": {
        "Check1": {
            "Message": "Message is not required filed",
            "RetVal": "PASS",
            "Value": {
                "Subcheck1": {
                    "Verbosity": 4,
                    "Command": "Command is not required filed",
                    "Value": "SubcheckValue1",
                    "RetVal": "ERROR",
                    "HowToFix": "test decsription",
                    "AutomationFix": "command"
                },
                "Subcheck2": {
                    "Verbosity": 4,
                    "Value": {
                        "Subcheck1": {
                            "Verbosity": 4,
                            "Value": "SubCheckValue1",
                            "RetVal": "ERROR",
                            "HowToFix": "test decsription",
                            "AutomationFix": "command"
                        }
                    },
                    "RetVal": "ERROR",
                    "HowToFix": "test decsription",
                    "AutomationFix": "command"
                }
            }
        },
        "Check2": {
            "Verbosity": 0,
            "Command": "Command is not required filed",
            "RetVal": "WARNING",
            "Value": {
                "Subcheck1": {
                    "Verbosity": 1,
                    "Message": "Message is not required filed",
                    "Value": "SubcheckValue1",
                    "RetVal": "FAIL"
                },
                "Subcheck2": {
                    "Verbosity": 2,
                    "Message": "Message is not required filed",
                    "Value": "SubcheckValue2",
                    "RetVal": "INFO"
                }
            }
        }
    }
}

examine_correct_result_dict = {
    "Value": {
        "Check1": {
            "Verbosity": 0,
            "Message": "Message is not required filed",
            "RetVal": "PASS",
            "Value": "CheckValue"
        },
        "Check2": {
            "Verbosity": 0,
            "Command": "Command is not required filed",
            "RetVal": "WARNING",
            "Value": {
                "Subcheck1": {
                    "Verbosity": 1,
                    "Message": "Message is not required filed",
                    "Value": "SubcheckValue1NotEgual",
                    "RetVal": "FAIL"
                },
                "Subcheck2": {
                    "Verbosity": 1,
                    "Message": "Message is not required filed",
                    "Value": "SubcheckValue2",
                    "RetVal": "INFO"
                }
            }
        }
    }
}


class TestClassCheckSummaryPrinter(unittest.TestCase):

    @patch("modules.printing.check_printer.CheckSummaryPrinter._get_key_width", return_value=20)
    @patch("shutil.get_terminal_size", return_value=terminal_size((60, 0)))
    def setUp(self, mock_get_terminal_size, mock_get_key_width):
        self.check_printer = CheckSummaryPrinter(correct_result_dict_default, None)

    def test_init_positive(self):
        self.assertTrue(hasattr(self.check_printer, "key_width"))
        self.assertTrue(hasattr(self.check_printer, "result_width"))
        self.assertTrue(hasattr(self.check_printer, "value_width"))
        self.assertTrue(hasattr(self.check_printer, "output_file"))

    def test_init_negtive(self):
        incorrect_test_result_dict = {"Check": {"Value": "Data"}}
        with self.assertRaises(ValueError):
            CheckSummaryPrinter(incorrect_test_result_dict, None)

    def test__get_widths_positive(self):
        expected_list_widths = [6 + 2, 6 + 2, 9 + 4, 9 + 4, 9 + 6, 9 + 4, 9 + 4]
        real_list_widths = []
        check_printer = CheckSummaryPrinter(correct_result_dict, None)
        check_printer._get_widths(correct_result_dict, 0, real_list_widths)
        self.assertEqual(expected_list_widths, real_list_widths)

    @patch("shutil.get_terminal_size", return_value=terminal_size((60, 0)))
    def test__get_key_width_positive(self, mock_get_terminal_size):
        expected_width = 20
        check_printer = CheckSummaryPrinter(correct_result_dict, None)
        real_width = check_printer._get_key_width(correct_result_dict)
        self.assertEqual(expected_width, real_width)

    @patch("shutil.get_terminal_size", return_value=terminal_size((60, 0)))
    def test__get_key_width_min_found_positive(self, mock_get_terminal_size):
        expected_width = MIN_KEY_WIDTH
        check_printer = CheckSummaryPrinter(correct_result_dict_long_key, None)
        real_width = check_printer._get_key_width(correct_result_dict_long_key)
        self.assertEqual(expected_width, real_width)

    @patch("shutil.get_terminal_size", return_value=terminal_size((200, 0)))
    def test__get_key_width_found_positive(self, mock_get_terminal_size):
        expected_width = 40
        check_printer = CheckSummaryPrinter(correct_result_dict_long_key, None)
        real_width = check_printer._get_key_width(correct_result_dict_long_key)
        self.assertEqual(expected_width, real_width)

    @patch("shutil.get_terminal_size", return_value=terminal_size((60, 0)))
    def test__get_key_width_min_positive(self, mock_get_terminal_size):
        expected_width = MIN_KEY_WIDTH
        check_printer = CheckSummaryPrinter(correct_result_dict_too_long_key, None)
        real_width = check_printer._get_key_width(correct_result_dict_too_long_key)
        self.assertEqual(expected_width, real_width)

    @patch("shutil.get_terminal_size", return_value=terminal_size((200, 0)))
    def test__get_key_width_max_positive(self, mock_get_terminal_size):
        expected_width = MAX_KEY_WIDTH
        check_printer = CheckSummaryPrinter(correct_result_dict_too_long_key, None)
        real_width = check_printer._get_key_width(correct_result_dict_too_long_key)
        self.assertEqual(expected_width, real_width)

    def test__get_key_width_negative(self):
        with self.assertRaises(ValueError):
            self.check_printer._get_key_width({})

    def test__result_format_positive(self):
        result_str = "PASS"
        expected_result_format = [
            "PASS   "
        ]
        real_result_format = self.check_printer._result_format(result_str)
        self.assertEqual(expected_result_format, real_result_format)

    def test__result_format_negative(self):
        result_str = "RESULTLONG"
        with self.assertRaises(ValueError):
            self.check_printer._result_format(result_str)

    def test__value_format_value_nodashes_positive(self):
        expected_value_format = [
            "Value                          "
        ]
        real_value_format = self.check_printer._value_format("Value", False)
        self.assertEqual(expected_value_format, real_value_format)

    def test__value_format_novalue_dashes_positive(self):
        expected_value_format = [
            "-" * self.check_printer.value_width
        ]
        real_value_format = self.check_printer._value_format("", True)
        self.assertEqual(expected_value_format, real_value_format)

    def test__value_format_novalue_nodashes_positive(self):
        expected_value_format = [
            " " * self.check_printer.value_width
        ]
        real_value_format = self.check_printer._value_format("", False)
        self.assertEqual(expected_value_format, real_value_format)

    def test__value_format_value_dashes_positive(self):
        expected_value_format = [
            "Value--------------------------"
        ]
        real_value_format = self.check_printer._value_format("Value", True)
        self.assertEqual(expected_value_format, real_value_format)

    def test__value_format_long_value_dashes_positive(self):
        expected_value_format = [
            "ValueValueValueValueValueValue-",
            "ValueValueValueValue           "
        ]
        real_value_format = self.check_printer._value_format("Value" * 10, True)
        self.assertEqual(expected_value_format, real_value_format)

    def test__key_format_zero_depth_out_dashes_positive(self):
        expected_key_format = [
            "  Key---------------"
        ]
        real_key_format = self.check_printer._key_format("Key", 0, [True], True)
        self.assertEqual(expected_key_format, real_key_format)

    def test__key_format_zero_depth_long_key_positive(self):
        expected_key_format = [
            "  KeyKeyKeyKeyKey   ",
            "  KeyKeyKeyKeyKey   "
        ]
        real_key_format = self.check_printer._key_format("Key" * 10, 0, [True])
        self.assertEqual(expected_key_format, real_key_format)

    def test__key_format_zero_depth_out_nodashes_positive(self):
        expected_key_format = [
            "  Key               "
        ]
        real_key_format = self.check_printer._key_format("Key", 0, [True], False)
        self.assertEqual(expected_key_format, real_key_format)

    def test__key_format_zero_depth_noout_dashes_positive(self):
        expected_key_format = [
            "  Key---------------"
        ]
        real_key_format = self.check_printer._key_format("Key", 0, [False], True)
        self.assertEqual(expected_key_format, real_key_format)

    def test__key_format_zero_depth_noout_nodashes_positive(self):
        expected_key_format = [
            "  Key               "
        ]
        real_key_format = self.check_printer._key_format("Key", 0, [False], False)
        self.assertEqual(expected_key_format, real_key_format)

    def test__key_format_depth_out_positive(self):
        expected_key_format = [
            "    │ └─Key         "
        ]
        real_key_format = self.check_printer._key_format("Key", 3, [False, True, False, True])
        self.assertEqual(expected_key_format, real_key_format)

    def test__key_format_depth_noout_positive(self):
        expected_key_format = [
            "    │ ├─Key         "
        ]
        real_key_format = self.check_printer._key_format("Key", 3, [False, True, False, False])
        self.assertEqual(expected_key_format, real_key_format)

    def test__key_format_depth_long_key_positive(self):
        expected_key_format = [
            "  └─KeyKeyKeyKeyK   ",
            "    eyKeyKeyKeyKe   ",
            "    yKey            "
        ]
        real_key_format = self.check_printer._key_format("Key" * 10, 1, [True, True])
        self.assertEqual(expected_key_format, real_key_format)

    def test__string_format_zero_depth_out_positive(self):
        expected_string_format = [
            "  String                                           "
        ]
        real_string_format = self.check_printer._string_format("String", 0, [True])
        self.assertEqual(expected_string_format, real_string_format)

    def test__string_format_zero_depth_noout_positive(self):
        expected_string_format = [
            "  String                                           "
        ]
        real_string_format = self.check_printer._string_format("String", 0, [False])
        self.assertEqual(expected_string_format, real_string_format)

    def test__string_format_zero_depth_long_string_positive(self):
        expected_string_format = [
            "  StringStringStringStringStringStringStringStri   ",
            "  ngStringString                                   "
        ]
        real_string_format = self.check_printer._string_format("String" * 10, 0, [True])
        self.assertEqual(expected_string_format, real_string_format)

    def test__string_format_depth_out_positive(self):
        expected_string_format = [
            "    │ └ String                                     "
        ]
        real_string_format = self.check_printer._string_format("String", 3, [False, True, False, True])
        self.assertEqual(expected_string_format, real_string_format)

    def test__string_format_depth_noout_positive(self):
        expected_string_format = [
            "    │ │ String                                     "
        ]
        real_string_format = self.check_printer._string_format("String", 3, [False, True, False, False])
        self.assertEqual(expected_string_format, real_string_format)

    def test__string_format_depth_long_string_positive(self):
        expected_string_format = [
            "    │ │ StringStringStringStringStringStringStri   ",
            "    │ └ ngStringStringString                       "
        ]
        real_string_format = self.check_printer._string_format("String" * 10, 3, [False, True, False, True])
        self.assertEqual(expected_string_format, real_string_format)

    def test__message_format_positive(self):
        expected_message_format = [
            "  Message: String                                  "
        ]
        real_message_format = self.check_printer._message_format("String", 0, [False])
        self.assertEqual(expected_message_format, real_message_format)

    def test__command_format_positive(self):
        expected_command_format = [
            "  Command: String                                  "
        ]
        real_command_format = self.check_printer._command_format("String", 0, [False])
        self.assertEqual(expected_command_format, real_command_format)

    @patch("modules.printing.check_printer.print_ex", side_effect=print_ex_mock)
    def test_print_line_positive(self, mocked_print_ex):
        expected_stdout = "|  Key---------------Value--------------------------Res    |\n"
        with patch('sys.stdout', new=StringIO()) as stdout:
            self.check_printer.print_line(
                "Key",
                "Value",
                "Res",
                Colors.Default,
                0,
                [False]
            )
            self.assertEqual(expected_stdout, stdout.getvalue())

    @patch("modules.printing.check_printer.print_ex", side_effect=print_ex_mock)
    def test_print_line_long_key_positive(self, mocked_print_ex):
        expected_stdout = "|  KeyKeyKeyKeyKey---Value--------------------------Res    |\n" + \
                          "|  KeyKeyKeyKeyKey                                         |\n"
        with patch('sys.stdout', new=StringIO()) as stdout:
            self.check_printer.print_line(
                "Key" * 10,
                "Value",
                "Res",
                Colors.Default,
                0,
                [False]
            )
            self.assertEqual(expected_stdout, stdout.getvalue())

    @patch("modules.printing.check_printer.print_ex", side_effect=print_ex_mock)
    def test_print_line_long_value_positive(self, mocked_print_ex):
        expected_stdout = "|  Key---------------ValueValueValueValueValueValue-Res    |\n" + \
                          "|                    ValueValueValueValue                  |\n"
        with patch('sys.stdout', new=StringIO()) as stdout:
            self.check_printer.print_line(
                "Key",
                "Value" * 10,
                "Res",
                Colors.Default,
                0,
                [False]
            )
            self.assertEqual(expected_stdout, stdout.getvalue())

    @patch("modules.printing.check_printer.print_ex", side_effect=print_ex_mock)
    def test_print_line_depth_out_positive(self, mocked_print_ex):
        expected_stdout = "|  └─Key-------------Value--------------------------Res    |\n"
        with patch('sys.stdout', new=StringIO()) as stdout:
            self.check_printer.print_line(
                "Key",
                "Value",
                "Res",
                Colors.Default,
                1,
                [False, True]
            )
            self.assertEqual(expected_stdout, stdout.getvalue())

    @patch("modules.printing.check_printer.print_ex", side_effect=print_ex_mock)
    def test_print_line_depth_noout_positive(self, mocked_print_ex):
        expected_stdout = "|  ├─Key-------------Value--------------------------Res    |\n"
        with patch('sys.stdout', new=StringIO()) as stdout:
            self.check_printer.print_line(
                "Key",
                "Value",
                "Res",
                Colors.Default,
                1,
                [False, False]
            )
            self.assertEqual(expected_stdout, stdout.getvalue())

    @patch("modules.printing.check_printer.print_ex", side_effect=print_ex_mock)
    def test_print_line_depth_long_value_positive(self, mocked_print_ex):
        expected_stdout = "|    │ └─Key---------ValueValueValueValueValueValue-Res    |\n" + \
                          "|    │               ValueValueValueValue                  |\n"
        with patch('sys.stdout', new=StringIO()) as stdout:
            self.check_printer.print_line(
                "Key",
                "Value" * 10,
                "Res",
                Colors.Default,
                1,
                [False, True, False, True]
            )
            self.assertEqual(expected_stdout, stdout.getvalue())

    @patch("modules.printing.check_printer.print_ex", side_effect=print_ex_mock)
    def test_print_message_positive(self, mocked_print_ex):
        expected_stdout = "|  Message: String                                         |\n"
        with patch('sys.stdout', new=StringIO()) as stdout:
            self.check_printer.print_message("String", Colors.Default, 0, [False])
            self.assertEqual(expected_stdout, stdout.getvalue())

    @patch("modules.printing.check_printer.print_ex", side_effect=print_ex_mock)
    def test_print_command_positive(self, mocked_print_ex):
        expected_stdout = "|  Command: String                                         |\n"
        with patch('sys.stdout', new=StringIO()) as stdout:
            self.check_printer.print_command("String", 0, [False])
            self.assertEqual(expected_stdout, stdout.getvalue())

    @patch("modules.printing.check_printer.print_ex", side_effect=print_ex_mock)
    @patch("shutil.get_terminal_size", return_value=terminal_size((60, 0)))
    def test_print_summary_tree_positive(
            self,
            mock_get_terminal_size,
            mocked_print_ex):
        check_printer = CheckSummaryPrinter(correct_result_dict, None)
        expected_stdout = f"|  Check1                                           {Colors.Green}       {Colors.Default}|\n" + \
                          f"|{Colors.Green}  Message: Message is not required filed           {Colors.Default}       |\n" + \
                          f"|  ├─Subcheck1-------SubcheckValue1-----------------{Colors.Red}ERROR  {Colors.Default}|\n" + \
                          "|  │ Command: Command is not required filed                |\n" + \
                          f"|{Colors.Red}  │ How to fix: test decsription                   {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  │ Command to fix: command                        {Colors.Default}       |\n" + \
                          f"|  ├─Subcheck2                                      {Colors.Red}       {Colors.Default}|\n" + \
                          f"|{Colors.Red}  │ How to fix: test decsription                   {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  └ Command to fix: command                        {Colors.Default}       |\n" + \
                          f"|    ├─Subcheck1-----SubCheckValue1-----------------{Colors.Red}ERROR  {Colors.Default}|\n" + \
                          f"|{Colors.Red}    │ How to fix: test decsription                 {Colors.Default}       |\n" + \
                          f"|{Colors.Red}    └ Command to fix: command                      {Colors.Default}       |\n" + \
                          f"|  Check2                                           {Colors.Yellow}       {Colors.Default}|\n" + \
                          "|  Command: Command is not required filed                  |\n" + \
                          f"|  ├─Subcheck1-------SubcheckValue1-----------------{Colors.Red}FAIL   {Colors.Default}|\n" + \
                          f"|{Colors.Red}  │ Message: Message is not required filed         {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  │ How to fix: The developer of the check did     {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  │ not provide information on how to solve the    {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  │ problem. To see the solution to the problem,   {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  │ ask the developer of the check to fill in      {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  │ the \"HowToFix\" field.                          {Colors.Default}       |\n" + \
                          f"|  ├─Subcheck2-------SubcheckValue2-----------------{Colors.Blue}INFO   {Colors.Default}|\n" + \
                          f"|{Colors.Blue}  └ Message: Message is not required filed         {Colors.Default}       |\n"  # noqa: E501

        with patch('sys.stdout', new=StringIO()) as stdout:
            check_printer.print_summary_tree(correct_result_dict["Value"])
            self.assertEqual(expected_stdout, stdout.getvalue())

    @patch("modules.printing.check_printer.print_ex", side_effect=print_ex_mock)
    @patch("shutil.get_terminal_size", return_value=terminal_size((60, 0)))
    def test_print_summary_tree_examine_not_equal_positive(
            self,
            mock_get_terminal_size,
            mocked_print_ex):
        check_printer = CheckSummaryPrinter(correct_result_dict, None)
        expected_stdout = f"|  Check1                                           {Colors.Green}       {Colors.Default}|\n" + \
                          f"|{Colors.Green}  Message: Message is not required filed           {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  Message: The value is not a dictionary. The      {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  value is 'CheckValue'.                           {Colors.Default}       |\n" + \
                          f"|  ├─Subcheck1-------SubcheckValue1-----------------{Colors.Red}ERROR  {Colors.Default}|\n" + \
                          "|  │ Command: Command is not required filed                |\n" + \
                          f"|{Colors.Red}  │ How to fix: test decsription                   {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  │ Command to fix: command                        {Colors.Default}       |\n" + \
                          f"|  ├─Subcheck2                                      {Colors.Red}       {Colors.Default}|\n" + \
                          f"|{Colors.Red}  │ How to fix: test decsription                   {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  └ Command to fix: command                        {Colors.Default}       |\n" + \
                          f"|    ├─Subcheck1-----SubCheckValue1-----------------{Colors.Red}ERROR  {Colors.Default}|\n" + \
                          f"|{Colors.Red}    │ How to fix: test decsription                 {Colors.Default}       |\n" + \
                          f"|{Colors.Red}    └ Command to fix: command                      {Colors.Default}       |\n" + \
                          f"|  Check2                                           {Colors.Yellow}       {Colors.Default}|\n" + \
                          "|  Command: Command is not required filed                  |\n" + \
                          f"|  ├─Subcheck1-------SubcheckValue1-----------------{Colors.Red}FAIL   {Colors.Default}|\n" + \
                          f"|{Colors.Red}  │ Message: Message is not required filed         {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  │ How to fix: The developer of the check did     {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  │ not provide information on how to solve the    {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  │ problem. To see the solution to the problem,   {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  │ ask the developer of the check to fill in      {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  │ the \"HowToFix\" field.                          {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  │ Message: The values of the current and         {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  │ compared runs are not equal. The value is 'S   {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  │ ubcheckValue1NotEgual'!!!!!!!!!!!!!!!!!!!!!!   {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  │ !                                              {Colors.Default}       |\n" + \
                          f"|  ├─Subcheck2-------SubcheckValue2-----------------{Colors.Blue}INFO   {Colors.Default}|\n" + \
                          f"|{Colors.Blue}  └ Message: Message is not required filed         {Colors.Default}       |\n"  # noqa: E501
        with patch('sys.stdout', new=StringIO()) as stdout:
            check_printer.print_summary_tree(
                correct_result_dict["Value"],
                examine_summary=examine_correct_result_dict["Value"]
            )
            self.assertEqual(expected_stdout, stdout.getvalue())

    @patch("modules.printing.check_printer.print_ex", side_effect=print_ex_mock)
    @patch("shutil.get_terminal_size", return_value=terminal_size((60, 0)))
    def test_print_summary_tree_examine_equal_positive(
            self,
            mock_get_terminal_size,
            mocked_print_ex):
        check_printer = CheckSummaryPrinter(correct_result_dict, None)
        expected_stdout = f"|  Check1                                           {Colors.Green}       {Colors.Default}|\n" + \
                          f"|{Colors.Green}  Message: Message is not required filed           {Colors.Default}       |\n" + \
                          f"|  ├─Subcheck1-------SubcheckValue1-----------------{Colors.Red}ERROR  {Colors.Default}|\n" + \
                          "|  │ Command: Command is not required filed                |\n" + \
                          f"|{Colors.Red}  │ How to fix: test decsription                   {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  │ Command to fix: command                        {Colors.Default}       |\n" + \
                          f"|  ├─Subcheck2                                      {Colors.Red}       {Colors.Default}|\n" + \
                          f"|{Colors.Red}  │ How to fix: test decsription                   {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  └ Command to fix: command                        {Colors.Default}       |\n" + \
                          f"|    ├─Subcheck1-----SubCheckValue1-----------------{Colors.Red}ERROR  {Colors.Default}|\n" + \
                          f"|{Colors.Red}    │ How to fix: test decsription                 {Colors.Default}       |\n" + \
                          f"|{Colors.Red}    └ Command to fix: command                      {Colors.Default}       |\n" + \
                          f"|  Check2                                           {Colors.Yellow}       {Colors.Default}|\n" + \
                          "|  Command: Command is not required filed                  |\n" + \
                          f"|  ├─Subcheck1-------SubcheckValue1-----------------{Colors.Red}FAIL   {Colors.Default}|\n" + \
                          f"|{Colors.Red}  │ Message: Message is not required filed         {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  │ How to fix: The developer of the check did     {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  │ not provide information on how to solve the    {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  │ problem. To see the solution to the problem,   {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  │ ask the developer of the check to fill in      {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  │ the \"HowToFix\" field.                          {Colors.Default}       |\n" + \
                          f"|  ├─Subcheck2-------SubcheckValue2-----------------{Colors.Blue}INFO   {Colors.Default}|\n" + \
                          f"|{Colors.Blue}  └ Message: Message is not required filed         {Colors.Default}       |\n"  # noqa: E501
        with patch('sys.stdout', new=StringIO()) as stdout:
            check_printer.print_summary_tree(
                correct_result_dict["Value"],
                examine_summary=correct_result_dict["Value"]
            )
            self.assertEqual(expected_stdout, stdout.getvalue())


class TestVerbosityProcessing(unittest.TestCase):

    def setUp(self):
        self.summary = correct_result_dict["Value"]

    def test__verbosity_processing_no_delete_positive(self):
        expected_processed_summary = self.summary
        real_processed_summary = deepcopy(self.summary)
        _verbosity_processing(real_processed_summary, 5)
        self.assertEqual(expected_processed_summary, real_processed_summary)

    def test__verbosity_processing_positive(self):
        expected_processed_summary = {
            "Check1": {
                "Message": "Message is not required filed",
                "RetVal": "PASS",
                "Value": {}
            },
            "Check2": {
                "Verbosity": 0,
                "RetVal": "WARNING",
                "Value": {
                    "Subcheck1": {
                        "Verbosity": 1,
                        "Message": "Message is not required filed",
                        "Value": "SubcheckValue1",
                        "RetVal": "FAIL"
                    },
                    "Subcheck2": {
                        "Verbosity": 2,
                        "Message": "Message is not required filed",
                        "Value": "SubcheckValue2",
                        "RetVal": "INFO"
                    }
                }
            }
        }
        real_processed_summary = deepcopy(self.summary)
        _verbosity_processing(real_processed_summary, 2)
        self.assertEqual(expected_processed_summary, real_processed_summary)


class TestStatusMessage(unittest.TestCase):

    def setUp(self):
        self.summary = correct_result_dict["Value"]

    def test__get_status_message_positive(self):
        expected_status_messages = ["Message is not required filed"]
        real_status_messages = _get_status_message(self.summary, "PASS")
        self.assertEqual(expected_status_messages, real_status_messages)

    def test__get_status_message_no_messages_positive(self):
        expected_status_messages = []
        real_status_messages = _get_status_message(self.summary, "ERROR")
        self.assertEqual(expected_status_messages, real_status_messages)


class BasePrintSummary(unittest.TestCase):

    def setUp(self):
        self.check_list = [
            BaseCheck(
                metadata=CheckMetadataPy(
                    name="name_of_check",
                    type="type",
                    tags="tag1,tag2,tag3",
                    descr="description",
                    dataReq="{}",
                    merit=0,
                    timeout=10,
                    version="0",
                    run="run"
                ),
                summary=CheckSummary(
                    result=dumps(correct_result_dict)
                )
            )
        ]


class TestPrintFullSummary(BasePrintSummary):

    @patch("modules.printing.check_printer.print_ex", side_effect=print_ex_mock)
    @patch("shutil.get_terminal_size", return_value=terminal_size((60, 0)))
    def test_print_full_summary_positive(
            self,
            mock_get_terminal_size,
            mocked_print_ex):
        expected_stdout = "\n" + \
                          "============================================================\n" + \
                          "Check name: name_of_check\n" + \
                          "Description: description\n" + \
                          "============================================================\n" + \
                          "\n" + \
                          f"|  Check1                                           {Colors.Green}       {Colors.Default}|\n" + \
                          f"|{Colors.Green}  Message: Message is not required filed           {Colors.Default}       |\n" + \
                          f"|  ├─Subcheck1-------SubcheckValue1-----------------{Colors.Red}ERROR  {Colors.Default}|\n" + \
                          "|  │ Command: Command is not required filed                |\n" + \
                          f"|{Colors.Red}  │ How to fix: test decsription                   {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  │ Command to fix: command                        {Colors.Default}       |\n" + \
                          f"|  ├─Subcheck2                                      {Colors.Red}       {Colors.Default}|\n" + \
                          f"|{Colors.Red}  │ How to fix: test decsription                   {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  └ Command to fix: command                        {Colors.Default}       |\n" + \
                          f"|    ├─Subcheck1-----SubCheckValue1-----------------{Colors.Red}ERROR  {Colors.Default}|\n" + \
                          f"|{Colors.Red}    │ How to fix: test decsription                 {Colors.Default}       |\n" + \
                          f"|{Colors.Red}    └ Command to fix: command                      {Colors.Default}       |\n" + \
                          f"|  Check2                                           {Colors.Yellow}       {Colors.Default}|\n" + \
                          "|  Command: Command is not required filed                  |\n" + \
                          f"|  ├─Subcheck1-------SubcheckValue1-----------------{Colors.Red}FAIL   {Colors.Default}|\n" + \
                          f"|{Colors.Red}  │ Message: Message is not required filed         {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  │ How to fix: The developer of the check did     {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  │ not provide information on how to solve the    {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  │ problem. To see the solution to the problem,   {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  │ ask the developer of the check to fill in      {Colors.Default}       |\n" + \
                          f"|{Colors.Red}  │ the \"HowToFix\" field.                          {Colors.Default}       |\n" + \
                          f"|  ├─Subcheck2-------SubcheckValue2-----------------{Colors.Blue}INFO   {Colors.Default}|\n" + \
                          f"|{Colors.Blue}  └ Message: Message is not required filed         {Colors.Default}       |\n"  # noqa: E501
        with patch('sys.stdout', new=StringIO()) as stdout:
            print_full_summary(self.check_list, 5, None)
            self.assertEqual(stdout.getvalue(), expected_stdout)

    @patch("modules.printing.check_printer.print_ex", side_effect=print_ex_mock)
    @patch("shutil.get_terminal_size", return_value=terminal_size((60, 0)))
    def test_print_full_summary_none_positive(
            self,
            mock_get_terminal_size,
            mocked_print_ex):
        expected_stdout = ""
        with patch('sys.stdout', new=StringIO()) as stdout:
            print_full_summary([BaseCheck()], 5, None)
            self.assertEqual(stdout.getvalue(), expected_stdout)

    @patch("modules.printing.check_printer.print_ex", side_effect=print_ex_mock)
    @patch("shutil.get_terminal_size", return_value=terminal_size((60, 0)))
    @patch("json.loads", return_value={})
    def test_print_full_summary_empty_summary_positive(
            self, mock_loads,
            mock_get_terminal_size,
            mocked_print_ex):
        expected_stdout = "\n" + \
                          "============================================================\n" + \
                          "Check name: name_of_check\n" + \
                          "Description: description\n" + \
                          "============================================================\n" + \
                          "\n" + \
                          f"{Colors.Red}Incorrect or empty JSON format.{Colors.Default}\n"  # noqa: E501
        with patch('sys.stdout', new=StringIO()) as stdout:
            print_full_summary(self.check_list, 5, None)
            self.assertEqual(stdout.getvalue(), expected_stdout)

    @patch("modules.printing.check_printer.print_ex", side_effect=print_ex_mock)
    @patch("shutil.get_terminal_size", return_value=terminal_size((60, 0)))
    @patch("json.loads", return_value={"a": 1})
    def test_print_full_summary_incorrect_summary_positive(
            self,
            mock_loads,
            mock_get_terminal_size,
            mocked_print_ex):
        expected_stdout = "\n" + \
                          "============================================================\n" + \
                          "Check name: name_of_check\n" + \
                          "Description: description\n" + \
                          "============================================================\n" + \
                          "\n" + \
                          f"{Colors.Red}Incorrect or empty JSON format.{Colors.Default}\n"  # noqa: E501
        with patch('sys.stdout', new=StringIO()) as stdout:
            print_full_summary(self.check_list, 5, None)
            self.assertEqual(stdout.getvalue(), expected_stdout)

    @patch("modules.printing.check_printer.print_ex", side_effect=print_ex_mock)
    @patch("shutil.get_terminal_size", return_value=terminal_size((60, 0)))
    def test_print_full_summary_incorrect_examine_positive(
            self,
            mock_get_terminal_size,
            mocked_print_ex):
        expected_stdout = "\n" + \
                          "============================================================\n" + \
                          "Check name: name_of_check\n" + \
                          "Description: description\n" + \
                          "============================================================\n" + \
                          "\n" + \
                          f"{Colors.Red}Incorrect or empty JSON format.{Colors.Default}\n"  # noqa: E501
        with patch('sys.stdout', new=StringIO()) as stdout:
            print_full_summary(self.check_list, 5, None, examine_data={})
            self.assertEqual(stdout.getvalue(), expected_stdout)


class TestPrintShortSummary(BasePrintSummary):

    @patch("modules.printing.check_printer.print_ex", side_effect=print_ex_mock)
    @patch("shutil.get_terminal_size", return_value=terminal_size((60, 0)))
    def test_print_short_summary_positive(
            self,
            mock_get_terminal_size,
            mocked_print_ex):
        expected_stdout = "============================================================\n" + \
                          "Check name: name_of_check\n" + \
                          "Description: description\n" + \
                          f"Result status: {Colors.Red}ERROR{Colors.Default}\n" + \
                          "============================================================\n" + \
                          "\n" + \
                          f"1 CHECK: 0 {Colors.Green}PASS{Colors.Default}, 0 {Colors.Red}FAIL{Colors.Default}, 0 {Colors.Yellow}WARNINGS{Colors.Default}, 1 {Colors.Red}ERROR{Colors.Default}\n"  # noqa: E501
        with patch('sys.stdout', new=StringIO()) as stdout:
            print_short_summary(self.check_list, None)
            self.assertEqual(stdout.getvalue(), expected_stdout)

    @patch("modules.printing.check_printer.print_ex", side_effect=print_ex_mock)
    @patch("shutil.get_terminal_size", return_value=terminal_size((60, 0)))
    def test_print_short_summary_none_positive(
            self,
            mock_get_terminal_size,
            mocked_print_ex):
        expected_stdout = f"1 CHECK: 0 {Colors.Green}PASS{Colors.Default}, 0 {Colors.Red}FAIL{Colors.Default}, 0 {Colors.Yellow}WARNINGS{Colors.Default}, 0 {Colors.Red}ERRORS{Colors.Default}\n"  # noqa: E501
        with patch('sys.stdout', new=StringIO()) as stdout:
            print_short_summary([BaseCheck()], None)
            self.assertEqual(stdout.getvalue(), expected_stdout)

    @patch("modules.printing.check_printer.print_ex", side_effect=print_ex_mock)
    @patch("shutil.get_terminal_size", return_value=terminal_size((60, 0)))
    @patch("json.loads", return_value={})
    def test_print_short_summary_empty_summary_positive(
            self,
            mock_loads,
            mock_get_terminal_size,
            mocked_print_ex):
        expected_stdout = "============================================================\n" + \
                          "Check name: name_of_check\n" + \
                          "Description: description\n" + \
                          f"Result status: {Colors.Red}ERROR{Colors.Default}\n" + \
                          "============================================================\n" + \
                          "\n" + \
                          f"1 CHECK: 0 {Colors.Green}PASS{Colors.Default}, 0 {Colors.Red}FAIL{Colors.Default}, 0 {Colors.Yellow}WARNINGS{Colors.Default}, 1 {Colors.Red}ERROR{Colors.Default}\n"  # noqa: E501
        with patch('sys.stdout', new=StringIO()) as stdout:
            print_short_summary(self.check_list, None)
            self.assertEqual(stdout.getvalue(), expected_stdout)

    @patch("modules.printing.check_printer.print_ex", side_effect=print_ex_mock)
    @patch("shutil.get_terminal_size", return_value=terminal_size((60, 0)))
    @patch("json.loads", return_value={"a": 1})
    def test_print_short_summary_incorrect_summary_positive(
            self,
            mock_loads,
            mock_get_terminal_size,
            mocked_print_ex):
        expected_stdout = "============================================================\n" + \
                          "Check name: name_of_check\n" + \
                          "Description: description\n" + \
                          f"Result status: {Colors.Red}ERROR{Colors.Default}\n" + \
                          "============================================================\n" + \
                          "\n" + \
                          f"1 CHECK: 0 {Colors.Green}PASS{Colors.Default}, 0 {Colors.Red}FAIL{Colors.Default}, 0 {Colors.Yellow}WARNINGS{Colors.Default}, 1 {Colors.Red}ERROR{Colors.Default}\n"  # noqa: E501
        with patch('sys.stdout', new=StringIO()) as stdout:
            print_short_summary(self.check_list, None)
            self.assertEqual(stdout.getvalue(), expected_stdout)

    @patch("modules.printing.check_printer.print_ex", side_effect=print_ex_mock)
    @patch("shutil.get_terminal_size", return_value=terminal_size((60, 0)))
    @patch("modules.printing.check_printer._get_status_message", return_value=["Message1", "Message2"])
    def test_print_short_summary_messages_positive(
            self,
            mock_get_status_message,
            mock_get_terminal_size,
            mocked_print_ex):
        expected_stdout = "============================================================\n" + \
                          "Check name: name_of_check\n" + \
                          "Description: description\n" + \
                          f"Result status: {Colors.Red}ERROR{Colors.Default}\n" + \
                          f"{Colors.Red}Message1{Colors.Default}\n" + \
                          f"{Colors.Red}Message2{Colors.Default}\n" + \
                          "============================================================\n" + \
                          "\n" + \
                          f"1 CHECK: 0 {Colors.Green}PASS{Colors.Default}, 0 {Colors.Red}FAIL{Colors.Default}, 0 {Colors.Yellow}WARNINGS{Colors.Default}, 1 {Colors.Red}ERROR{Colors.Default}\n"  # noqa: E501
        with patch('sys.stdout', new=StringIO()) as stdout:
            print_short_summary(self.check_list, None)
            self.assertEqual(stdout.getvalue(), expected_stdout)


class TestPrintSummary(BasePrintSummary):

    @patch("modules.printing.check_printer.print_ex", side_effect=print_ex_mock)
    @patch("modules.printing.check_printer.print_short_summary")
    @patch("modules.printing.check_printer.print_full_summary")
    def test_print_summary_short_positive(
            self,
            mock_print_full_summary,
            mock_print_short_summary,
            mocked_print_ex):
        expected_stdout = f"\n{Colors.Yellow}Checks results:{Colors.Default}\n\n"
        with patch('sys.stdout', new=StringIO()) as stdout:
            print_summary(self.check_list, -1, None)
            self.assertEqual(stdout.getvalue(), expected_stdout)
            mock_print_short_summary.assert_called_once_with(self.check_list, None)
            mock_print_full_summary.assert_not_called()

    @patch("modules.printing.check_printer.print_ex", side_effect=print_ex_mock)
    @patch("modules.printing.check_printer.print_short_summary")
    @patch("modules.printing.check_printer.print_full_summary")
    def test_print_summary_full_positive(
            self,
            mock_print_full_summary,
            mock_print_short_summary,
            mocked_print_ex):
        expected_stdout = f"\n{Colors.Yellow}Checks results:{Colors.Default}\n\n"
        with patch('sys.stdout', new=StringIO()) as stdout:
            print_summary(self.check_list, 5, None)
            self.assertEqual(stdout.getvalue(), expected_stdout)
            mock_print_full_summary.assert_called_once_with(self.check_list, 5, None, None)
            mock_print_short_summary.assert_not_called()


if __name__ == '__main__':
    unittest.TestCase.maxDiff = None
    unittest.main()
