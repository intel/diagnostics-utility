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


def gcc_check(json_node: Dict):
    check_result = {"CheckResult": {}, "CheckStatus": "INFO"}
    get_gcc_version(check_result["CheckResult"])
    get_gcc_location(check_result["CheckResult"])
    get_libgcc_location(check_result["CheckResult"])

    json_node.update({"GCC compiler": check_result})


def get_gcc_version(json_node: Dict) -> None:
    check_result = {"CheckResult": "Undefined", "CheckStatus": "INFO", "Command": "gcc --version"}
    try:
        command = ["gcc", "--version"]
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        stdout, _ = process.communicate()
        if process.returncode != 0:
            raise Exception("Cannot get information about GCC compiler version.")
        gcc_version = stdout.splitlines()[0].strip().split(" ")[-1]
        check_result["CheckResult"] = gcc_version
    except Exception as error:
        check_result["CheckStatus"] = "ERROR"
        check_result["Message"] = str(error)
        check_result["HowToFix"] = "This error is unexpected. Please report the issue to " \
            "Diagnostics Utility for Intel® oneAPI Toolkits repository: " \
            "https://github.com/intel/diagnostics-utility."

    json_node.update({"GCC compiler version": check_result})


def get_gcc_location(json_node: Dict) -> None:
    check_result = {"CheckResult": "Undefined", "CheckStatus": "INFO", "Command": "which gcc"}
    try:
        command = ["which", "gcc"]
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        stdout, _ = process.communicate()
        if process.returncode != 0:
            raise Exception("Cannot get information about GCC compiler location")
        gcc_location = stdout.strip()
        check_result["CheckResult"] = gcc_location
    except Exception as error:
        check_result["CheckStatus"] = "ERROR"
        check_result["Message"] = str(error)
        check_result["HowToFix"] = "This error is unexpected. Please report the issue to " \
            "Diagnostics Utility for Intel® oneAPI Toolkits repository: " \
            "https://github.com/intel/diagnostics-utility."
    json_node.update({"GCC compiler location": check_result})


def get_libgcc_location(json_node: Dict) -> None:
    check_result = {"CheckResult": "Undefined", "CheckStatus": "INFO", "Command": "gcc -print-libgcc-file-name"}  # noqa: E501
    try:
        command = ["gcc", "-print-libgcc-file-name"]
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        stdout, _ = process.communicate()
        if process.returncode != 0:
            raise Exception("Cannot get information about the GCC companion library location")
        gcc_location = stdout.strip()
        check_result["CheckResult"] = gcc_location
    except Exception as error:
        check_result["CheckStatus"] = "ERROR"
        check_result["Message"] = str(error)
        check_result["HowToFix"] = "This error is unexpected. Please report the issue to " \
            "Diagnostics Utility for Intel® oneAPI Toolkits repository: " \
            "https://github.com/intel/diagnostics-utility."
    json_node.update({"GCC companion library location": check_result})


def run_gcc_check(data: dict) -> CheckSummary:
    result_json = {"CheckResult": {}}

    gcc_check(result_json["CheckResult"])

    check_summary = CheckSummary(
        result=json.dumps(result_json, indent=4)
    )

    return check_summary


def get_api_version() -> str:
    return "0.2"


def get_check_list() -> List[CheckMetadataPy]:
    someCheck = CheckMetadataPy(
        name="compiler_check",
        type="Data",
        groups="default,sysinfo,compile,host",
        descr="This check shows information about the GCC compiler.",
        dataReq="{}",
        merit=0,
        timeout=5,
        version=2,
        run="run_gcc_check"
    )
    return [someCheck]
