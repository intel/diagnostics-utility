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

import os
import grp
import json
import getpass
from pathlib import Path
from typing import Dict, List, FrozenSet

from modules.check import CheckSummary, CheckMetadataPy
from checkers_py.linux.common.gpu_helper import are_intel_gpus_found
from checkers_py.linux.common.gpu_helper import get_card_devices, get_render_devices


def _get_required_groups(files: List[Path]) -> FrozenSet[str]:
    return set([file.group() for file in files])


def _get_user_groups(username: str) -> List[str]:
    return [group.gr_name for group in grp.getgrall() if username in group.gr_mem]


def check_user_in_required_groups(json_node: Dict) -> None:
    username = getpass.getuser()

    card_devices = get_card_devices()
    render_devices = get_render_devices()

    if len(card_devices) == 0 and len(render_devices) == 0:
        json_node.update({
            "user_group_check": {
                "CheckResult": "",
                "CheckStatus": "ERROR",
                "Message": "Direct Rendering Infrastructure (DRI) cannot find graphics hardware.",
                "HowToFix": "For Intel GPU(s) install and load the i915 driver."
            }
        })
        return

    required_groups = _get_required_groups([*card_devices, *render_devices])
    user_groups = _get_user_groups(username)

    user_is_in_sudo = "sudo" in user_groups
    for required_group in required_groups:
        check_result = {"CheckResult": "", "CheckStatus": "PASS",
                        "Command": f"groups | grep {required_group}"}
        user_is_not_in_required_group = required_group not in user_groups
        if user_is_not_in_required_group:
            check_result["CheckStatus"] = "FAIL"
            if user_is_in_sudo:
                check_result["Message"] = f"Current user is not part of the {required_group} group."
                check_result["HowToFix"] = f"Add current user to the {required_group} group. " \
                    f"Then restart the terminal and try again."
                check_result["AutomationFix"] = f"sudo usermod -a -G {required_group} {username}"
            else:
                check_result["Message"] = f"Current user is not part of the {required_group} group."
                check_result["HowToFix"] = f"Contact the system administrator to add current user " \
                    f"to the {required_group} group."
        json_node.update({f"Current user is in the {required_group} group": check_result})


def run_user_group_check(data: dict) -> CheckSummary:
    result_json = {"CheckResult": {}}

    current_user_is_root = os.getuid() == 0
    if current_user_is_root:
        result_json["CheckResult"].update({
            "user_group_check": {
                "CheckResult": "",
                "CheckStatus": "PASS",
                "Message": "Root user does not need to be in groups to have access to devices. "
                           "The root user always has access to devices."
            }
        })
    else:
        if not are_intel_gpus_found(data):
            result_json["CheckResult"].update({
                "user_group_check": {
                    "CheckResult": "",
                    "CheckStatus": "ERROR",
                    "Message": "Check cannot verify that user is in the same group as the GPU(s) "
                               "because there are no Intel GPU(s) on the system.",
                    "HowToFix": "Ignore this error if you do not have Intel GPU(s) on the system."
                }
            })
        else:
            check_user_in_required_groups(result_json["CheckResult"])

    check_summary = CheckSummary(
        result=json.dumps(result_json, indent=4)
    )
    return check_summary


def get_api_version() -> str:
    return "0.2"


def get_check_list() -> List[CheckMetadataPy]:
    someCheck = CheckMetadataPy(
        name="user_group_check",
        type="Data",
        groups="default,profiling,gpu,runtime,target",
        descr="This check verifies that the current user is in the same group as the GPU(s).",
        dataReq="{\"intel_gpu_detector_check\": 2}",
        merit=80,
        timeout=30,
        version=2,
        run="run_user_group_check"
    )
    return [someCheck]
