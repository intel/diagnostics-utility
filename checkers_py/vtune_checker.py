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
import subprocess
import os
from typing import Dict, List

from checkers_py.common import advisor_vtune_helper as common_advisor_vtune
from modules.check import CheckSummary, CheckMetadataPy


def check_metrics_discovery_API_lib(json_node: Dict) -> None:
    value = {"Value": "", "RetVal": "PASS", "Command": "ls -l /usr/lib/x86_64-linux-gnu | grep libmd"}
    try:
        ls_process = subprocess.Popen(
            ["ls", "-l", "/usr/lib/x86_64-linux-gnu"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        grep_process = subprocess.Popen(
            ["grep", "libmd"],
            stdin=ls_process.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        ls_process.stdout.close()

        if ls_process.wait() != 0:
            raise Exception("Cannot get information about x86_64-bit libraries.")

        stdout, _ = grep_process.communicate()
        if grep_process.returncode in [0, 1]:
            if not stdout.splitlines():
                value["RetVal"] = "FAIL"
                value["Message"] = "Install Metrics Library for Metrics Discovery API."
        else:
            raise Exception("Error from grep function")
    except Exception as error:
        value["RetVal"] = "ERROR"
        value["Message"] = str(error)
    json_node.update({"Metrics Library for Metrics Discovery API is installed": value})


def check_debugFS_permissions(json_node: Dict) -> None:
    value = {"Value": "Configured", "RetVal": "PASS", "Command": "ls -l /sys/kernel/debug"}
    if not os.access('/sys/kernel/debug', os.W_OK & os.R_OK):
        value["Value"] = "Not configured"
        value["RetVal"] = "FAIL"
        value["Message"] = "Use the prepare_debugfs.sh script to set read/write permissions to debugFS."
    json_node.update({"debugFS permissions": value})


def check_kernel_config_options(json_node: Dict) -> None:
    value = {
        "Value": "Undefined",
        "RetVal": "PASS",
        "Command": f"grep CONFIG_DRM_I915_LOW_LEVEL_TRACEPOINTS /boot/config-{platform.uname().release}"
    }
    try:
        proc = subprocess.Popen(
            ["grep", "CONFIG_DRM_I915_LOW_LEVEL_TRACEPOINTS", f"/boot/config-{platform.uname().release}"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        stdout, _ = proc.communicate()
        if proc.returncode != 0:
            raise Exception("Cannot get information about kernel config option.")
        value["Value"] = "Enable"
        if stdout and ('is not set' in stdout.splitlines()[0] or stdout.splitlines()[0].split('=')[1] == 'n'):
            value["Value"] = "Disable or not set"
            value["RetVal"] = "FAIL"
            value["Message"] = "Rebuild the i915 driver or kernel."
    except Exception as error:
        value["RetVal"] = "ERROR"
        value["Message"] = str(error)
    json_node.update({"CONFIG_DRM_I915_LOW_LEVEL_TRACEPOINTS": value})


def run_vtune_check(data: dict) -> CheckSummary:
    result_json = {"Value": {}}

    if common_advisor_vtune.get_OS() == common_advisor_vtune.LINUX:
        check_metrics_discovery_API_lib(result_json["Value"])
        common_advisor_vtune.check_perf_stream_paranoid(result_json["Value"])
        check_debugFS_permissions(result_json["Value"])
        check_kernel_config_options(result_json["Value"])
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
        name="vtune_check",
        type="Data",
        tags="profiling,runtime,target",
        descr="This check verifies if the system is ready to do VTune analysis on GPU(s).",
        dataReq="{}",
        rights="user",
        timeout=10,
        version="0.1",
        run="run_vtune_check"
    )
    return [someCheck]
