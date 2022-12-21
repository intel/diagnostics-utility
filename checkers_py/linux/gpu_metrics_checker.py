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

from checkers_py.linux.common.gpu_helper import is_level_zero_initialized
from modules.check import CheckSummary, CheckMetadataPy

import json
import os
from typing import List, Dict


known_devices: Dict[str, Dict[str, str]] = {
    "0x4905": {
        "freq": "1550",
        "flops": "2000",
        "mem_bw": "56",
        "pcie_bw": "4.8"
    },
    "0x3e98": {
        "freq": "1200",
        "flops": "450",
        "mem_bw": "30",
        "pcie_bw": "10"
    },
    "0x193b": {
        "freq": "950",
        "flops": "1000",
        "mem_bw": "26",
        "pcie_bw": "13"
    },
    "0x203": {
        "freq": "1200",
        "flops": "2000",
        "mem_bw": "70",
        "pcie_bw": "15"
    },
    "0x205": {
        "freq": "1200",
        "flops": "6800",
        "mem_bw": "220",
        "pcie_bw": "15"
    },
    "0x20a": {
        "freq": "1200",
        "flops": "4000",
        "mem_bw": "125",
        "pcie_bw": "15"
    }
}


class Device:
    name: str
    id: str
    max_freq: str
    min_freq: str
    cur_freq: str
    mem_bandwidth: str
    pcie_bandwidth: str
    gpu_type: str
    enumeration: str

    def __init__(
            self,
            name: str,
            id: str,
            max_freq: str,
            min_freq: str,
            cur_freq: str,
            mem_bandwidth: str,
            pcie_bandwidth: str,
            gpu_type: str,
            enumeration: str
            ) -> None:
        self.name = name
        self.id = id
        self.max_freq = max_freq
        self.min_freq = min_freq
        self.cur_freq = cur_freq
        self.mem_bandwidth = mem_bandwidth
        self.pcie_bandwidth = pcie_bandwidth
        self.gpu_type = gpu_type
        self.enumeration = enumeration


def parse_devices(data: Dict) -> List[Device]:
    result: List[Device] = []

    is_lz_initialized, lz_driver_message = is_level_zero_initialized(data)
    if not is_lz_initialized:
        raise Exception(lz_driver_message)

    lz_slice = data["gpu_backend_check"]["Value"]["GPU"]["Value"]["Intel® oneAPI Level Zero Driver"]["Value"]["Driver information"]["Value"]  # noqa: E501
    if not isinstance(lz_slice, dict):
        return result
    driver_number = int(lz_slice["Installed driver number"]["Value"])
    counter = 0
    for i in range(driver_number):
        devices_slice = lz_slice[f"Driver # {i}"]["Value"]["Devices"]
        device_number = int(devices_slice["Value"]["Device number"]["Value"])
        for j in range(device_number):
            device_slice = devices_slice["Value"][f"Device # {j}"]["Value"]
            device_type = device_slice["Device type"]["Value"]
            if device_type != "Graphics Processing Unit":
                continue
            data_slice = data["intel_gpu_detector_check"]["Value"]["GPU information"]["Value"]["Initialized devices"]["Value"]  # noqa: E501
            type_slice = data_slice[f"Intel GPU #{j+1}"]["Value"]
            device = Device(
                name=device_slice["Device name"]["Value"],
                id=device_slice["Device ID"]["Value"],
                max_freq=device_slice["Device maximum frequency, MHz"]["Value"],
                min_freq=device_slice["Device minimum frequency, MHz"]["Value"],
                cur_freq=device_slice["Device current frequency, MHz"]["Value"],
                mem_bandwidth=device_slice["Memory bandwidth, GB/s"]["Value"],
                pcie_bandwidth=device_slice["PCIe bandwidth, GB/s"]["Value"],
                gpu_type=type_slice["GPU type"]["Value"],
                enumeration=str(counter)
                )
            counter += 1
            result.append(device)
        return result


def have_administrative_priviliges():
    have_dri_access = os.access("/sys/kernel/debug/dri/", os.R_OK)
    if not have_dri_access:
        raise PermissionError("Unable to get information about uninitialized devices because "
                              "the user does not have read access to /sys/kernel/debug/dri/.")


