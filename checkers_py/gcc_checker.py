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


def get_gcc_version(json_node: Dict) -> None:
    value = {"Value": "Undefined", "RetVal": "INFO", "Command": "gcc --version"}
    try:
        command = ["gcc", "--version"]
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        stdout, _ = process.communicate()
        if process.returncode != 0:
            raise Exception("Cannot get information about GCC compiler version")
        gcc_version = stdout.splitlines()[0].strip().split(" ")[-1]
        value["Value"] = gcc_version
    except Exception as error:
        value["RetVal"] = "ERROR"
        value["Message"] = str(error)
    json_node.update({"GCC compiler version": value})


def run_gcc_check(data: dict) -> CheckSummary:
    result_json = {"Value": {}}

    get_gcc_version(result_json["Value"])

    check_summary = CheckSummary(
        result=json.dumps(result_json, indent=4)
    )

    return check_summary


def get_api_version() -> str:
    return "0.1"


def get_check_list() -> List[CheckMetadataPy]:
    someCheck = CheckMetadataPy(
        name="gcc_version_check",
        type="Data",
        tags="default,sysinfo,compile,host",
        descr="This check shows information about GCC compiler version.",
        dataReq="{}",
        rights="user",
        timeout=5,
        version="0.1",
        run="run_gcc_check"
    )
    return [someCheck]
