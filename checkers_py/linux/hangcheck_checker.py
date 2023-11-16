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
from checkers_py.linux.common.gpu_helper import are_intel_gpus_found, intel_gpus_not_found_handler

import os
import json
import itertools
import configparser
import subprocess

from typing import Dict, List

UBUNTU_GRUB_FILE_PATH = "/etc/default/grub"
UBUNTU_GRUB_CONFIG_KEY = "GRUB_CMDLINE_LINUX_DEFAULT"
UBUNTU_HANGCHECK_FILE_PATH = "/sys/module/i915/parameters/enable_hangcheck"
GRUB_HANGCHECK_VALUE = "i915.enable_hangcheck=0"


def _check_hangcheck_in_grub(check_result: Dict) -> None:
    config = configparser.ConfigParser()
    check_result["Command"] = f"grep {GRUB_HANGCHECK_VALUE} {UBUNTU_GRUB_FILE_PATH}"
    try:
        with open(UBUNTU_GRUB_FILE_PATH) as grub_config_file:
            config.read_file(
                itertools.chain(["[default]"], grub_config_file), source=UBUNTU_GRUB_FILE_PATH)

        if (config.has_option("default", UBUNTU_GRUB_CONFIG_KEY)):
            grub_kernel_config = config.get("default", UBUNTU_GRUB_CONFIG_KEY)
            if (GRUB_HANGCHECK_VALUE in grub_kernel_config):
                check_result["CheckStatus"] = "PASS"
                check_result["Message"] = "Kernel hangcheck is disabled. If it is not working, " \
                    "reboot or run 'sudo update-grub' for it to take effect."
    except PermissionError as error:
        check_result["CheckStatus"] = "ERROR"
        check_result["Message"] = str(error),
        check_result["HowToFix"] = "Try to run the Diagnostics Utility for Intel® oneAPI Toolkits " \
            "with administrative privileges."
    except Exception as error:
        check_result["CheckStatus"] = "ERROR"
        check_result["Message"] = str(error)
        check_result["HowToFix"] = "This error is unexpected. Please report the issue to " \
            "Diagnostics Utility for Intel® oneAPI Toolkits repository: " \
            "https://github.com/intel/diagnostics-utility."


def _check_hangcheck_in_config(check_result: Dict) -> None:
    check_result["Command"] = f"cat {UBUNTU_HANGCHECK_FILE_PATH}"
    try:
        with open(UBUNTU_HANGCHECK_FILE_PATH, "r") as hangcheck_file:
            hangcheck_contents = hangcheck_file.read()
        if (hangcheck_contents.strip() in {"N", "n", "0"}):
            check_result["CheckStatus"] = "PASS"
            check_result["Message"] = "To disable GPU hangcheck across reboots, visit " \
                "https://www.intel.com/content/www/us/en/develop/documentation/get-started-with-intel-oneapi-hpc-linux/top/before-you-begin.html."  # noqa: E501
    except PermissionError as error:
        check_result["CheckStatus"] = "ERROR"
        check_result["Message"] = str(error)
        check_result["HowToFix"] = "Try to run the Diagnostics Utility for Intel® oneAPI Toolkits " \
            "with administrative privileges."
    except Exception as error:
        check_result["CheckStatus"] = "ERROR"
        check_result["Message"] = str(error)
        check_result["HowToFix"] = "This error is unexpected. Please report the issue to " \
            "Diagnostics Utility for Intel® oneAPI Toolkits repository: " \
            "https://github.com/intel/diagnostics-utility."


