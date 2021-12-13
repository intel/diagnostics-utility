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
import platform
from typing import Dict, List

from checkers_py.common import debugger_helper as common_debugger
from modules.check import CheckSummary, CheckMetadataPy


def check_linux_kernel_version(json_node: Dict) -> None:
    value_pass = {"Value": "Supported", "RetVal": "PASS", "Command": "uname -r"}
    value_fail = {"Value": "Not supported", "RetVal": "FAIL", "Command": "uname -r",
                  "Message": "This Linux kernel version is not supported."}
    linux_kernel_version = platform.uname().release.split(".")

    if len(linux_kernel_version) < 2:
        json_node.update({"Linux kernel version": value_fail})
        return

    try:
        linux_kernel_version[0] = int(linux_kernel_version[0])
        linux_kernel_version[1] = int(linux_kernel_version[1])
    except ValueError:
        json_node.update({"Linux kernel version": value_fail})
        return

    if linux_kernel_version[0] < 4 or (linux_kernel_version[0] == 4 and linux_kernel_version[1] < 14):
        json_node.update({"Linux kernel version": value_fail})
        return

    json_node.update({"Linux kernel version": value_pass})


def run_debugger_check(data: dict) -> CheckSummary:
    result_json = {"Value": {}}
    if common_debugger.get_OS() == "Linux":
        check_linux_kernel_version(result_json["Value"])
        common_debugger.check_gdb_exist(result_json["Value"])
        common_debugger.check_libipt_exist(result_json["Value"])
        common_debugger.check_libiga_exist(result_json["Value"])
    else:
        result_json["Value"] = {
            "Error message": {
                "Value": "",
                "RetVal": "ERROR",
                "Message": "This check works on linux only."
            }
        }

    check_summary = CheckSummary(
        result=json.dumps(result_json, indent=4)
    )
    return check_summary


def get_api_version() -> str:
    return "0.1"


def get_check_list() -> List[CheckMetadataPy]:
    someCheck = CheckMetadataPy(
        name="debugger_check",
        type="Data",
        tags="debugger,gdb",
        descr="This check verifies if the environment is ready to use gdb (Intel(R) Distribution for GDB*.",
        dataReq="{}",
        rights="user",
        timeout=10,
        version="0.1",
        run="run_debugger_check"
    )
    return [someCheck]
