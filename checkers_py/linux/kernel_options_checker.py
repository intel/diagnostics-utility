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


def _check_perf_stream_paranoid(json_node: Dict) -> None:
    check_result = {"CheckResult": "Undefined", "CheckStatus": "INFO",
                    "Command": "sysctl -n dev.i915.perf_stream_paranoid"}
    try:
        proc = subprocess.Popen(
            ['sysctl', '-n', 'dev.i915.perf_stream_paranoid'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        stdout, _ = proc.communicate()
        if proc.returncode != 0:
            raise Exception("Cannot get information about operating sysctl option")
        check_result["CheckResult"] = stdout.splitlines()[0]
    except Exception as error:
        check_result["CheckStatus"] = "ERROR"
        check_result["Message"] = str(error)
        check_result["HowToFix"] = "This error is unexpected. Please report the issue to " \
            "Diagnostics Utility for Intel® oneAPI Toolkits repository: " \
            "https://github.com/intel/diagnostics-utility."
    json_node.update({"Perf stream paranoid": check_result})


def get_kernel_settings(json_node: Dict) -> None:
    kernel_settings = {}

    _check_perf_stream_paranoid(kernel_settings)

    check_result = {"CheckResult": kernel_settings, "CheckStatus": "INFO"}
    json_node.update({"Kernel settings": check_result})


def get_kernel_boot_options(json_node: Dict) -> None:
    check_result = {"CheckResult": "Undefined", "CheckStatus": "INFO", "Command": "cat /proc/cmdline"}
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
            options.update({key: {"CheckResult": val, "CheckStatus": "INFO"}})
        check_result["CheckResult"] = options
    except Exception as error:
        check_result["CheckStatus"] = "ERROR"
        check_result["Message"] = str(error)
        check_result["HowToFix"] = "This error is unexpected. Please report the issue to " \
            "Diagnostics Utility for Intel® oneAPI Toolkits repository: " \
            "https://github.com/intel/diagnostics-utility."
    json_node.update({"Kernel boot options": check_result})


def run_kernel_check(data: dict) -> CheckSummary:
    result_json = {"CheckResult": {}}

    get_kernel_settings(result_json["CheckResult"])
    get_kernel_boot_options(result_json["CheckResult"])

    check_summary = CheckSummary(
        result=json.dumps(result_json, indent=4)
    )

    return check_summary


def get_api_version() -> str:
    return "0.2"


def get_check_list() -> List[CheckMetadataPy]:
    someCheck = CheckMetadataPy(
        name="kernel_options_check",
        type="Data",
        groups="sysinfo,runtime,target",
        descr="This check shows kernel options.",
        dataReq="{}",
        merit=0,
        timeout=5,
        version=2,
        run="run_kernel_check"
    )
    return [someCheck]
