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
import subprocess
from typing import List, Dict


def get_hostname(json_node: Dict) -> None:
    value = {
        "Value": "Undefined",
        "RetVal": "INFO",
        "Command": "cat /etc/hostname"
    }
    try:
        with open("/etc/hostname", "r") as etc_hostname:
            hostname = etc_hostname.readline().strip()
            value["Value"] = hostname
    except Exception as error:
        value["RetVal"] = "ERROR"
        value["Message"] = str(error)
    json_node.update({"Hostname": value})


def _get_bios_vendor(json_node: Dict) -> None:
    value = {"BIOS vendor": {
        "Value": "Undefined",
        "RetVal": "INFO",
        "Command": "cat /sys/class/dmi/id/bios_vendor"
    }}
    try:
        with open("/sys/class/dmi/id/bios_vendor", "r") as bios_vendor_file:
            bios_vendor = bios_vendor_file.readline().strip()
            value["BIOS vendor"]["Value"] = bios_vendor
    except Exception as error:
        value["BIOS vendor"]["RetVal"] = "ERROR"
        value["BIOS vendor"]["Message"] = str(error)
    json_node.update(value)


def _get_bios_version(json_node: Dict) -> None:
    value = {"BIOS version": {
        "Value": "Undefined",
        "RetVal": "INFO",
        "Command": "cat /sys/class/dmi/id/bios_version"
    }}
    try:
        with open("/sys/class/dmi/id/bios_version", "r") as bios_verion_file:
            bios_version = bios_verion_file.readline().strip()
            value["BIOS version"]["Value"] = bios_version
    except Exception as error:
        value["BIOS version"]["RetVal"] = "ERROR"
        value["BIOS version"]["Message"] = str(error)
    json_node.update(value)


def _get_bios_release(json_node: Dict) -> None:
    value = {"BIOS release": {
        "Value": "Undefined",
        "RetVal": "INFO",
        "Command": "cat /sys/class/dmi/id/bios_release"
    }}
    can_provide_info = os.path.exists("/sys/class/dmi/id/bios_release")
    if can_provide_info:
        try:
            with open("/sys/class/dmi/id/bios_release", "r") as bios_release_file:
                bios_release = bios_release_file.readline().strip()
                value["BIOS release"]["Value"] = bios_release
                value["BIOS release"]["Verbosity"] = 1
        except Exception as error:
            value["BIOS release"]["RetVal"] = "ERROR"
            value["BIOS release"]["Message"] = str(error)
        json_node.update(value)


def _get_bios_date(json_node: Dict) -> None:
    value = {"BIOS date": {
        "Value": "Undefined",
        "RetVal": "INFO",
        "Command": "cat /sys/class/dmi/id/bios_date"
    }}
    can_provide_info = os.path.exists("/sys/class/dmi/id/bios_date")
    if can_provide_info:
        try:
            with open("/sys/class/dmi/id/bios_date", "r") as bios_date_file:
                bios_date = bios_date_file.readline().strip()
                value["BIOS date"]["Value"] = bios_date
                value["BIOS date"]["Verbosity"] = 2
        except Exception as error:
            value["BIOS date"]["RetVal"] = "ERROR"
            value["BIOS date"]["Message"] = str(error)
        json_node.update(value)


def get_bios_information(json_node: Dict) -> None:
    value = {"Value": "Undefined", "RetVal": "INFO"}
    bios_info = {}

    _get_bios_vendor(bios_info)
    _get_bios_version(bios_info)
    _get_bios_release(bios_info)
    _get_bios_date(bios_info)

    value["Value"] = bios_info
    json_node.update({"BIOS information": value})


def get_uname(json_node: Dict) -> None:
    value = {"Value": "Undefined", "RetVal": "INFO", "Command": "uname -a"}
    try:
        command = ["uname", "-a"]
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        stdout, _ = process.communicate()
        if process.returncode != 0:
            raise Exception("Cannot get information about operating system name")
        uname = stdout.splitlines()[0].strip()
        value["Value"] = uname
    except Exception as error:
        value["RetVal"] = "ERROR"
        value["Message"] = str(error)
    json_node.update({"Operating system name": value})


def get_cpu_frequency(json_node: Dict) -> None:
    verbosity_level = 1
    MHz_pattern = re.compile(r"cpu MHz\s*\:\s((\d*[.])?\d+)")
    value = {
        "Value": "Undefined",
        "RetVal": "INFO",
        "Verbosity": verbosity_level,
        "Command": "cat /proc/cpuinfo"}
    try:
        with open("/proc/cpuinfo", "r") as cpu_frequency_file:
            cpu_frequency = {}
            core_number = 0
            for line in cpu_frequency_file.readlines():
                result = MHz_pattern.search(line)
                if result:
                    cpu_frequency.update(
                        {f"Core {core_number}": {
                            "Value": f"{result.group(1)} MHz",
                            "RetVal": "INFO",
                            "Verbosity": verbosity_level
                        }})
                    core_number += 1
            value["Value"] = cpu_frequency
    except Exception as error:
        value["RetVal"] = "ERROR"
        value["Message"] = str(error)
    json_node.update({"CPU frequency": value})


def get_cpu_info(json_node: Dict) -> None:
    value = {
        "Value": "Undefined",
        "RetVal": "INFO",
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
        cpu_info.update({"Model name": {"Value": output["Model name"], "RetVal": "INFO"}})
        cpu_info.update({"Architecture": {"Value": output["Architecture"], "RetVal": "INFO"}})
        cpu_info.update({"Vendor": {"Value": output["Vendor ID"], "RetVal": "INFO", "Verbosity": 1}})
        cpu_info.update({"CPU count": {"Value": output["CPU(s)"], "RetVal": "INFO"}})
        cpu_info.update(
            {"Thread(s) per core": {"Value": output["Thread(s) per core"], "RetVal": "INFO", "Verbosity": 2}})
        cpu_info.update(
            {"Core(s) per socket": {"Value": output["Core(s) per socket"], "RetVal": "INFO", "Verbosity": 2}})
        cpu_info.update({"Socket(s)": {"Value": output["Socket(s)"], "RetVal": "INFO", "Verbosity": 2}})
        get_cpu_frequency(cpu_info)
        value["Value"] = cpu_info
    except Exception as error:
        value["RetVal"] = "ERROR"
        value["Message"] = str(error)
    json_node.update({"CPU information": value})


def run_base_check(data: dict) -> CheckSummary:
    result_json = {"Value": {}}

    get_hostname(result_json["Value"])
    get_cpu_info(result_json["Value"])
    get_bios_information(result_json["Value"])
    get_uname(result_json["Value"])

    check_summary = CheckSummary(
        result=json.dumps(result_json, indent=4)
    )

    return check_summary


def get_api_version() -> str:
    return "0.1"


def get_check_list() -> List[CheckMetadataPy]:
    someCheck = CheckMetadataPy(
        name="base_system_check",
        type="Data",
        tags="sysinfo,compile,runtime,host,target",
        descr="This check shows information about hostname, CPU, BIOS and operating system.",
        dataReq="{}",
        rights="user",
        timeout=5,
        version="0.1",
        run="run_base_check"
    )
    return [someCheck]
