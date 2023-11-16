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
    check_result = {
        "CheckResult": platform.node(),
        "CheckStatus": "INFO"
    }
    json_node.update({"Hostname": check_result})


def _get_bios_vendor(json_node: Dict) -> None:
    check_result = {"BIOS vendor": {
        "CheckResult": "Undefined",
        "CheckStatus": "INFO"
    }}
    bios_reg_key = r"HARDWARE\DESCRIPTION\System\BIOS"
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, bios_reg_key) as key:
            bios_vendor = winreg.QueryValueEx(key, "BIOSVendor")[0]
            check_result["BIOS vendor"]["CheckResult"] = bios_vendor
    except Exception as error:
        check_result["BIOS vendor"]["CheckStatus"] = "ERROR"
        check_result["BIOS vendor"]["Message"] = str(error)
        check_result["BIOS vendor"]["HowToFix"] = "The Windows registry does not contain information about BIOS. " \
            "Ignore this error."  # noqa: E501
    json_node.update(check_result)


def _get_bios_version(json_node: Dict) -> None:
    check_result = {"BIOS version": {
        "CheckResult": "Undefined",
        "CheckStatus": "INFO"
    }}
    bios_reg_key = r"HARDWARE\DESCRIPTION\System\BIOS"
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, bios_reg_key) as key:
            bios_version = winreg.QueryValueEx(key, "BIOSVersion")[0]
            check_result["BIOS version"]["CheckResult"] = bios_version
    except Exception as error:
        check_result["BIOS version"]["CheckStatus"] = "ERROR"
        check_result["BIOS version"]["Message"] = str(error)
        check_result["BIOS version"]["HowToFix"] = "The Windows registry does not contain information about BIOS. " \
            "Ignore this error."  # noqa: E501
    json_node.update(check_result)


def _get_bios_release(json_node: Dict) -> None:
    check_result = {"BIOS release": {
        "CheckResult": "Undefined",
        "CheckStatus": "INFO"
    }}
    bios_reg_key = r"HARDWARE\DESCRIPTION\System\BIOS"
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, bios_reg_key) as key:
            bios_release_major = str(winreg.QueryValueEx(key, "BiosMajorRelease")[0])
            bios_release_minor = str(winreg.QueryValueEx(key, "BiosMinorRelease")[0])
            check_result["BIOS release"]["CheckResult"] = {
                "Major": {
                    "CheckResult": bios_release_major,
                    "CheckStatus": "INFO"
                },
                "Minor": {
                    "CheckResult": bios_release_minor,
                    "CheckStatus": "INFO"
                }
            }
    except Exception as error:
        check_result["BIOS release"]["CheckStatus"] = "ERROR"
        check_result["BIOS release"]["Message"] = str(error)
        check_result["BIOS release"]["HowToFix"] = "The Windows registry does not contain information about BIOS. " \
            "Ignore this error."  # noqa: E501
    json_node.update(check_result)


def _get_bios_date(json_node: Dict) -> None:
    check_result = {"BIOS date": {
        "CheckResult": "Undefined",
        "CheckStatus": "INFO"
    }}
    bios_reg_key = r"HARDWARE\DESCRIPTION\System\BIOS"
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, bios_reg_key) as key:
            bios_date = winreg.QueryValueEx(key, "BIOSReleaseDate")[0]
            check_result["BIOS date"]["CheckResult"] = bios_date
            check_result["BIOS date"]["Verbosity"] = 2
    except Exception as error:
        check_result["BIOS date"]["CheckStatus"] = "ERROR"
        check_result["BIOS date"]["Message"] = str(error)
        check_result["BIOS date"]["HowToFix"] = "The Windows registry does not contain information about BIOS. " \
            "Ignore this error."  # noqa: E501
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


def _get_os_edition(json_node: Dict) -> None:
    check_result = {
        "Edition": {
            "CheckResult": "Undefined",
            "CheckStatus": "INFO"
        }
    }
    os_edition_reg_key = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, os_edition_reg_key) as key:
            edition = winreg.QueryValueEx(key, "EditionID")[0]
            check_result["Edition"]["CheckResult"] = edition
    except Exception as error:
        check_result["Edition"]["CheckStatus"] = "ERROR"
        check_result["Edition"]["Message"] = str(error)
        check_result["Edition"]["HowToFix"] = "The Windows registry does not contain information about windows " \
            "edition. Ignore this error."  # noqa: E501
    json_node.update(check_result)


