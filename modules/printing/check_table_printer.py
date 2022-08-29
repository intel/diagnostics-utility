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

from pathlib import Path
from typing import Optional

from modules.printing.table_printer import draw_line, draw_info_row
from modules.printing.printer_helper import Aligment, Colors


def print_metadata(checks, output_file: Optional[Path]) -> None:
    TOTAL_NUM = 3

    CONSOLE_MIN = 60
    CONSOLE_WIDTH = max(CONSOLE_MIN, shutil.get_terminal_size().columns)

    WIDTH_NAME_COL = max([len(check.get_metadata().name) for check in checks]) + 2 \
        if CONSOLE_WIDTH > CONSOLE_MIN \
        else min(20, max([len(check.get_metadata().name) for check in checks]) + 2)
    WIDTH_TAGS_COL = max([len(tag) for check in checks for tag in check.get_metadata().tags.split(",")]) + 2
    WIDTH_DESCR_COL = int(
        (CONSOLE_WIDTH - WIDTH_NAME_COL - WIDTH_TAGS_COL - (TOTAL_NUM + 1)))

    table_column_names = ["Check name", "Tags", "Description"]
    lengths = []
    lengths.append(WIDTH_NAME_COL)
    lengths.append(WIDTH_TAGS_COL)
    lengths.append(WIDTH_DESCR_COL)

    # Draw title
    draw_line(lengths, output_file)
    draw_info_row(
        lengths, table_column_names, output_file,
        column_colors=[Colors.Yellow]*TOTAL_NUM,
        column_aligment=[Aligment.c]*TOTAL_NUM)

    # Draw content
    TOTAL_NUM = len(lengths)
    clr = [Colors.Default] * (TOTAL_NUM)
    alig = [Aligment.l] * (TOTAL_NUM)

    checks_by_importance = sorted(checks, key=lambda check: check.get_metadata().merit, reverse=True)
    for check in checks_by_importance:
        metadata = check.get_metadata()
        cols = [metadata.name, metadata.tags.replace(",", " "), metadata.descr]
        draw_info_row(
            lengths, cols, output_file, column_colors=clr, column_aligment=alig, separator_line=False)
    draw_line(lengths, output_file)
