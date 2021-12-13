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

from modules.check import CheckSummary, CheckMetadataPy

import json
import subprocess
from typing import List, Dict


def get_kernel_boot_options(json_node: Dict) -> None:
    value = {"Value": "Undefined", "RetVal": "INFO", "Command": "cat /proc/cmdline"}
    try:
        command = ["cat", "/proc/cmdline"]
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        stdout, _ = process.communicate()
        if process.returncode != 0:
            raise Exception("Cannot get information about kernel boot options")
        options = {}
        for option in stdout.strip().split(" "):
            option_list = option.split("=", 1)
            key, val = option_list if len(option_list) == 2 else (option, "")
            options.update({key: {"Value": val, "RetVal": "INFO"}})
        value["Value"] = options
    except Exception as error:
        value["RetVal"] = "ERROR"
        value["Message"] = str(error)
    json_node.update({"Kernel boot options": value})


def run_kernel_boot_options_check(data: dict) -> CheckSummary:
    result_json = {"Value": {}}

    get_kernel_boot_options(result_json["Value"])

    check_summary = CheckSummary(
        result=json.dumps(result_json, indent=4)
    )

    return check_summary


def get_api_version() -> str:
    return "0.1"


def get_check_list() -> List[CheckMetadataPy]:
    someCheck = CheckMetadataPy(
        name="kernel_boot_options_check",
        type="Data",
        tags="sysinfo,runtime,target",
        descr="This check shows kernel boot options.",
        dataReq="{}",
        rights="user",
        timeout=5,
        version="0.1",
        run="run_kernel_boot_options_check"
    )
    return [someCheck]
