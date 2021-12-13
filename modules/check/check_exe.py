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
import subprocess
import json

from pathlib import Path
from typing import List, Dict

from modules.check.check import BaseCheck, CheckSummary, CheckMetadataPy

from modules.log import trace  # type: ignore


class CheckExe(BaseCheck):

    def __init__(self, path: Path):
        self.path = str(path)
        metadata_dict = json.loads(self._run_check('--get_metadata'))
        self.metadata = CheckMetadataPy(
            name=metadata_dict['name'],
            type=metadata_dict['type'],
            tags=metadata_dict['tags'],
            descr=metadata_dict['descr'],
            dataReq=metadata_dict['dataReq'],
            rights=metadata_dict['rights'],
            timeout=metadata_dict['timeout'],
            version=metadata_dict['version'],
            run=metadata_dict['run']
        )

    def get_api_version(self) -> str:
        return self._run_check('--get_api_version')

    @trace(log_args=True)
    def run(self, data: Dict) -> CheckSummary:
        if bool(data):
            raise NotImplementedError("Pass data to exe module does not implemented")
        summary_dict = json.loads(self._run_check('--get_summary'))
        return CheckSummary(
            result=summary_dict['result']
        )

    def _run_check(self, param) -> str:
        process = subprocess.Popen(
            [self.path, param], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        stdout, _ = process.communicate()
        if process.returncode != 0:
            raise Exception(f"Cannot run {self.path} with {param}")
        return stdout.strip()


@trace(log_args=True)
def getChecksExe(checker_path: Path) -> List[BaseCheck]:
    if not checker_path.exists():
        logging.error(f"Failed to load {str(checker_path)}: No such file")
        raise OSError(f"Failed to load {str(checker_path)}: No such file")
    return [CheckExe(checker_path)]