def _get_os_machine(json_node: Dict) -> None:
    check_result = {
        "Machine": {
            "CheckResult": "Undefined",
            "CheckStatus": "INFO"
        }
    }
    cpu_arh_key = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, cpu_arh_key) as key:
            machine = winreg.QueryValueEx(key, "PROCESSOR_ARCHITECTURE")[0]
            check_result["Machine"]["CheckResult"] = machine
    except Exception as error:
        check_result["Machine"]["CheckStatus"] = "ERROR"
        check_result["Machine"]["Message"] = str(error)
        check_result["Machine"]["HowToFix"] = "The Windows registry does not contain information about processor " \
            "architecture. Ignore this error."  # noqa: E501
    json_node.update(check_result)


def get_os_information(json_node: Dict) -> None:
    uname = platform.uname()
    check_result = {
        "CheckResult": {
            "System": {
                "CheckResult": uname.system,
                "CheckStatus": "INFO"
            },
            "Release": {
                "CheckResult": uname.release,
                "CheckStatus": "INFO"
            },
            "Version": {
                "CheckResult": uname.version,
                "CheckStatus": "INFO"
            }
        },
        "CheckStatus": "INFO"
    }
    _get_os_edition(check_result["CheckResult"])
    _get_os_machine(check_result["CheckResult"])
    json_node.update({"Operating system information": check_result})


def get_cpu_frequency(cpu_reg_key: str, json_node: Dict) -> None:
    verbosity_level = 1
    check_result = {
        "CheckResult": "Undefined",
        "CheckStatus": "INFO",
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
                        "CheckResult": "Undefined",
                        "CheckStatus": "INFO",
                        "Verbosity": verbosity_level
                    }
                    try:
                        with winreg.OpenKey(
                                winreg.HKEY_LOCAL_MACHINE, f"{cpu_reg_key}\\{core_reg_key}") as core_key:
                            frequency = winreg.QueryValueEx(core_key, "~MHz")[0]
                            cpu_core_frequency_value["CheckResult"] = f"{frequency} MHz"
                    except Exception as error:
                        cpu_core_frequency_value["CheckStatus"] = "ERROR"
                        cpu_core_frequency_value["Message"] = str(error)
                        cpu_core_frequency_value["Verbosity"] = 0
                    cpu_frequency.update({f"Core {core_number}": cpu_core_frequency_value})
                    core_number += 1
                except Exception:
                    break
        check_result["CheckResult"] = cpu_frequency
    except Exception as error:
        check_result["CheckStatus"] = "ERROR"
        check_result["Message"] = str(error)
        check_result["HowToFix"] = "The Windows registry does not contain information about CPU frequency. " \
            "Ignore this error."
    json_node.update({"CPU frequency": check_result})


def get_cpu_info(json_node: Dict) -> None:
    check_result = {
        "CheckResult": "Undefined",
        "CheckStatus": "INFO"
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
        cpu_info.update({"Model identifier": {"CheckResult": cpu_model_identifier, "CheckStatus": "INFO"}})
        cpu_info.update({"Model name": {"CheckResult": cpu_model_name, "CheckStatus": "INFO"}})
        cpu_info.update({"Vendor": {"CheckResult": cpu_vendor, "CheckStatus": "INFO", "Verbosity": 1}})
        cpu_info.update({"CPU count": {"CheckResult": cpu_count, "CheckStatus": "INFO"}})
        get_cpu_frequency(cpu_reg_key, cpu_info)
        check_result["CheckResult"] = cpu_info
    except Exception as error:
        check_result["CheckStatus"] = "ERROR"
        check_result["Message"] = str(error)
        check_result["HowToFix"] = "The Windows registry does not contain information about CPU. " \
            "Ignore this error."
    json_node.update({"CPU information": check_result})


def run_base_check(data: dict) -> CheckSummary:
    result_json = {"CheckResult": {},
                   "CheckStatus": "INFO"}

    get_hostname(result_json["CheckResult"])
    get_cpu_info(result_json["CheckResult"])
    get_bios_information(result_json["CheckResult"])
    get_os_information(result_json["CheckResult"])
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
        groups="default,sysinfo,compile,runtime,host,target",
        descr="This check shows information about hostname, CPU, BIOS and operating system.",
        dataReq="{}",
        merit=0,
        timeout=5,
        version=2,
        run="run_base_check"
    )
    return [someCheck]
