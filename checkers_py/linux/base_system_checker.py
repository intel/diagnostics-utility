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

import os
import re
import json
import platform
import subprocess

from typing import List, Dict


def get_hostname(json_node: Dict) -> None:
    check_result = {
        "CheckResult": "Undefined",
        "CheckStatus": "INFO",
        "Command": "cat /etc/hostname"
    }
    try:
        with open("/etc/hostname", "r") as etc_hostname:
            hostname = etc_hostname.readline().strip()
            check_result["CheckResult"] = hostname
    except Exception as error:
        check_result["CheckStatus"] = "ERROR"
        check_result["Message"] = str(error)
        check_result["HowToFix"] = "The system does not contain '/etc/hostname'. Ignore this error."
    json_node.update({"Hostname": check_result})


def _get_bios_vendor(json_node: Dict) -> None:
    check_result = {"BIOS vendor": {
        "CheckResult": "Undefined",
        "CheckStatus": "INFO",
        "Command": "cat /sys/class/dmi/id/bios_vendor"
    }}
    try:
        with open("/sys/class/dmi/id/bios_vendor", "r") as bios_vendor_file:
            bios_vendor = bios_vendor_file.readline().strip()
            check_result["BIOS vendor"]["CheckResult"] = bios_vendor
    except Exception as error:
        check_result["BIOS vendor"]["CheckStatus"] = "ERROR"
        check_result["BIOS vendor"]["Message"] = str(error)
        check_result["BIOS vendor"]["HowToFix"] = "The system does not contain information about BIOS. " \
            "Ignore this error."
    json_node.update(check_result)


def _get_bios_version(json_node: Dict) -> None:
    check_result = {"BIOS version": {
        "CheckResult": "Undefined",
        "CheckStatus": "INFO",
        "Command": "cat /sys/class/dmi/id/bios_version"
    }}
    try:
        with open("/sys/class/dmi/id/bios_version", "r") as bios_verion_file:
            bios_version = bios_verion_file.readline().strip()
            check_result["BIOS version"]["CheckResult"] = bios_version
    except Exception as error:
        check_result["BIOS version"]["CheckStatus"] = "ERROR"
        check_result["BIOS version"]["Message"] = str(error)
        check_result["BIOS version"]["HowToFix"] = "The system does not contain information about BIOS. " \
            "Ignore this error."
    json_node.update(check_result)


def _get_bios_release(json_node: Dict) -> None:
    check_result = {"BIOS release": {
        "CheckResult": "Undefined",
        "CheckStatus": "INFO",
        "Command": "cat /sys/class/dmi/id/bios_release"
    }}
    can_provide_info = os.path.exists("/sys/class/dmi/id/bios_release")
    if can_provide_info:
        try:
            with open("/sys/class/dmi/id/bios_release", "r") as bios_release_file:
                bios_release = bios_release_file.readline().strip()
                check_result["BIOS release"]["CheckResult"] = bios_release
                check_result["BIOS release"]["Verbosity"] = 1
        except Exception as error:
            check_result["BIOS release"]["CheckStatus"] = "ERROR"
            check_result["BIOS release"]["Message"] = str(error)
            check_result["BIOS release"]["HowToFix"] = ""\
                "The system does not contain information about BIOS. " \
                "Ignore this error."
        json_node.update(check_result)


def _get_bios_date(json_node: Dict) -> None:
    check_result = {"BIOS date": {
        "CheckResult": "Undefined",
        "CheckStatus": "INFO",
        "Command": "cat /sys/class/dmi/id/bios_date"
    }}
    can_provide_info = os.path.exists("/sys/class/dmi/id/bios_date")
    if can_provide_info:
        try:
            with open("/sys/class/dmi/id/bios_date", "r") as bios_date_file:
                bios_date = bios_date_file.readline().strip()
                check_result["BIOS date"]["CheckResult"] = bios_date
                check_result["BIOS date"]["Verbosity"] = 2
        except Exception as error:
            check_result["BIOS date"]["CheckStatus"] = "ERROR"
            check_result["BIOS date"]["Message"] = str(error)
            check_result["BIOS date"]["HowToFix"] = "The system does not contain information about BIOS. " \
                "Ignore this error."
        json_node.update(check_result)


def get_bios_information(json_node: Dict) -> None:
    check_result = {"CheckResult": "Undefined", "CheckStatus": "INFO"}
    bios_info = {}

    _get_bios_vendor(bios_info)
    _get_bios_version(bios_info)
    _get_bios_release(bios_info)
    _get_bios_date(bios_info)

    check_result["CheckResult"] = bios_info
    json_node.update({"BIOS information": check_result})


