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
import logging

from pathlib import Path
from typing import List, Dict

from modules.check.check_list_py import CheckListPy
from modules.check.check import CheckMetadataPy, BaseCheck, CheckSummary

from modules.log import trace  # type: ignore


class CheckPy(BaseCheck):

    def __init__(self, metadata: CheckMetadataPy, check_list: CheckListPy):
        self.check_list = check_list
        self.metadata = metadata

    def get_api_version(self) -> str:
        return self.check_list.api_version

    @trace(log_args=True)
    def run(self, data: Dict) -> CheckSummary:
        func = getattr(self.check_list.checker_module, self.metadata.run)
        return func(data)

    def __str__(self) -> str:
        return f"{type(self).__name__}('check_list'='{self.check_list}', 'metadata'='{self.metadata}')"


@trace(log_args=True)
def getChecksPy(checker_path: Path, version: str) -> List[BaseCheck]:
    if not checker_path.exists():
        logging.error(f"Failed to load {str(checker_path)}: No such file.")
        raise OSError(f"Failed to load {str(checker_path)}: No such file.")
    sys.path.append(str(checker_path.parent))
    check_list = CheckListPy(checker_path)
    if check_list.api_version != version:
        logging.error(f"Failed to load {str(checker_path)}:{str(checker_path)} is incompatible.")
        raise ValueError(f"Failed to load {str(checker_path)}:{str(checker_path)} is incompatible.")
    return [CheckPy(check, check_list) for check in check_list]
