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

from typing import Optional
from pathlib import Path

from modules.printing.printer_helper import Colors


def print_ex_mock(
        message: str,
        file_path: Optional[Path],
        color: str = Colors.Default,
        end: str = "\n") -> None:
    is_colored = True if color != Colors.Default else False
    colored_message = f"{color}{message}{Colors.Default}" if is_colored else message
    print(colored_message, end=end)
