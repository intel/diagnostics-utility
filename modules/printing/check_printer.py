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

import shutil
import json
import logging
import itertools

from pathlib import Path
from textwrap import wrap
from typing import Dict, List, Optional

from modules.printing.printer_helper import Colors
from modules.printing.printer import print_ex
from modules.check.check import BaseCheck


PREFIX_KEY_IN = '\u251C' + '\u2500'
PREFIX_KEY_OUT = '\u2514' + '\u2500'
PREFIX_IN = '\u2502' + " "
PREFIX_OUT = '\u2514' + " "

SEPARATOR = "|"
MIN_KEY_WIDTH = 20
MAX_KEY_WIDTH = 70
SEPARATOR_WIDTH = 2
CONSOLE_MIN = 60


class CheckSummaryPrinter:
    def __init__(self, summary: Dict, output_file: Optional[Path]) -> None:
        self.output_file = output_file

        self.key_width = self._get_key_width(summary)
        self.result_width = 7
        self.value_width = max(CONSOLE_MIN, shutil.get_terminal_size().columns) - \
            self.key_width - self.result_width - SEPARATOR_WIDTH

    def _get_widths(self, summary: Dict, depth: int, widths: List[int]):
        for key, value in summary.items():
            if key == 'CheckResult' and type(value) is dict:
                shift = 2 if depth == 0 else depth * 2 + 2
                widths.extend([len(nested_key) + shift for nested_key in [*value]])
                for _, nested_value in value.items():
                    self._get_widths(nested_value, depth + 1, widths)

    def _get_key_width(self, summary: Dict) -> int:
        widths = []
        self._get_widths(summary, 0, widths)
        if not widths:
            raise ValueError("Cannot get information about key widths.")
        for key_width in range(MIN_KEY_WIDTH, MAX_KEY_WIDTH + 1, 10):
            ex_widths = [width for width in widths if width > key_width]
            if len(ex_widths)/len(widths) < 0.1:
                return key_width if max(CONSOLE_MIN, shutil.get_terminal_size().columns) > 2 * key_width \
                    else MIN_KEY_WIDTH
        return MAX_KEY_WIDTH if max(CONSOLE_MIN, shutil.get_terminal_size().columns) > 2 * MAX_KEY_WIDTH \
            else MIN_KEY_WIDTH

    def _result_format(self, res: str) -> List[str]:
        if len(res) > self.result_width:
            raise ValueError("Output string is too long to display.")
        spaces = self.result_width - len(res)
        return [res + " " * spaces]

    def _value_format(self, value: str, dashes: bool = False) -> List[str]:
        format_lines = []
        if value:
            value_lines = wrap(value, self.value_width - 1)
            for num, line in enumerate(value_lines):
                num_end = self.value_width - len(line)
                end = "-" * num_end if dashes and num == 0 else " " * num_end
                format_lines.append(line + end)
        else:
            symbol = "-" if dashes else " "
            format_lines.append(symbol * self.value_width)
        return format_lines

    def _key_format(self, key: str, depth: int, out: List[bool], dashes: bool = False) -> List[str]:
        format_lines = []
        prefix = PREFIX_KEY_OUT if out[depth] else PREFIX_KEY_IN
        prefix_tr = "  " if out[depth] else PREFIX_IN
        shift = "  "
        if depth > 0:
            for depth_out in out[1:-1]:
                shift += "  " if depth_out else PREFIX_IN
        shift_tr = shift if depth == 0 else shift + prefix_tr
        shift_fr = shift if depth == 0 else shift + prefix
        key_lines = wrap(key, self.key_width - len(shift_fr) - 3)
        for num, line in enumerate(key_lines):
            num_end = self.key_width - len(line) - len(shift_fr)
            end = "-" * num_end if dashes and num == 0 else " " * num_end
            format_lines.append(shift_fr + line + end) if num == 0 \
                else format_lines.append(shift_tr + line + end)
        return format_lines

    def _string_format(self, string: str, depth: int, out: List[bool]) -> List[str]:
        prefix = PREFIX_OUT if out[depth] else PREFIX_IN
        shift = "  "
        if depth > 0:
            for depth_out in out[1:-1]:
                shift += "  " if depth_out else PREFIX_IN
        shift_in = shift if depth == 0 else shift + PREFIX_IN
        shift_out = shift if depth == 0 else shift + prefix
        string_lines = wrap(string, self.key_width + self.value_width - len(shift_in) - 3)
        format_lines = []
        for num, line in enumerate(string_lines):
            num_end = self.key_width + self.value_width - len(line) - len(shift_in)
            end = " " * num_end
            format_lines.append(shift_out + line + end) if num == len(string_lines) - 1 \
                else format_lines.append(shift_in + line + end)
        return format_lines

    def _list_format(self, strings: List[str], depth: int, out: List[bool]) -> List[str]:
        prefix = PREFIX_IN
        shift = "  "
        if depth > 0:
            for depth_out in out[1:-1]:
                shift += "  " if depth_out else PREFIX_IN
        shift_in = shift if depth == 0 else shift + PREFIX_IN
        shift_out = shift if depth == 0 else shift + prefix
        string_lines = list(itertools.chain(*
                            (wrap(s, self.key_width + self.value_width - len(shift_in) - 3)
                                for s in strings)))
        format_lines = []
        for num, line in enumerate(string_lines):
            num_end = self.key_width + self.value_width - len(line) - len(shift_in)
            end = " " * num_end
            format_lines.append(shift_out + line + end) if num == len(string_lines) - 1 \
                else format_lines.append(shift_in + line + end)
        return format_lines

    def _message_format(self, message: str, depth: int, out: List[bool]) -> List[str]:
        message = f'Message: {message}'
        return self._string_format(message, depth, out)

    def _logs_format(self, logs: List[str], depth: int, out: List[bool]) -> List[str]:
        logs.insert(0, 'Logs: ')
        return self._list_format(logs, depth, out)

    def _command_format(self, command: str, depth: int, out: List[bool]) -> List[str]:
        command = f'Command: {command}'
        return self._string_format(command, depth, out)

    def _how_to_fix_format(self, how_to_fix_message: str, depth: int, out: List[bool]) -> List[str]:
        command = f'How to fix: {how_to_fix_message}'
        return self._string_format(command, depth, out)

    def _automation_fix_format(self, _automation_fix_command: str, depth: int, out: List[bool]) -> List[str]:
        command = f'Command to fix: {_automation_fix_command}'
        return self._string_format(command, depth, out)

    def print_line(
            self, key: str, value: str, result: str, color,
            depth: int, out: List[bool]) -> None:
        key_format_lines = self._key_format(key, depth, out, bool(len(value)) or bool(len(result)))
        value_format_lines = self._value_format(value, bool(len(result)))
        result_format_lines = self._result_format(result)
        num_break_lines = max(
            len(key_format_lines),
            len(value_format_lines),
            len(result_format_lines)
        )
        for i in range(num_break_lines - len(key_format_lines)):
            prefix = "  " if out[depth] else PREFIX_IN
            shift = "  "
            if depth > 0:
                for depth_out in out[1:-1]:
                    shift += "  " if depth_out else PREFIX_IN
            shift = shift if depth == 0 else shift + prefix
            key_format_lines.append(shift + " " * (self.key_width - len(shift)))
        for i in range(num_break_lines - len(value_format_lines)):
            value_format_lines.append(" " * self.value_width)
        for i in range(num_break_lines - len(result_format_lines)):
            result_format_lines.append(" " * self.result_width)
        for i in range(num_break_lines):
            print_ex(SEPARATOR + key_format_lines[i] +
                     value_format_lines[i], self.output_file, end="")
            print_ex(result_format_lines[i], self.output_file, color=color, end="")
            print_ex(SEPARATOR, self.output_file)

    def print_message(self, message: str, color, depth: int, out: List[bool]) -> None:
        message_format_lines = self._message_format(message, depth, out)
        for line in message_format_lines:
            print_ex(SEPARATOR, self.output_file, end="")
            print_ex(line, self.output_file, color=color, end="")
            print_ex(self._result_format("")[0] + SEPARATOR, self.output_file)

    def print_logs(self, logs: List[str], color, depth: int, out: List[bool]) -> None:
        logs_format_lines = self._logs_format(logs, depth, out)
        for line in logs_format_lines:
            print_ex(SEPARATOR, self.output_file, end="")
            print_ex(line, self.output_file, color=color, end="")
            print_ex(self._result_format("")[0] + SEPARATOR, self.output_file)

    def print_how_to_fix(self, how_to_fix: str, color, depth: int, out: List[bool]) -> None:
        how_to_fix_lines = self._how_to_fix_format(how_to_fix, depth, out)
        for line in how_to_fix_lines:
            print_ex(SEPARATOR, self.output_file, end="")
            print_ex(line, self.output_file, color=color, end="")
            print_ex(self._result_format("")[0] + SEPARATOR, self.output_file)

    def print_automation_fix(self, automation_fix: str, color, depth: int, out: List[bool]) -> None:
        automation_fix_lines = self._automation_fix_format(automation_fix, depth, out)
        for line in automation_fix_lines:
            print_ex(SEPARATOR, self.output_file, end="")
            print_ex(line, self.output_file, color=color, end="")
            print_ex(self._result_format("")[0] + SEPARATOR, self.output_file)

    def print_command(self, command: str, depth: int, out: List[bool]) -> None:
        command_format_lines = self._command_format(command, depth, out)
        for line in command_format_lines:
            print_ex(SEPARATOR + line + self._result_format("")[0] + SEPARATOR, self.output_file)

    def print_summary_tree(self, summary, depth: int = 0,
                           out: List[bool] = [], examine_summary: Optional[Dict] = None) -> None:
        for num, item in enumerate(summary.items()):
            key, data = item
            current_out = True if num == len(summary) - 1 else False

            print_solution_description = False
            how_to_fix_default_message = \
                "The developer of the check did not provide information on how to solve the problem. " \
                "To see the solution to the problem, ask the developer of the check to fill in the " \
                "\"HowToFix\" field."

            color = Colors.Default
            if data['CheckStatus'] == "PASS":
                color = Colors.Green
            elif data['CheckStatus'] == "ERROR":
                color = Colors.Red
                print_solution_description = True
            elif data['CheckStatus'] == "FAIL":
                color = Colors.Red
                print_solution_description = True
            elif data['CheckStatus'] == "WARNING":
                color = Colors.Yellow
            elif data['CheckStatus'] == "INFO":
                color = Colors.Blue

            if isinstance(data['CheckResult'], dict):
                command_exist = True if 'Command' in data and data['Command'] != "" else False
                message_exist = True if 'Message' in data and data['Message'] != "" else False
                logs_exist = True if 'Logs' in data and data['Logs'] != "" else False
                how_to_fix_exist = True if 'HowToFix' in data and data['HowToFix'] != "" else False
                automation_fix_exist = True if 'AutomationFix' in data and data['AutomationFix'] != "" \
                    else False

                line_out = current_out if (not message_exist and not command_exist and
                                           not print_solution_description) else False
                command_out = current_out if not message_exist and not print_solution_description else False
                message_out = current_out if not print_solution_description else False
                how_to_fix_out = current_out if not automation_fix_exist else False
                automation_fix_out = current_out

                self.print_line(key, "", "", color, depth, out+[line_out])
                if command_exist:
                    self.print_command(data['Command'], depth, out+[command_out])
                if message_exist:
                    self.print_message(data['Message'], color, depth, out+[message_out])
                if logs_exist:
                    self.print_logs(data['Logs'], color, depth, out)
                if print_solution_description:
                    how_to_fix_message = data["HowToFix"] if how_to_fix_exist else how_to_fix_default_message
                    self.print_how_to_fix(how_to_fix_message, color, depth, out+[how_to_fix_out])
                    if automation_fix_exist:
                        self.print_automation_fix(
                            data['AutomationFix'], color, depth, out+[automation_fix_out])

                if examine_summary is not None:
                    if isinstance(examine_summary[key]['CheckResult'], dict):
                        self.print_summary_tree(
                            data['CheckResult'],
                            depth=depth+1,
                            out=out+[current_out],
                            examine_summary=examine_summary[key]['CheckResult']
                        )
                    else:
                        self.print_message(
                            f"The value is not a dictionary. The value is '{examine_summary[key]['CheckResult']}'.",  # noqa: E501
                            Colors.Red, depth, out=out+[False])
                        self.print_summary_tree(data['CheckResult'], depth=depth+1, out=out+[current_out])
                else:
                    self.print_summary_tree(data['CheckResult'], depth=depth+1, out=out+[current_out])
            else:
                command_exist = True if 'Command' in data and data['Command'] != "" else False
                message_exist = True if 'Message' in data and data['Message'] != "" else False
                logs_exist = True if 'Logs' in data and data['Logs'] != "" else False
                how_to_fix_exist = True if 'HowToFix' in data and data['HowToFix'] != "" else False
                automation_fix_exist = True if 'AutomationFix' in data and data['AutomationFix'] != "" \
                    else False

                line_out = current_out if (not message_exist and not command_exist and
                                           not print_solution_description) else False
                command_out = current_out if not message_exist and not print_solution_description else False
                message_out = current_out if not print_solution_description else False
                how_to_fix_out = current_out if not automation_fix_exist else False
                automation_fix_out = current_out

                self.print_line(key, str(data['CheckResult']), data['CheckStatus'], color, depth, out+[line_out])   # noqa: E501
                if command_exist:
                    self.print_command(data['Command'], depth, out+[command_out])
                if message_exist:
                    self.print_message(data['Message'], color, depth, out+[message_out])
                if logs_exist:
                    self.print_logs(data['Logs'], color, depth, out)
                if print_solution_description:
                    how_to_fix_message = data["HowToFix"] if how_to_fix_exist else how_to_fix_default_message
                    self.print_how_to_fix(how_to_fix_message, color, depth, out+[how_to_fix_out])
                    if automation_fix_exist:
                        self.print_automation_fix(
                            data['AutomationFix'], color, depth, out+[automation_fix_out])

                if examine_summary is not None and examine_summary[key]['CheckResult'] != data['CheckResult']:  # noqa: E501
                    self.print_message(
                        f"The values of the current and compared runs are not equal. "
                        f"The value is '{examine_summary[key]['CheckResult']}'!!!!!!!!!!!!!!!!!!!!!!!",
                        Colors.Red, depth, out+[current_out])