def show_metrics_for_unknown_device(json_node: Dict, device: Device) -> None:
    value = {
        "Value": "Undefined",
        "RetVal": "WARNING",
        "Message": "For this GPU, good numbers are not known."
    }
    device_metrics = {}

    frequency = {"GPU Frequency, MHz (Max/Target)": {"Value": f"{device.max_freq}/unknown", "RetVal": "INFO"}}
    if device.max_freq == "unknown":
        frequency["GPU Frequency, MHz (Max/Target)"].update({"RetVal": "ERROR"})
        frequency["GPU Frequency, MHz (Max/Target)"].update(
            {"Message": "The Level Zero driver cannot find out information about frequency.",
            "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."}) # noqa E501)
    device_metrics.update(frequency)

    mem_bandwidth = {
        "Memory bandwidth, GB/s (Max/Target)": {"Value": f"{device.mem_bandwidth}/unknown", "RetVal": "INFO"}}
    if device.mem_bandwidth == "unknown" and device.gpu_type == "Discrete":
        mem_bandwidth["Memory bandwidth, GB/s (Max/Target)"].update({"RetVal": "ERROR"})
        mem_bandwidth["Memory bandwidth, GB/s (Max/Target)"].update(
            {"Message": "The Level Zero driver cannot find out information about memory bandwidth.",
            "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."}) # noqa E501
        device_metrics.update(mem_bandwidth)
    elif device.mem_bandwidth != "unknown" and device.gpu_type == "Discrete":
        device_metrics.update(mem_bandwidth)
    else:
        pass

    pcie_bandwidth = {
        "PCIe bandwidth, GB/s (Max/Target)": {"Value": f"{device.pcie_bandwidth}/unknown", "RetVal": "INFO"}}
    if device.pcie_bandwidth == "unknown" and device.gpu_type == "Discrete":
        pcie_bandwidth["PCIe bandwidth, GB/s (Max/Target)"].update({"RetVal": "ERROR"})
        pcie_bandwidth["PCIe bandwidth, GB/s (Max/Target)"].update(
            {"Message": "The Level Zero driver cannot find out information about PCIe bandwidth.",
             "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."}) # noqa E501
        device_metrics.update(pcie_bandwidth)
    elif device.pcie_bandwidth != "unknown" and device.gpu_type == "Discrete":
        device_metrics.update(pcie_bandwidth)
    else:
        pass

    value["Value"] = device_metrics
    json_node.update({f"#{device.enumeration} {device.name}": value})


