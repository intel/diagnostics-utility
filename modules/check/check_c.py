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

import logging

from pathlib import Path
from typing import List, Dict

from modules.check.check_list import Check, CheckList
from modules.check.check import BaseCheck, CheckSummary, CheckMetadataPy

from modules.log import trace  # type: ignore
import json


class CheckC(BaseCheck):

    def __init__(self, check: Check, check_list: CheckList):
        self.check = check
        self.check_list = check_list
        self.metadata = CheckMetadataPy(
            name=check.check_metadata.name.decode("utf-8"),
            type=check.check_metadata.type.decode("utf-8"),
            tags=check.check_metadata.tags.decode("utf-8"),
            descr=check.check_metadata.descr.decode("utf-8"),
            dataReq=check.check_metadata.dataReq.decode("utf-8"),
            rights=check.check_metadata.rights.decode("utf-8"),
            timeout=check.check_metadata.timeout,
            version=check.check_metadata.version.decode("utf-8"),
            run="run"
        )
        self.api_version = check_list.api_version

    def get_api_version(self) -> str:
        return self.api_version

    @trace(log_args=True)
    def run(self, data: Dict) -> CheckSummary:
        run_result = self.check.run(json.dumps(data).encode('utf-8'))
        return CheckSummary(
            result=run_result.result.decode("utf-8")
        )

    def __str__(self) -> str:
        return f"{type(self).__name__}('check_list'='{self.check_list}', 'metadata'='{self.metadata}')"


@trace(log_args=True)
def getChecksC(lib_checker_path: Path) -> List[BaseCheck]:
    if not lib_checker_path.exists():
        logging.error(f"Failed to load {str(lib_checker_path)}: No such file")
        raise OSError(f"Failed to load {str(lib_checker_path)}: No such file")
    chList = []
    check_list = CheckList(str(lib_checker_path))
    for check in check_list:
        chList.append(CheckC(check, check_list))
    return chList