def _verbosity_processing(summary: Dict, required_verbosity: int, parent_verbosity: Optional[int] = None):
    del_keys = []
    for key, data in summary.items():
        result_verbosity = 0 if 'Verbosity' not in data or data['Verbosity'] == '' \
            else data['Verbosity']
        if required_verbosity < 3:
            if "Command" in data:
                del data["Command"]
        if parent_verbosity is not None and result_verbosity < parent_verbosity:
            result_verbosity = parent_verbosity
            logging.warning(
                "The verbosity level of the subtree is less than the verbosity level of the higher node.")
        if isinstance(data['CheckResult'], dict) and result_verbosity <= required_verbosity:
            _verbosity_processing(data['CheckResult'], required_verbosity, parent_verbosity=result_verbosity)
        if result_verbosity > required_verbosity:
            del_keys.append(key)
    for key in del_keys:
        del summary[key]


def print_full_summary(
        checks: List[BaseCheck], required_verbosity: int,
        output_file: Optional[Path], examine_data: Optional[Dict] = None) -> None:
    for check in checks:
        metadata = check.get_metadata()
        summary = check.get_summary()
        if summary is None:
            continue
        print_ex("", output_file)
        print_ex("=" * max(CONSOLE_MIN, shutil.get_terminal_size().columns), output_file)
        print_ex(f"Check name: {metadata.name}", output_file)
        print_ex(f"Description: {metadata.descr}", output_file)
        print_ex("=" * max(CONSOLE_MIN, shutil.get_terminal_size().columns), output_file)
        print_ex("", output_file)

        try:
            summary_result = json.loads(summary.result)
            examine_summary = examine_data[metadata.name]['CheckResult'] if examine_data is not None \
                else None
            if len(summary_result) == 0:
                raise ValueError
            _verbosity_processing(summary_result['CheckResult'], required_verbosity)
            check_printer = CheckSummaryPrinter(summary_result, output_file)
            check_printer.print_summary_tree(summary_result['CheckResult'], examine_summary=examine_summary)

        except (ValueError, KeyError, TypeError):  # includes simplejson.decoder.JSONDecodeError
            print_ex("Incorrect or empty JSON format.", output_file, color=Colors.Red)
            continue