def compare_metrics_for_known_device(json_node: Dict, device: Device) -> None:
    value = {"Value": "Undefined", "RetVal": "PASS"}
    device_metrics = {}

    frequency = {"GPU Frequency, MHz (Max/Target)": {
        "Value": f"{device.max_freq}/{known_devices[device.id]['freq']}", "RetVal": "PASS"}} # noqa
    if device.max_freq == "unknown":
        frequency["GPU Frequency, MHz (Max/Target)"].update({"RetVal": "ERROR"}) # noqa
        frequency["GPU Frequency, MHz (Max/Target)"].update(
            {"Message": "The Level Zero driver cannot find out information about frequency.", # noqa
            "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."}) # noqa E501
    elif float(device.max_freq) < float(known_devices[device.id]['freq']):
        frequency["GPU Frequency, MHz (Max/Target)"].update({"RetVal": "FAIL"})
        frequency["GPU Frequency, MHz (Max/Target)"].update(
            {"Message": "The maximum GPU frequency is less than the target bandwidth.", # noqa
            "HowToFix": f"The maximum GPU frequency: {device.max_freq}, should be equal or greater than " # noqa
                        f"the target value: {known_devices[device.id]['freq']}."}) # noqa
    device_metrics.update(frequency)

    mem_bandwidth = {"Memory bandwidth, GB/s (Max/Target)": {
        "Value": f"{device.mem_bandwidth}/{known_devices[device.id]['mem_bw']}", "RetVal": "PASS"}}
    if device.mem_bandwidth == "unknown":
        mem_bandwidth["Memory bandwidth, GB/s (Max/Target)"].update({"RetVal": "ERROR"})
        mem_bandwidth["Memory bandwidth, GB/s (Max/Target)"].update(
            {"Message": "The Level Zero driver cannot find out information about memory bandwidth.",
            "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."}) # noqa E501
    elif float(device.mem_bandwidth) < float(known_devices[device.id]['mem_bw']):
        mem_bandwidth["Memory bandwidth, GB/s (Max/Target)"].update({"RetVal": "FAIL"})
        mem_bandwidth["Memory bandwidth, GB/s (Max/Target)"].update(
            {"Message": "The maximum memory bandwidth is less than the target bandwidth.",
             "HowToFix": f"The maximum memory bandwidth: {device.mem_bandwidth}, should be equal or greater "
             f"than the target value: {known_devices[device.id]['mem_bw']}."})
    device_metrics.update(mem_bandwidth)

    pcie_bandwidth = {"PCIe bandwidth, GB/s (Max/Target)": {
        "Value": f"{device.pcie_bandwidth}/{known_devices[device.id]['pcie_bw']}", "RetVal": "PASS"}}
    if device.pcie_bandwidth == "unknown":
        pcie_bandwidth["PCIe bandwidth, GB/s (Max/Target)"].update({"RetVal": "ERROR"})
        pcie_bandwidth["PCIe bandwidth, GB/s (Max/Target)"].update(
            {"Message": "The Level Zero driver cannot find out information about PCIe bandwidth.",
             "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."}) # noqa
    elif float(device.pcie_bandwidth) < float(known_devices[device.id]['pcie_bw']):
        pcie_bandwidth["PCIe bandwidth, GB/s (Max/Target)"].update({"RetVal": "FAIL"})
        pcie_bandwidth["PCIe bandwidth, GB/s (Max/Target)"].update(
            {"Message": "The maximum PCIe bandwidth is less than the target bandwidth.",
             "HowToFix": f"The maximum PCIe bandwidth: {device.pcie_bandwidth}, should be equal or greater " # noqa E501
                         f"than the target value: {known_devices[device.id]['pcie_bw']}."})
    device_metrics.update(pcie_bandwidth)

    value["Value"] = device_metrics
    json_node.update({f"#{device.enumeration} {device.name}": value})


def process_device(json_node: Dict, device: Device) -> None:
    is_known_device = device.id in known_devices
    if is_known_device:
        compare_metrics_for_known_device(json_node, device)
    else:
        show_metrics_for_unknown_device(json_node, device)


def timeout_in_gpu_backend_check_occurred(data: Dict) -> bool:
    return data["gpu_backend_check"]["Value"] == "GPU"


def run_gpu_metrics_check(data: Dict) -> CheckSummary:
    result_json = {"Value": {}}

    try:
        have_administrative_priviliges()
        if timeout_in_gpu_backend_check_occurred(data):
            raise Exception("The GPU backend check failed or timed out. You may see irrelevant GPU "
                            "information as a result.")
        devices = parse_devices(data)
        if len(devices) == 0:
            raise Exception("Level Zero driver did not provide information about GPUs.")
        for device in devices:
            process_device(result_json["Value"], device)

    except PermissionError as error:
        result_json["Value"].update({
            "GPU metrics check": {
                "Value": "",
                "RetVal": "ERROR",
                "Message": str(error),
                "HowToFix": "Run depending checkers to diagnose the problem."}})   # noqa E501

    except Exception as error:
        result_json["Value"].update({
            "GPU metrics check": {
                "Value": "",
                "RetVal": "ERROR",
                "Message": str(error),
                "HowToFix": "Run gpu_backend_check to diagnose the problem."}})

    check_summary = CheckSummary(
        result=json.dumps(result_json, indent=4)
        )

    return check_summary


def get_api_version() -> str:
    return "0.1"


def get_check_list() -> List[CheckMetadataPy]:
    someCheck = CheckMetadataPy(
        name="gpu_metrics_check",
        type="Data",
        tags="gpu,runtime,target",
        descr="This check verifies that GPU metrics are good.",
        dataReq="{\"gpu_backend_check\": 1, \"intel_gpu_detector_check\": 1}",
        merit=40,
        timeout=5,
        version=1,
        run="run_gpu_metrics_check"
    )
    return [someCheck]
