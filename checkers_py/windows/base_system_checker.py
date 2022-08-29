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
import winreg
import platform

from typing import List, Dict


def get_hostname(json_node: Dict) -> None:
    value = {
        "Value": platform.node(),
        "RetVal": "INFO"
    }
    json_node.update({"Hostname": value})


def _get_bios_vendor(json_node: Dict) -> None:
    value = {"BIOS vendor": {
        "Value": "Undefined",
        "RetVal": "INFO"
    }}
    bios_reg_key = r"HARDWARE\DESCRIPTION\System\BIOS"
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, bios_reg_key) as key:
            bios_vendor = winreg.QueryValueEx(key, "BIOSVendor")[0]
            value["BIOS vendor"]["Value"] = bios_vendor
    except Exception as error:
        value["BIOS vendor"]["RetVal"] = "ERROR"
        value["BIOS vendor"]["Message"] = str(error)
        value["BIOS vendor"]["HowToFix"] = "The Windows registry does not contain information about BIOS. " \
                                           "Ignore this error."
    json_node.update(value)


def _get_bios_version(json_node: Dict) -> None:
    value = {"BIOS version": {
        "Value": "Undefined",
        "RetVal": "INFO"
    }}
    bios_reg_key = r"HARDWARE\DESCRIPTION\System\BIOS"
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, bios_reg_key) as key:
            bios_version = winreg.QueryValueEx(key, "BIOSVersion")[0]
            value["BIOS version"]["Value"] = bios_version
    except Exception as error:
        value["BIOS version"]["RetVal"] = "ERROR"
        value["BIOS version"]["Message"] = str(error)
        value["BIOS version"]["HowToFix"] = "The Windows registry does not contain information about BIOS. " \
                                            "Ignore this error."
    json_node.update(value)


def _get_bios_release(json_node: Dict) -> None:
    value = {"BIOS release": {
        "Value": "Undefined",
        "RetVal": "INFO"
    }}
    bios_reg_key = r"HARDWARE\DESCRIPTION\System\BIOS"
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, bios_reg_key) as key:
            bios_release_major = str(winreg.QueryValueEx(key, "BiosMajorRelease")[0])
            bios_release_minor = str(winreg.QueryValueEx(key, "BiosMinorRelease")[0])
            value["BIOS release"]["Value"] = {
                "Major": {
                    "Value": bios_release_major,
                    "RetVal": "INFO"
                },
                "Minor": {
                    "Value": bios_release_minor,
                    "RetVal": "INFO"
                }
            }
    except Exception as error:
        value["BIOS release"]["RetVal"] = "ERROR"
        value["BIOS release"]["Message"] = str(error)
        value["BIOS release"]["HowToFix"] = "The Windows registry does not contain information about BIOS. " \
                                            "Ignore this error."
    json_node.update(value)


def _get_bios_date(json_node: Dict) -> None:
    value = {"BIOS date": {
        "Value": "Undefined",
        "RetVal": "INFO"
    }}
    bios_reg_key = r"HARDWARE\DESCRIPTION\System\BIOS"
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, bios_reg_key) as key:
            bios_date = winreg.QueryValueEx(key, "BIOSReleaseDate")[0]
            value["BIOS date"]["Value"] = bios_date
            value["BIOS date"]["Verbosity"] = 2
    except Exception as error:
        value["BIOS date"]["RetVal"] = "ERROR"
        value["BIOS date"]["Message"] = str(error)
        value["BIOS date"]["HowToFix"] = "The Windows registry does not contain information about BIOS. " \
                                         "Ignore this error."
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


def _get_os_edition(json_node: Dict) -> None:
    value = {
        "Edition": {
            "Value": "Undefined",
            "RetVal": "INFO"
        }
    }
    os_edition_reg_key = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, os_edition_reg_key) as key:
            edition = winreg.QueryValueEx(key, "EditionID")[0]
            value["Edition"]["Value"] = edition
    except Exception as error:
        value["Edition"]["RetVal"] = "ERROR"
        value["Edition"]["Message"] = str(error)
        value["Edition"]["HowToFix"] = "The Windows registry does not contain information about windows " \
                                       "edition. Ignore this error."
    json_node.update(value)


def _get_os_machine(json_node: Dict) -> None:
    value = {
        "Machine": {
            "Value": "Undefined",
            "RetVal": "INFO"
        }
    }
    cpu_arh_key = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, cpu_arh_key) as key:
            machine = winreg.QueryValueEx(key, "PROCESSOR_ARCHITECTURE")[0]
            value["Machine"]["Value"] = machine
    except Exception as error:
        value["Machine"]["RetVal"] = "ERROR"
        value["Machine"]["Message"] = str(error)
        value["Machine"]["HowToFix"] = "The Windows registry does not contain information about processor " \
                                       "architecture. Ignore this error."
    json_node.update(value)


