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

import textwrap

from pathlib import Path
from typing import List, Optional

from modules.printing.printer import print_ex
from modules.printing.printer_helper import Aligment, Colors


def draw_line(lengths: List[int], output_file: Optional[Path]) -> None:
    if (len(lengths) > 0):
        print_ex("+", output_file, end="")
        for length in lengths:
            print_ex(f"{'-' * length}+", output_file, end="")
        print_ex("", output_file)


def draw_info_row(
        lengths: List[int], columns: List[str], output_file: Optional[Path],
        column_colors: List[str] = [], column_aligment: List[str] = [], separator_line: bool = True) -> None:
    if (len(lengths) > 0 and len(lengths) == len(columns)):
        column_colors += [Colors.Default] * (len(lengths) - len(column_colors))
        column_aligment += [Aligment.l] * (len(lengths) - len(column_aligment))
        wrapped_text = [textwrap.wrap(col, width - 2) for col, width in zip(columns, lengths)]
        col_row_max = max([len(col) for col in wrapped_text])
        for i in range(0, col_row_max):
            print_ex("|", output_file, end="")
            for length, text, clr, alig in zip(lengths, wrapped_text, column_colors, column_aligment):
                text_out = text[i] if i < len(text) else ""
                width = length - 2
                print_ex(
                    f" {text_out:{alig}{width}} ", output_file, color=clr, end="")
                print_ex("|", output_file, end="")
            print_ex("", output_file)
        if separator_line:
            draw_line(lengths, output_file)
