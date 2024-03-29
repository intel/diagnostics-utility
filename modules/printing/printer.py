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

import sys

from pathlib import Path
from typing import Optional

from modules.printing.printer_helper import Colors
STDOUT_PRINTING = True


def enable_stdout_printing(status: bool) -> None:
    global STDOUT_PRINTING
    STDOUT_PRINTING = status


def print_ex(message: str, file_path: Optional[Path] = None, color: str = Colors.Default,
             end: str = "\n") -> None:

    is_colored = True if color != Colors.Default else False
    colored_message = f"{color}{message}{Colors.Default}" if is_colored else message
    if STDOUT_PRINTING:
        print(colored_message.encode("utf-8").decode(sys.stdout.encoding), end=end)
    if file_path is not None:
        file = open(file_path, "a", encoding="utf-8")
        file.write(message.encode("utf-8").decode(sys.stdout.encoding) + end)
        file.close()
