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

import json
import subprocess
import os
import logging

from pathlib import Path
from typing import List, Dict

from modules.check.check import BaseCheck, CheckSummary, CheckMetadataPy
from modules.log import trace  # type: ignore


PATH_TO_ONEAPI_USER = Path.home() / "intel" / "oneapi"
PATH_TO_ONEAPI_OPT = Path("/opt/intel/oneapi")


class SysCheck(BaseCheck):
    def __init__(self, sys_check_path: Path):
        product_name = str(sys_check_path).split("/")[-4]
        self.metadata = CheckMetadataPy(
            name=f"{product_name}_sys_check",
            type="",
            tags="syscheck",
            descr=f"System check for {product_name} found in {sys_check_path}",
            dataReq="{}",
            rights="user",
            timeout=10,
            version="",
            run=str(sys_check_path))

    def get_api_version(self) -> str:
        return "0.1"

    @trace(log_args=True)
    def run(self, data: Dict) -> CheckSummary:
        if bool(data):
            raise NotImplementedError("Pass data to sys check module does not implemented")
        if os.getuid() == 0:
            result_json = {
                "Value": {
                    self.metadata.name: {
                        "RetVal": "ERROR",
                        "Value": "Undefined",
                        "Message": "Sys_checks cannot be run with root privileges"
                    }
                }
            }
            result_json_str = json.dumps(result_json)
            return CheckSummary(
                result=result_json_str
            )
        process = subprocess.Popen(
            "source " + self.metadata.run, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            encoding="utf-8", executable="/bin/bash", shell=True)
        stdout, stderr = process.communicate()
        retval = 'PASS' if process.returncode == 0 else 'FAIL'
        result_json = {
            "Value": {
                self.metadata.name: {
                    "RetVal": retval,
                    "Value": {
                        "Stdout": {
                            "Value": stdout.strip(),
                            "RetVal": retval
                        },
                        "Stderr": {
                            "Value": stderr.strip(),
                            "RetVal": retval
                        }
                    }
                }
            }
        }
        result_json_str = json.dumps(result_json)
        return CheckSummary(
            result=result_json_str
        )


@trace(log_args=True)
def getSysChecks(sys_check_path: Path) -> List[BaseCheck]:
    if not sys_check_path.is_file():
        logging.error(f"Failed to load {sys_check_path}: No such file")
        raise OSError(f"Failed to load {sys_check_path}: No such file")
    return [SysCheck(sys_check_path)]


def search_sys_checks() -> List[Path]:
    sys_checks_opt = PATH_TO_ONEAPI_OPT.rglob("latest/sys_check/sys_check.sh")
    sys_checks_user = PATH_TO_ONEAPI_USER.rglob("latest/sys_check/sys_check.sh")
    return [*sys_checks_opt, *sys_checks_user]