def get_os_information(json_node: Dict) -> None:
    uname = platform.uname()
    value = {
        "Value": {
            "System": {
                "Value": uname.system,
                "RetVal": "INFO"
            },
            "Release": {
                "Value": uname.release,
                "RetVal": "INFO"
            },
            "Version": {
                "Value": uname.version,
                "RetVal": "INFO"
            }
        },
        "RetVal": "INFO"
    }
    _get_os_edition(value["Value"])
    _get_os_machine(value["Value"])
    json_node.update({"Operating system information": value})


def get_cpu_frequency(cpu_reg_key: str, json_node: Dict) -> None:
    verbosity_level = 1
    value = {
        "Value": "Undefined",
        "RetVal": "INFO",
        "Verbosity": verbosity_level
    }
    try:
        cpu_frequency = {}
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, cpu_reg_key) as key:
            core_number = 0
            while True:
                try:
                    core_reg_key = winreg.EnumKey(key, core_number)
                    cpu_core_frequency_value = {
                        "Value": "Undefined",
                        "RetVal": "INFO",
                        "Verbosity": verbosity_level
                    }
                    try:
                        with winreg.OpenKey(
                                winreg.HKEY_LOCAL_MACHINE, f"{cpu_reg_key}\\{core_reg_key}") as core_key:
                            frequency = winreg.QueryValueEx(core_key, "~MHz")[0]
                            cpu_core_frequency_value["Value"] = f"{frequency} MHz"
                    except Exception as error:
                        cpu_core_frequency_value["RetVal"] = "ERROR"
                        cpu_core_frequency_value["Message"] = str(error)
                        cpu_core_frequency_value["Verbosity"] = 0
                    cpu_frequency.update({f"Core {core_number}": cpu_core_frequency_value})
                    core_number += 1
                except Exception:
                    break
        value["Value"] = cpu_frequency
    except Exception as error:
        value["RetVal"] = "ERROR"
        value["Message"] = str(error)
        value["HowToFix"] = "The Windows registry does not contain information about CPU frequency. " \
                            "Ignore this error."
    json_node.update({"CPU frequency": value})


def get_cpu_info(json_node: Dict) -> None:
    value = {
        "Value": "Undefined",
        "RetVal": "INFO"
    }
    cpu_reg_key = r"HARDWARE\DESCRIPTION\System\CentralProcessor"
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, cpu_reg_key) as key:
            cpu_count = 0
            while True:
                try:
                    winreg.EnumKey(key, cpu_count)
                    cpu_count += 1
                except Exception:
                    break

        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, f"{cpu_reg_key}\\0") as key:
            cpu_model_identifier = winreg.QueryValueEx(key, "Identifier")[0]
            cpu_model_name = winreg.QueryValueEx(key, "ProcessorNameString")[0]
            cpu_vendor = winreg.QueryValueEx(key, "VendorIdentifier")[0]

        cpu_info = {}
        cpu_info.update({"Model identifier": {"Value": cpu_model_identifier, "RetVal": "INFO"}})
        cpu_info.update({"Model name": {"Value": cpu_model_name, "RetVal": "INFO"}})
        cpu_info.update({"Vendor": {"Value": cpu_vendor, "RetVal": "INFO", "Verbosity": 1}})
        cpu_info.update({"CPU count": {"Value": cpu_count, "RetVal": "INFO"}})
        get_cpu_frequency(cpu_reg_key, cpu_info)
        value["Value"] = cpu_info
    except Exception as error:
        value["RetVal"] = "ERROR"
        value["Message"] = str(error)
        value["HowToFix"] = "The Windows registry does not contain information about CPU. " \
                            "Ignore this error."
    json_node.update({"CPU information": value})


def run_base_check(data: dict) -> CheckSummary:
    result_json = {"Value": {}}

    get_hostname(result_json["Value"])
    get_cpu_info(result_json["Value"])
    get_bios_information(result_json["Value"])
    get_os_information(result_json["Value"])

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
        tags="default,sysinfo,compile,runtime,host,target",
        descr="This check shows information about hostname, CPU, BIOS and the operating system.",
        dataReq="{}",
        merit=0,
        timeout=5,
        version=1,
        run="run_base_check"
    )
    return [someCheck]
