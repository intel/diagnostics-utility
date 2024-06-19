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

import fnmatch
import os
import re
import json
import subprocess
from typing import List, Dict
from os.path import exists


def _function_cmd(command):
    fork_process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    std_out, _ = fork_process.communicate()
    return fork_process.returncode, std_out


def _get_i915_driver_loaded_info(json_node: Dict) -> None:
    check_result = {"CheckResult": "", "CheckStatus": "PASS", "Command": "lsmod | grep i915"}

    try:
        lsmod_process = subprocess.Popen(
            ["lsmod"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        grep_process = subprocess.Popen(
            ["grep", "i915"], stdin=lsmod_process.stdout,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        lsmod_process.stdout.close()

        if lsmod_process.wait() != 0:
            raise Exception("Cannot get information about kernel modules that are currently loaded.")
        stdout, _ = grep_process.communicate()
        if grep_process.returncode not in [0, 1]:
            raise Exception("Cannot get information about whether the Intel® Graphics Driver is loaded.")

        if not stdout.splitlines():
            check_result["CheckStatus"] = "FAIL"
            check_result["Message"] = "Module i915 is not loaded."
            check_result["HowToFix"] = "Try to load i915 module with the following command: modprobe i915."
            check_result["AutomationFix"] = "modprobe i915"

    except Exception as error:
        check_result["CheckStatus"] = "ERROR"
        check_result["Message"] = str(error)
        check_result["HowToFix"] = "This error is unexpected. Please report the issue to " \
            "Diagnostics Utility for oneAPI repository: " \
            "https://github.com/intel/diagnostics-utility."
    json_node.update({"Intel® Graphics Driver is loaded": check_result})


def _get_topology_path(json_node: Dict, bus) -> None:
    link = os.path.join("/sys/bus/pci/devices/", bus)
    relative_path = "/sys/devices"
    path = os.path.realpath(link)
    rel_path = os.path.relpath(path, relative_path)
    check_result = {
        "CheckResult": rel_path,
        "CheckStatus": "INFO",
        "Verbosity": 1,
        "Command": f"readlink {link}"
    }
    json_node.update({"PCI bus-tree": check_result})


def _get_tile_count(json_node: Dict, path) -> None:
    check_result = {
        "CheckResult": "Undefined",
        "CheckStatus": "INFO",
        "Verbosity": 1,
        "Command": f"ls {path} | grep -i 'gt[0-9]$' | wc -l"
    }
    try:
        ls_process = subprocess.Popen(
            ["ls", path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        grep_process = subprocess.Popen(
            ["grep", "-i", "gt[0-9]$"], stdin=ls_process.stdout,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        ls_process.stdout.close()

        if ls_process.wait() != 0:
            raise Exception(f"Cannot list information about the FILEs in directory: {path}. "
                            f"'ls' command returned error code {ls_process.returncode}.")

        stdout, _ = grep_process.communicate()
        if grep_process.returncode in [0, 1]:
            count = len(stdout.splitlines())
            check_result["CheckResult"] = count
        else:
            raise Exception("Cannot get information to determine tiles count."
                            f"'grep' command returned error code {grep_process.returncode}.")
    except Exception as error:
        check_result["CheckStatus"] = "ERROR"
        check_result["Message"] = str(error)
        check_result["Verbosity"] = 0
        check_result["HowToFix"] = "There is not a known solution for this error."
    json_node.update({"Tile count": check_result})


def _count_initializedGPU():
    cmd = ["ls", "/dev/dri/"]
    _, cmd_out = _function_cmd(cmd)
    cmd_count = cmd_out.count('render')
    return cmd_count


def _check_gpu_info_path():
    have_dri_access = os.access("/sys/kernel/debug/dri/", os.R_OK)
    if not have_dri_access:
        raise PermissionError("Unable to get information about initialized devices because "
                              "the user does not have read access to /sys/kernel/debug/dri/.")
    dirList = []
    for dName, _, fList in os.walk("/sys/kernel/debug/dri/"):
        for fileName in fList:
            if fnmatch.fnmatch(fileName, "i915_gpu_info"):
                dirList.append(dName)
    filter_path = filter(None, dirList)
    return filter_path


def _get_initializedGPU(json_node: Dict) -> None:
    paths = _check_gpu_info_path()
    counter_loop = 1
    for path in paths:
        output = {}
        with open(f"{path}/i915_gpu_info", "r") as gpu_info_file:
            lines = gpu_info_file.readlines()
            for line in lines:
                if re.search(".:.", line):
                    key, val = [elem.strip() for elem in line.split(":", 1)]
                    output.update({key: val})
        with open(f"{path}/name", "r") as name_file:
            bus = name_file.readline().strip().split()[1][4:]

        gpu = {"GPU id": {
            "CheckResult": output["PCI ID"],
            "CheckStatus": "INFO",
            "Command": f"cat {path}/i915_gpu_info | grep -i 'pci id' | awk '{{print $3}}'"
        },
            "Bus info": {
                "CheckResult": bus,
                "CheckStatus": "INFO",
                "Verbosity": 1,
                "Command": f"cat {path}/name | awk '{{print $2}}'"
        },
            "EU Counts": {
                "CheckResult": output["EU total"],
                "CheckStatus": "INFO",
                "Verbosity": 1,
                "Command": f"cat {path}/i915_gpu_info | grep -i 'EU total' | awk '{{print $3}}'"
        },
            "Platform": {
                "CheckResult": output["Platform"],
                "CheckStatus": "INFO",
                "Verbosity": 1,
                "Command": f"cat {path}/i915_gpu_info | grep -i '^platform' | awk '{{print $2}}' | uniq"
        },
            "GuC firmware": {
                "CheckResult": output["GuC firmware"].split("/")[-1],
                "CheckStatus": "INFO",
                "Verbosity": 1,
                "Command": f"cat {path}/i915_gpu_info | grep -i 'GuC firmware' | awk '{{print $3}}' | "
                           "xargs basename"
        },
            "HuC firmware": {
                "CheckResult": output["HuC firmware"].split("/")[-1],
                "CheckStatus": "INFO",
                "Verbosity": 1,
                "Command": f"cat {path}/i915_gpu_info | grep -i 'HuC firmware' | awk '{{print $3}}' | "
                           "xargs basename"
        },
            "GPU type": {
                "CheckResult": "Discrete" if output["is_dgfx"] == "yes" else "Integrated",
                "CheckStatus": "INFO",
                "Verbosity": 1,
                "Command": f"cat {path}/i915_gpu_info | grep -i 'is_dgfx' | awk '{{print $0}}'"
        }
        }
        _get_topology_path(gpu, bus)
        _get_tile_count(gpu, path)
        gpu_info = {f"Intel GPU #{counter_loop}": {
            "CheckResult": gpu,
            "CheckStatus": "INFO"}}
        json_node.update(gpu_info)
        counter_loop += 1


def _count_uninitializedGPU():
    hw_count = 0
    if exists('/sbin/lspci'):
        command = ['/sbin/lspci']
    else:
        command = ["lspci"]
    return_code, stdout = _function_cmd(command)
    if return_code != 0:
        raise Exception("Cannot get information about GPU(s).")
    for line in stdout.splitlines():
        if "VGA compatible controller" in line or "Display controller" in line:
            is_intel_gpu = len(line.split("Intel Corporation")) == 2
            if is_intel_gpu:
                hw_count += 1
    return hw_count


def _get_uninitializedGPU(slots, json_node: Dict) -> int:
    have_dri_access = os.access("/sys/kernel/debug/dri/", os.R_OK)
    if not have_dri_access:
        raise PermissionError("Unable to get information about uninitialized devices because "
                              "the user does not have read access to /sys/kernel/debug/dri/.")
    hw_count = 0
    if exists('/sbin/lspci'):
        command = ['/sbin/lspci']
    else:
        command = ["lspci"]
    return_code, stdout = _function_cmd(command)
    if return_code != 0:
        raise Exception("Cannot get information about GPU(s).")
    for line in stdout.splitlines():
        if "VGA compatible controller" in line or "Display controller" in line:
            is_intel_gpu = len(line.split("Intel Corporation")) == 2
            if is_intel_gpu and line.split()[0] not in slots:
                hw_count += 1
                gpu = {
                    f"Intel GPU #{hw_count}": {
                        "CheckResult": {
                            "Bus info": {
                                "CheckResult": line.split()[0],
                                "CheckStatus": "INFO"
                            },
                            "Name": {
                                "CheckResult": " ".join(line.split()[1:]),
                                "CheckStatus": "INFO"
                            },
                        },
                        "CheckStatus": "INFO",
                        "Command": 'lspci | grep -e "VGA compatible controller" -e "Display controller"'
                                   ' | grep -i "Intel Corporation"'
                    }
                }
                json_node.update(gpu)
    return hw_count


def get_gpu_info(json_node: Dict) -> None:
    check_result = {"CheckResult": "Undefined", "CheckStatus": "INFO"}
    try:

        gpu_full_info = {}
        _get_i915_driver_loaded_info(gpu_full_info)

        gpu_counter = _count_initializedGPU()
        all_gpu_counter = _count_uninitializedGPU()

        gpu_detailed_info = {}
        slots = []
        if gpu_counter != 0:
            try:
                gpu_info = {}
                _get_initializedGPU(gpu_info)
                gpu_detailed_info.update({
                    "Initialized devices": {
                        "CheckResult": gpu_info,
                        "CheckStatus": "INFO"
                    }
                })
                for key in gpu_info:
                    slots.append(re.sub(r'^.*?:', '', gpu_info[key]
                                 ["CheckResult"]["Bus info"]["CheckResult"]))
            except PermissionError as error:
                gpu_detailed_info.update({
                    "Initialized devices": {
                        "CheckResult": "",
                        "CheckStatus": "ERROR",
                        "Message": str(error),
                        "HowToFix": "Try to run the Diagnostics Utility for oneAPI "
                                    "with administrative privilege or join the video and render groups."
                    }
                })
            except Exception as error:
                gpu_detailed_info.update({
                    "Initialized devices": {
                        "CheckResult": "",
                        "CheckStatus": "ERROR",
                        "Message": str(error),
                        "HowToFix": "This error is unexpected. Please report the issue to "
                                    "Diagnostics Utility for oneAPI repository: "
                                    "https://github.com/intel/diagnostics-utility."
                    }
                })

        if all_gpu_counter > gpu_counter:
            try:
                gpu_info = {}
                count_hw = _get_uninitializedGPU(slots, gpu_info)
                if count_hw != 0:
                    gpu_detailed_info.update({
                        "Uninitialized devices": {
                            "CheckResult": gpu_info,
                            "CheckStatus": "ERROR",
                            "Message": "Some GPU(s) are not initialized.",
                            "HowToFix": "To initialize GPU(s), please run the following command: "
                                        "modprobe i915.",
                            "AutomationFix": "modprobe i915"

                        }
                    })
            except PermissionError as error:
                gpu_detailed_info.update({
                    "Uninitialized devices": {
                        "CheckResult": "",
                        "CheckStatus": "ERROR",
                        "Message": str(error),
                        "HowToFix": "Try to run the Diagnostics Utility for oneAPI "
                                    "with administrative privilege or join the video and render groups."
                    }
                })
            except Exception as error:
                gpu_detailed_info.update({
                    "Uninitialized devices": {
                        "CheckResult": "",
                        "CheckStatus": "ERROR",
                        "Message": str(error),
                        "HowToFix": "This error is unexpected. Please report the issue to "
                                    "Diagnostics Utility for oneAPI repository: "
                                    "https://github.com/intel/diagnostics-utility."
                    }
                })

        gpus_found = gpu_counter != 0 or all_gpu_counter > gpu_counter
        if gpus_found:
            gpu_full_info.update({
                "Intel GPU(s) is present on the bus": {
                    "CheckStatus": "PASS",
                    "CheckResult": ""
                },
                "Number of Intel GPU(s) on the system": {
                    "CheckStatus": "INFO",
                    "CheckResult": all_gpu_counter
                }
            })
            gpu_full_info.update(gpu_detailed_info)
        else:
            gpu_full_info.update({
                "Intel GPU(s) is present on the bus": {
                    "CheckStatus": "FAIL",
                    "Message": "There are no Intel GPU(s) on the system.",
                    "HowToFix": "Plug Intel GPU(s) into an empty PCI slot.",
                    "CheckResult": ""
                }
            })

        check_result["CheckResult"] = gpu_full_info
    except Exception as error:
        check_result["CheckStatus"] = "ERROR"
        check_result["CheckResult"] = {
            "Intel GPU(s) is present on the bus": {
                "CheckStatus": "ERROR",
                "Message": str(error),
                "CheckResult": "",
                "HowToFix": "This error is unexpected. Please report the issue to "
                            "Diagnostics Utility for oneAPI repository: "
                            "https://github.com/intel/diagnostics-utility."
            }
        }
    json_node.update({"GPU information": check_result})


def run_intel_gpu_detector_check(data: dict) -> CheckSummary:
    result_json = {"CheckResult": {}}

    get_gpu_info(result_json["CheckResult"])

    check_summary = CheckSummary(
        result=json.dumps(result_json, indent=4)
    )

    return check_summary


def get_api_version() -> str:
    return "0.2"


def get_check_list() -> List[CheckMetadataPy]:
    someCheck = CheckMetadataPy(
        name="intel_gpu_detector_check",
        type="Data",
        groups="default,gpu,sysinfo,profiling,runtime,target",
        descr="This check shows which Intel GPU(s) is on the system, based on "
              "lspci information and internal table.",
        dataReq="{}",
        merit=20,
        timeout=5,
        version=2,
        run="run_intel_gpu_detector_check"
    )
    return [someCheck]
