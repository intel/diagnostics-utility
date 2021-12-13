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
from types import ModuleType
from typing import List, Dict

from modules.check.check import CheckMetadataPy, BaseCheck, CheckSummary

from modules.log import trace  # type: ignore


class CheckPy(BaseCheck):

    def __init__(self, metadata: CheckMetadataPy, module: ModuleType):
        self.__module = module
        self.metadata = metadata

    def get_api_version(self) -> str:
        func = getattr(self.__module, "get_api_version")
        return func()

    @trace(log_args=True)
    def run(self, data: Dict) -> CheckSummary:
        func = getattr(self.__module, self.metadata.run)
        return func(data)

    def __str__(self) -> str:
        return f"{type(self).__name__}('module'='{self.__module.__file__}', 'metadata'='{self.metadata}')"


@trace(log_args=True)
def getChecksPy(lib_checker_path: Path) -> List[BaseCheck]:
    if not lib_checker_path.exists():
        logging.error(f"Failed to load {str(lib_checker_path)}: No such file")
        raise OSError(f"Failed to load {str(lib_checker_path)}: No such file")
    sys.path.append(str(lib_checker_path.parent))
    module = __import__(lib_checker_path.stem)
    check_list = module.get_check_list()
    return [CheckPy(check, module) for check in check_list]
