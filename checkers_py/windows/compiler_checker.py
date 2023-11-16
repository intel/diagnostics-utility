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

from checkers_py.windows.common.termninal_helper import run_powershell_command
from modules.check import CheckSummary, CheckMetadataPy
import json
import re
from typing import List


def get_api_version() -> str:
    return "0.2"


def get_check_list() -> List[CheckMetadataPy]:
    someCheck = CheckMetadataPy(
        name="compiler_check",
        type="Data",
        groups="default,sysinfo,compile,runtime,host,target",
        descr="This check shows information about the compiler.",
        dataReq="{}",
        merit=0,
        timeout=5,
        version=2,
        run="run_compiler_check"
    )
    return [someCheck]


def run_compiler_check(data: dict) -> CheckSummary:
    result_json = {"CheckResult": {}}
    result_json["CheckResult"].update(get_msvc_compiler_info())

    check_summary = CheckSummary(
        result=json.dumps(result_json, indent=4)
    )

    return check_summary


def get_msvc_compiler_info():
    check_result = {"CheckResult": {}, "CheckStatus": "INFO"}
    check_result["CheckResult"].update(get_msvc_compiler_version())

    return {"MSVC compiler": check_result}


def get_msvc_compiler_version() -> None:
    check_result = {"CheckResult": "Undefined", "CheckStatus": "INFO", "Command": "cl"}
    try:
        _, stderr, return_code = run_powershell_command("cl")
        if (not return_code == 0):
            check_result["CheckStatus"] = "FAIL"
            check_result["Message"] = "MSVC compiler not found."
            check_result["HowToFix"] = "Make sure the compiler is installed" \
                " and present in the PATH environment variable"
        else:
            search_version = re.search(r'(\d*\.\d*\.\d*(\.\d*)?)', stderr)
            if (search_version is None):
                check_result["CheckStatus"] = "FAIL"
                check_result["Message"] = "Failed to get compiler version."
            else:
                cl_version = search_version.group(0)
                check_result["CheckResult"] = cl_version
    except Exception as error:
        check_result["CheckStatus"] = "ERROR"
        check_result["Message"] = str(error)
        check_result["HowToFix"] = "This error is unexpected. Please report the issue to " \
            "Diagnostics Utility for Intel® oneAPI Toolkits repository: " \
            "https://github.com/intel/diagnostics-utility."

    return {"Version": check_result}