def get_uname(json_node: Dict) -> None:
    uname = platform.uname()
    check_result = {
        "CheckResult": {
            "System": {
                "CheckResult": uname.system,
                "CheckStatus": "INFO"
            },
            "Node": {
                "CheckResult": uname.node,
                "CheckStatus": "INFO"
            },
            "Release": {
                "CheckResult": uname.release,
                "CheckStatus": "INFO"
            },
            "Version": {
                "CheckResult": uname.version,
                "CheckStatus": "INFO"
            },
            "Machine": {
                "CheckResult": uname.machine,
                "CheckStatus": "INFO"
            },
            "Processor": {
                "CheckResult": uname.processor,
                "CheckStatus": "INFO"
            }
        },
        "CheckStatus": "INFO",
        "Command": "uname -a"
    }
    json_node.update({"Operating system information": check_result})


def get_cpu_frequency(json_node: Dict) -> None:
    verbosity_level = 1
    MHz_pattern = re.compile(r"cpu MHz\s*\:\s((\d*[.])?\d+)")
    check_result = {
        "CheckResult": "Undefined",
        "CheckStatus": "INFO",
        "Verbosity": verbosity_level,
        "Command": "cat /proc/cpuinfo"
    }
    try:
        with open("/proc/cpuinfo", "r") as cpu_frequency_file:
            cpu_frequency = {}
            core_number = 0
            for line in cpu_frequency_file.readlines():
                result = MHz_pattern.search(line)
                if result:
                    cpu_frequency.update(
                        {f"Core {core_number}": {
                            "CheckResult": f"{result.group(1)} MHz",
                            "CheckStatus": "INFO",
                            "Verbosity": verbosity_level
                        }})
                    core_number += 1
            check_result["CheckResult"] = cpu_frequency
    except Exception as error:
        check_result["CheckStatus"] = "ERROR"
        check_result["Message"] = str(error)
        check_result["HowToFix"] = "The system does not contain information about CPU frequency. " \
            "Ignore this error."
    json_node.update({"CPU frequency": check_result})


def get_cpu_info(json_node: Dict) -> None:
    check_result = {
        "CheckResult": "Undefined",
        "CheckStatus": "INFO",
        "Command": "lscpu"
    }
    try:
        command = ["lscpu"]
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        stdout, _ = process.communicate()
        if process.returncode != 0:
            raise Exception("Cannot get information about CPU")
        output = {}
        for line in stdout.splitlines():
            key, val = [elem.strip() for elem in line.split(":", 1)]
            output.update({key: val})

        cpu_info = {}
        cpu_info.update({"Model name": {"CheckResult": output["Model name"], "CheckStatus": "INFO"}})
        cpu_info.update({"Architecture": {"CheckResult": output["Architecture"], "CheckStatus": "INFO"}})
        cpu_info.update({"Vendor": {"CheckResult": output["Vendor ID"], "CheckStatus": "INFO", "Verbosity": 1}})  # noqa: E501
        cpu_info.update({"CPU count": {"CheckResult": output["CPU(s)"], "CheckStatus": "INFO"}})
        cpu_info.update(
            {"Thread(s) per core":
             {"CheckResult": output["Thread(s) per core"],
              "CheckStatus": "INFO",
                 "Verbosity": 2}})
        cpu_info.update(
            {"Core(s) per socket":
             {"CheckResult": output["Core(s) per socket"],
              "CheckStatus": "INFO",
                 "Verbosity": 2}})
        cpu_info.update(
            {"Socket(s)": {"CheckResult": output["Socket(s)"], "CheckStatus": "INFO", "Verbosity": 2}})
        get_cpu_frequency(cpu_info)
        check_result["CheckResult"] = cpu_info
    except Exception as error:
        check_result["CheckStatus"] = "ERROR"
        check_result["Message"] = str(error)
        check_result["HowToFix"] = "The system does not contain information about CPU. " \
            "Ignore this error."
    json_node.update({"CPU information": check_result})


def run_base_check(data: dict) -> CheckSummary:
    result_json = {"CheckResult": {}}

    get_hostname(result_json["CheckResult"])
    get_cpu_info(result_json["CheckResult"])
    get_bios_information(result_json["CheckResult"])
    get_uname(result_json["CheckResult"])

    check_summary = CheckSummary(
        result=json.dumps(result_json, indent=4)
    )

    return check_summary


def get_api_version() -> str:
    return "0.2"


def get_check_list() -> List[CheckMetadataPy]:
    someCheck = CheckMetadataPy(
        name="base_system_check",
        type="Data",
        groups="sysinfo,compile,runtime,host,target",
        descr="This check shows information about hostname, CPU, BIOS and operating system.",
        dataReq="{}",
        merit=0,
        timeout=5,
        version=2,
        run="run_base_check"
    )
    return [someCheck]
