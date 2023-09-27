# /*******************************************************************************
# Copyright Intel Corporation.
# This software and the related documents are Intel copyrighted materials, and your use of them
# is governed by the express license under which they were provided to you (License).
# Unless the License provides otherwise, you may not use, modify, copy, publish, distribute, disclose
# or transmit this software or the related documents without Intel"s prior written permission.
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


def _run_check(path: Path, param: str) -> str:
    process = subprocess.Popen(
        [path, param], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    stdout, _ = process.communicate()
    if process.returncode != 0:
        raise Exception(f"Cannot run {path} with {param}")
    return stdout.strip()


class CheckExe(BaseCheck):

    def __init__(self, path: Path):
        self.path = path
        metadata_dict = json.loads(_run_check(self.path, "--get_metadata"))
        self.metadata = CheckMetadataPy(
            name=metadata_dict["name"],
            type=metadata_dict["type"],
            groups=metadata_dict["groups"],
            descr=metadata_dict["descr"],
            dataReq=metadata_dict["dataReq"],
            merit=metadata_dict["merit"],
            timeout=metadata_dict["timeout"],
            version=metadata_dict["version"],
            run=metadata_dict["run"]
        )

    def get_api_version(self) -> str:
        return _run_check(self.path, "--get_api_version")

    @trace(log_args=True)
    def run(self, data: Dict) -> CheckSummary:
        if bool(data):
            raise NotImplementedError("Unable to pass data to the exe module. Implement the exe module.")
        get_summary = _run_check(self.path, "--get_summary").replace("\n", "")
        summary_dict = json.loads(get_summary)
        return CheckSummary(
            result=json.dumps(summary_dict["result"])
        )


@trace(log_args=True)
def getChecksExe(checker_path: Path, version: str) -> List[BaseCheck]:
    if not checker_path.exists():
        logging.error(f"Failed to load {str(checker_path)}: File not found.")
        raise OSError(f"Failed to load {str(checker_path)}: File not found.")
    if _run_check(checker_path, "--get_api_version") != version:
        logging.error(f"Failed to load {str(checker_path)}:{str(checker_path)} is incompatible.")
        raise ValueError(f"Failed to load {str(checker_path)}:{str(checker_path)} is incompatible.")
    return [CheckExe(checker_path)]
