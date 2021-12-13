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

from checkers_py.common import advisor_vtune_helper as common_advisor_vtune
from modules.check import CheckSummary, CheckMetadataPy


def check_linux_kernel_version(json_node: Dict) -> None:
    value = {"Value": "Supported", "RetVal": "PASS", "Command": "uname -r"}
    linux_kernel_version = platform.uname().release
    kernel, major, _ = linux_kernel_version.split('.')
    if int(kernel) < 4 or (int(kernel) == 4 and int(major) < 14):
        value["Value"] = "Not supported"
        value["RetVal"] = "FAIL"
        value["Message"] = "This Linux kernel version is not supported."
    json_node.update({"Linux kernel version": value})


def run_advisor_check(data: dict) -> CheckSummary:
    result_json = {"Value": {}}
    if common_advisor_vtune.get_OS() == common_advisor_vtune.LINUX:
        check_linux_kernel_version(result_json["Value"])
        common_advisor_vtune.check_perf_stream_paranoid(result_json["Value"])
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
        name="advisor_check",
        type="Data",
        tags="profiling,kernel,runtime,target",
        descr="This check verifies if the environment is ready to analyze GPU kernels.",
        dataReq="{}",
        rights="user",
        timeout=10,
        version="0.1",
        run="run_advisor_check"
    )
    return [someCheck]