def _get_status_message(summary: Dict, result_status: str) -> List[str]:
    result_massages = []
    for _, data in summary.items():
        if data["CheckStatus"] == result_status and 'Message' in data and data['Message'] != "":
            result_massages.append(data['Message'])
        if isinstance(data['CheckResult'], dict):
            result_massages.extend(_get_status_message(data['CheckResult'], result_status))
    return result_massages


def print_short_summary(
        checks: List[BaseCheck], output_file: Optional[Path]) -> None:
    checks_run = len(checks)
    checks_pass = 0
    checks_fail = 0
    checks_error = 0
    checks_warning = 0
    for check in checks:
        metadata = check.get_metadata()
        summary = check.get_summary()

        if summary is None:
            checks_run -= 1
            continue

        result_status = ""
        result_color = ""

        if summary.error_code == 0:
            checks_pass += 1
            result_status = "PASS"
            result_color = Colors.Green
        elif summary.error_code == 1:
            checks_warning += 1
            result_status = "WARNING"
            result_color = Colors.Yellow
        elif summary.error_code == 2:
            checks_fail += 1
            result_status = "FAIL"
            result_color = Colors.Red
        elif summary.error_code == 3:
            checks_error += 1
            result_status = "ERROR"
            result_color = Colors.Red

        print_ex("=" * max(CONSOLE_MIN, shutil.get_terminal_size().columns), output_file)
        print_ex(f"Check name: {metadata.name}", output_file)
        print_ex(f"Description: {metadata.descr}", output_file)
        print_ex("Result status: ", output_file, end="")
        print_ex(f"{result_status}", output_file, color=result_color)

        try:
            summary_result = json.loads(summary.result)
            result_messages = _get_status_message(summary_result["CheckResult"], result_status)
            if len(result_messages) != 0:
                for message in result_messages:
                    print_ex(message, output_file, color=result_color)
        except (ValueError, KeyError, TypeError):  # includes simplejson.decoder.JSONDecodeError
            pass
        print_ex("=" * max(CONSOLE_MIN, shutil.get_terminal_size().columns), output_file)
        print_ex("", output_file)

    plural_suffix = "" if checks_run == 1 else "S"
    plural_suffix_err = "" if checks_error == 1 else "S"
    plural_suffix_war = "" if checks_warning == 1 else "S"

    print_ex(f"{checks_run} CHECK{plural_suffix}", output_file, end=": ")
    print_ex(f"{checks_pass}", output_file, end=" ")
    print_ex("PASS", output_file, color=Colors.Green, end=", ")
    print_ex(f"{checks_fail}", output_file, end=" ")
    print_ex("FAIL", output_file, color=Colors.Red, end=", ")
    print_ex(f"{checks_warning}", output_file, end=" ")
    print_ex(f"WARNING{plural_suffix_war}", output_file, color=Colors.Yellow, end=", ")
    print_ex(f"{checks_error}", output_file, end=" ")
    print_ex(f"ERROR{plural_suffix_err}", output_file, color=Colors.Red)


def print_summary(
        checks: List[BaseCheck], required_verbosity: int,
        output_file: Optional[Path], examine_data: Optional[Dict] = None) -> None:
    print_ex("", output_file)
    print_ex("Checks results:", output_file, color=Colors.Yellow)
    print_ex("", output_file)
    checks_by_importance = sorted(checks, key=lambda check: check.get_metadata().merit, reverse=True)
    if required_verbosity == -1:
        print_short_summary(checks_by_importance, output_file)
    else:
        print_full_summary(checks_by_importance, required_verbosity, output_file, examine_data)
