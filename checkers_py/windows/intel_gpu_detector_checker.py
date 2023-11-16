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

import re
import json
from typing import List


def get_api_version() -> str:
    return "0.2"


def get_check_list() -> List[CheckMetadataPy]:
    someCheck = CheckMetadataPy(
        name="intel_gpu_detector_check",
        type="Data",
        groups="default,gpu,sysinfo,profiling,runtime,target",
        descr="This check shows information about Intel GPU(s) on the system, based on "
              "win32_VideoController WMI class.",
        dataReq="{}",
        merit=20,
        timeout=5,
        version=2,
        run="run_intel_gpu_detector_check"
    )
    return [someCheck]


def run_intel_gpu_detector_check(data: dict) -> CheckSummary:
    result_json = {"CheckResult": {}}
    result_json["CheckResult"] = get_gpu_driver_info()
    check_summary = CheckSummary(
        result=json.dumps(result_json, indent=4)
    )
    return check_summary


def get_gpu_driver_info() -> None:
    check_result = {"CheckResult": {}, "CheckStatus": "PASS"}
    try:
        controllers = fetch_video_controllers()
        controllers_count = len(controllers)
        if (not controllers_count == 0):
            for i in range(controllers_count):
                check_result["CheckResult"].update(
                    {f"Intel GPU #{i+1}": get_video_controller_properties(controllers[i])})
        else:
            check_result["CheckResult"] = "Undefined"
            check_result["CheckStatus"] = "FAIL"
            check_result["Message"] = "No Intel supported GPU detected." \
                " Use of the Intel® oneAPI Toolkits is not supported."
    except Exception as err:
        check_result["CheckResult"] = "Undefined"
        check_result["CheckStatus"] = "ERROR"
        check_result["Message"] = str(err)
        check_result["HowToFix"] = "This error is unexpected. Please report the issue to " \
            "Diagnostics Utility for Intel® oneAPI Toolkits repository: " \
            "https://github.com/intel/diagnostics-utility."

    return {"GPU information": check_result}


def fetch_video_controllers():
    res_devices = []
    out, err, _ = run_powershell_command(
        "Get-CimInstance -ClassName Win32_VideoController | "
        "format-list Name,Status,DriverVersion,PNPDeviceID")
    if (err):
        raise Exception(err)
    if (out == ""):
        return res_devices
    devices = out.split('\n\n')
    devices = [" ".join(device.replace('\n', ';').split()) for device in devices]

    for d in devices:
        device_as_map = {}
        name_match = re.search('Name : ([^;]*)', d)
        device_as_map["Name"] = name_match.group(1) if name_match is not None else None
        if (not re.search("intel", device_as_map["Name"], re.IGNORECASE)):
            continue
        status_match = re.search('Status : ([^;]*)', d)
        device_as_map["Status"] = status_match.group(1) if status_match is not None else None
        driver_version_match = re.search('DriverVersion : ([^;]*)', d)
        device_as_map["Driver Version"] = driver_version_match.group(
            1) if driver_version_match is not None else None
        pciID_match = re.search('PNPDeviceID : .*DEV_([^&]*)', d)
        device_as_map["PCI ID"] = pciID_match.group(1) if pciID_match is not None else None
        res_devices.append(device_as_map)
    return res_devices


def get_video_controller_properties(controller):
    check_result = {
        "CheckResult": {},
        "CheckStatus": "INFO"
    }
    check_result["CheckResult"].update(get_video_controller_name(controller))
    check_result["CheckResult"].update(get_video_controller_status(controller))
    check_result["CheckResult"].update(get_video_controller_driver_version(controller))
    check_result["CheckResult"].update(get_video_controller_pci_id(controller))
    check_result["CheckResult"].update(get_gpu_type(controller))
    return check_result


def get_video_controller_name(controller):
    check_result = {
        "CheckResult": controller["Name"],
        "CheckStatus": "INFO",
    }
    return {"Name": check_result}


def get_video_controller_status(controller):
    check_result = {
        "CheckResult": controller["Status"],
        "CheckStatus": "INFO",
    }
    return {"Status": check_result}


def get_video_controller_driver_version(controller):
    check_result = {
        "CheckResult": controller["Driver Version"],
        "CheckStatus": "INFO",
    }
    return {"Driver Version": check_result}


def get_video_controller_pci_id(controller):
    check_result = {
        "CheckResult": controller["PCI ID"],
        "CheckStatus": "INFO",
    }
    return {"PCI ID": check_result}


def get_gpu_type(controller):
    check_result = {
        "CheckResult": "Undefined",
        "CheckStatus": "INFO",
    }
    check_result["CheckResult"] = check_gpu_type_by_pci_id(controller["PCI ID"])
    return {"GPU type": check_result}


def check_gpu_type_by_pci_id(pci_id):
    pci_id_of_discrete_gpu = [
        "OBDA", "0BD9", "OBDB", "OBD7", "OBD6", "0BD0", "OBD5", "56C0", "56C1",

        "56B3", "56B2", "56A4", "56A3", "5697", "5696", "5695", "56B1", "56B0",
        "56A6", "56A5", "56A1", "56A0", "5694", "5693", "5692", "5691", "5690",

        "4907", "4905"
    ]
    if any(id == pci_id for id in pci_id_of_discrete_gpu):
        return "Discrete"
    else:
        return "Integrated"