def check_hangcheck_is_disabled(json_node: Dict) -> None:
    check_result = {
        "CheckResult": "",
        "CheckStatus": "FAIL",
        "Message": "To disable GPU hangcheck, visit "
                   "https://www.intel.com/content/www/us/en/docs/oneapi/installation-guide-hpc-cluster/2023-0/step-4-set-up-user-permissions-for-using-the.html#GPU-DISABLE-HANGCHECK."  # noqa: E501
    }

    if (os.path.isfile(UBUNTU_GRUB_FILE_PATH)):
        _check_hangcheck_in_grub(check_result)
    if (check_result["CheckStatus"] == "FAIL" and os.path.isfile(UBUNTU_HANGCHECK_FILE_PATH)):
        _check_hangcheck_in_config(check_result)

    if (check_result["CheckStatus"] == "FAIL"):
        check_result["HowToFix"] = "Try disable GPU hangcheck, based on instructions from " \
            "https://www.intel.com/content/www/us/en/docs/oneapi/installation-guide-hpc-cluster/2023-0/step-4-set-up-user-permissions-for-using-the.html#GPU-DISABLE-HANGCHECK."  # noqa E501

    json_node.update({"GPU hangcheck is disabled": check_result})


def check_non_zero_pre_emption_timeouts(json_node: Dict) -> None:
    check_result = {
        "CheckResult": "",
        "CheckStatus": "PASS",
        "Command": "find /sys/devices -regex .*/drm/card[0-9]*/engine/[rc]cs[0-9]*/preempt_timeout_ms "
                   "-exec cat {} +"
    }
    try:
        process = subprocess.Popen(
            ["find", "/sys/devices", "-regex", ".*/drm/card[0-9]*/engine/[rc]cs[0-9]*/preempt_timeout_ms",
             "-exec", "cat", "{}", "+"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")

        stdout, _ = process.communicate()
        if process.returncode != 0:
            raise Exception("Cannot get information about preempt_timeout_ms")

        ptimeout_info = {
            "preempt_timeout_ms=0 to prevent long-running jobs from hanging": {
                "CheckResult": "",
                "CheckStatus": "PASS"
            }}

        timeouts = stdout.splitlines()
        timeout = 0 if len(stdout.splitlines()) == 0 else max([int(timeout) for timeout in timeouts])
        if timeout != 0:
            error_dict = {
                "CheckResult": "",
                "CheckStatus": "FAIL",
                "Message":
                    f"preempt_timeout_ms={timeout} - long-running jobs may not run to completion.",
                "HowToFix": "To disable preemption timeout, visit "
                            "https://www.intel.com/content/www/us/en/develop/documentation/installation-guide-for-intel-oneapi-toolkits-hpc-cluster/top/step-4-set-up-user-permissions.html#step-4-set-up-user-permissions-for-using-the-device-files-for-intel-gpus_disable-timeout"  # noqa E501
                }
            ptimeout_info["preempt_timeout_ms=0 to prevent long-running jobs from hanging"] = error_dict
        check_result["CheckResult"] = ptimeout_info
    except Exception as error:
        check_result["CheckStatus"] = "ERROR"
        check_result["Message"] = str(error)
        check_result["HowToFix"] = "This error is unexpected. Please report the issue to " \
            "Diagnostics Utility for Intel® oneAPI Toolkits repository: " \
            "https://github.com/intel/diagnostics-utility."

    json_node.update({"Queried preempt_timeout_ms": check_result})


def run_hangcheck_check(data: dict) -> CheckSummary:
    result_json = {"CheckResult": {}}

    if not are_intel_gpus_found(data):
        intel_gpus_not_found_handler(result_json["CheckResult"])

    check_hangcheck_is_disabled(result_json["CheckResult"])
    check_non_zero_pre_emption_timeouts(result_json["CheckResult"])

    check_summary = CheckSummary(
        result=json.dumps(result_json, indent=4)
    )
    return check_summary


def get_api_version() -> str:
    return "0.2"


def get_check_list() -> List[CheckMetadataPy]:
    hangcheckCheck = CheckMetadataPy(
        name="hangcheck_check",
        type="Data",
        groups="gpu,sysinfo,profiling,runtime,target",
        descr="This check verifies that the GPU hangcheck option is disabled to allow long-running jobs.",
        dataReq="{\"intel_gpu_detector_check\": 2}",
        merit=80,
        timeout=5,
        version=2,
        run="run_hangcheck_check"
    )
    return [hangcheckCheck]
