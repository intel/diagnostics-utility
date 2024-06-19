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
from typing import List, Dict, Tuple


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


def run_gpu_metrics_check(data: Dict) -> CheckSummary:
    result_json = {"CheckResult": {}}

    try:
        if timeout_in_gpu_backend_check_occurred(data):
            raise Exception("The GPU backend check failed or timed out. You may see irrelevant GPU "
                            "information as a result.")
        devices = parse_devices(data)
        if len(devices) == 0:
            raise Exception("Intel® oneAPI Level Zero driver did not provide information about GPUs.")
        for device in devices:
            process_device(result_json["CheckResult"], device)

    except PermissionError as error:
        result_json["CheckResult"].update({
            "GPU metrics check": {
                "CheckResult": "",
                "CheckStatus": "ERROR",
                "Message": str(error),
                "HowToFix": "Run depending checkers to diagnose the problem."}})   # noqa E501

    except Exception as error:
        result_json["CheckResult"].update({
            "GPU metrics check": {
                "CheckResult": "",
                "CheckStatus": "ERROR",
                "Message": str(error),
                "HowToFix": "Run gpu_backend_check to diagnose the problem."}})

    check_summary = CheckSummary(
        result=json.dumps(result_json, indent=4)
    )

    return check_summary


def parse_devices(data: Dict) -> List[Device]:
    result: List[Device] = []

    is_lz_initialized, lz_driver_message = is_level_zero_initialized(data)
    if not is_lz_initialized:
        raise Exception(lz_driver_message)
    lz_slice = data["gpu_backend_check"]["CheckResult"]["GPU"]["CheckResult"]["Intel® oneAPI Level Zero Driver"]["CheckResult"]["Driver information"]["CheckResult"]  # noqa: E501

    if not isinstance(lz_slice, dict):
        return result
    driver_number = int(lz_slice["Installed driver number"]["CheckResult"])

    counter = 0
    for i in range(driver_number):
        devices_slice = lz_slice[f"Driver # {i}"]["CheckResult"]["Devices"]
        device_number = int(devices_slice["CheckResult"]["Device number"]["CheckResult"])
        for j in range(device_number):
            device_slice = devices_slice["CheckResult"][f"Device # {j}"]["CheckResult"]
            device_type = device_slice["Device type"]["CheckResult"]
            if device_type != "Graphics Processing Unit":
                continue
            lz_id = device_slice["Device ID"]["CheckResult"]
            device_type = get_device_type(lz_id, data["intel_gpu_detector_check"])
            if device_type is None:
                continue
            device = Device(
                name=device_slice["Device name"]["CheckResult"],
                id=lz_id,
                max_freq=device_slice["Device maximum frequency, MHz"]["CheckResult"],
                min_freq=device_slice["Device minimum frequency, MHz"]["CheckResult"],
                cur_freq=device_slice["Device current frequency, MHz"]["CheckResult"],
                mem_bandwidth=device_slice["Memory bandwidth, GB/s"]["CheckResult"],
                pcie_bandwidth=device_slice["PCIe bandwidth, GB/s"]["CheckResult"],
                gpu_type=device_type,
                enumeration=str(counter)
            )
            counter += 1
            result.append(device)
    return result


def get_device_type(level_zero_id, intel_gpu_detector_data) -> str:
    data_slice = intel_gpu_detector_data["CheckResult"]["GPU information"]["CheckResult"]  # noqa: E501
    for key, value in data_slice.items():
        pci_id = value["CheckResult"]["PCI ID"]["CheckResult"].lower()
        if level_zero_id[2:] == pci_id:
            return value["CheckResult"]["GPU type"]["CheckResult"]


def is_level_zero_initialized(data: Dict) -> Tuple[bool, str]:
    lz_driver_message = ''
    lz_driver_loaded_check_status = data["gpu_backend_check"]["CheckResult"]["GPU"]["CheckResult"]["Intel® oneAPI Level Zero Driver"]["CheckResult"]["Driver is loaded."]["CheckStatus"]  # noqa: E501
    if lz_driver_loaded_check_status == "ERROR":
        lz_driver_message = data["gpu_backend_check"]["CheckResult"]["GPU"]["CheckResult"]["Intel® oneAPI Level Zero Driver"]["CheckResult"]["Driver is loaded."]["Message"]  # noqa: E501
    else:
        lz_driver_info_check_status = data["gpu_backend_check"]["CheckResult"]["GPU"]["CheckResult"]["Intel® oneAPI Level Zero Driver"]["CheckResult"]["Driver information"]["CheckStatus"]  # noqa: E501
        if lz_driver_info_check_status == "ERROR":
            lz_driver_message = data["gpu_backend_check"]["CheckResult"]["GPU"]["CheckResult"]["Intel® oneAPI Level Zero Driver"]["CheckResult"]["Driver information"]["Message"]  # noqa: E501

    is_level_zero_initialized = lz_driver_loaded_check_status == "PASS" and lz_driver_info_check_status == "INFO"  # noqa: E501

    return is_level_zero_initialized, lz_driver_message


def process_device(json_node: Dict, device: Device) -> None:
    check_result = {
        "CheckResult": "Undefined",
        "CheckStatus": "WARNING",
        "Message": "For this GPU, values are not known."
    }

    is_known_device = device.id in known_devices

    frequency = get_max_freq_from_l0(device, is_known_device)
    mem_bandwidth = get_mem_bandwidth_from_l0(device, is_known_device)
    pcie_bandwidth = get_pcie_bandwidth_from_l0(device, is_known_device)
    device_metrics = {}

    device_metrics.update(frequency)
    if device.gpu_type == "Discrete":
        device_metrics.update(mem_bandwidth)
        device_metrics.update(pcie_bandwidth)

    check_result["CheckResult"] = device_metrics
    json_node.update({f"#{device.enumeration} {device.name} {device.id}": check_result})


def get_max_freq_from_l0(device: Device, is_known_device: bool) -> Dict:
    if is_known_device:
        frequency = {"GPU Frequency, MHz (Max/Target)": {
            "CheckResult": f"{device.max_freq}/{known_devices[device.id]['freq']}",
            "CheckStatus": "PASS"}}  # noqa
        if device.max_freq == "unknown":
            frequency["GPU Frequency, MHz (Max/Target)"].update({"CheckStatus": "ERROR"})  # noqa
            frequency["GPU Frequency, MHz (Max/Target)"].update(
                {"Message": "Intel® oneAPI Level Zero driver cannot provide information about frequency.",  # noqa
                "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for oneAPI repository: https://github.com/intel/diagnostics-utility."})  # noqa E501
        elif float(device.max_freq) < float(known_devices[device.id]['freq']):
            frequency["GPU Frequency, MHz (Max/Target)"].update({"CheckStatus": "FAIL"})
            frequency["GPU Frequency, MHz (Max/Target)"].update(
                {"Message": "The maximum GPU frequency is less than the target bandwidth.",  # noqa
                "HowToFix": f"The maximum GPU frequency: {device.max_freq}, should be equal or greater than "  # noqa
                            f"the target value: {known_devices[device.id]['freq']}."})  # noqa
    else:
        frequency = {"GPU Frequency, MHz (Max/Target)": {
            "CheckResult": f"{device.max_freq}/unknown",
            "CheckStatus": "INFO"}}
        if device.max_freq == "unknown" and device.gpu_type == "Discrete":
            frequency["GPU Frequency, MHz (Max/Target)"].update({"CheckStatus": "ERROR"})
            frequency["GPU Frequency, MHz (Max/Target)"].update(
                {"Message": "Intel® oneAPI Level Zero driver cannot provide information about frequency.",
                "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for oneAPI repository: https://github.com/intel/diagnostics-utility."})  # noqa E501)
    return frequency


def get_mem_bandwidth_from_l0(device: Device, is_known_device: bool) -> Dict:
    if is_known_device:
        mem_bandwidth = {"Memory bandwidth, GB/s (Max/Target)": {
            "CheckResult": f"{device.mem_bandwidth}/{known_devices[device.id]['mem_bw']}", "CheckStatus": "PASS"}}  # noqa E501
        if device.mem_bandwidth == "unknown":
            mem_bandwidth["Memory bandwidth, GB/s (Max/Target)"].update({"CheckStatus": "ERROR"})
            mem_bandwidth["Memory bandwidth, GB/s (Max/Target)"].update(
                {"Message": "Intel® oneAPI Level Zero driver cannot provide information about memory bandwidth.",  # noqa E501
                "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for oneAPI repository: https://github.com/intel/diagnostics-utility."})  # noqa E501
        elif float(device.mem_bandwidth) < float(known_devices[device.id]['mem_bw']):
            mem_bandwidth["Memory bandwidth, GB/s (Max/Target)"].update({"CheckStatus": "FAIL"})
            mem_bandwidth["Memory bandwidth, GB/s (Max/Target)"].update(
                {"Message": "The maximum memory bandwidth is less than the target bandwidth.",
                 "HowToFix": f"The maximum memory bandwidth: {device.mem_bandwidth}, should be equal or greater "  # noqa E501
                 f"than the target value: {known_devices[device.id]['mem_bw']}."})
    else:
        mem_bandwidth = {
            "Memory bandwidth, GB/s (Max/Target)":
            {"CheckResult": f"{device.mem_bandwidth}/unknown",
             "CheckStatus": "INFO"}}
        if device.mem_bandwidth == "unknown" and device.gpu_type == "Discrete":
            mem_bandwidth["Memory bandwidth, GB/s (Max/Target)"].update({"CheckStatus": "ERROR"})
            mem_bandwidth["Memory bandwidth, GB/s (Max/Target)"].update(
                {"Message": "Intel® oneAPI Level Zero driver cannot provide information about memory bandwidth.",  # noqa E501
                "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for oneAPI repository: https://github.com/intel/diagnostics-utility."})  # noqa E501
    return mem_bandwidth


def get_pcie_bandwidth_from_l0(device: Device, is_known_device: bool) -> Dict:
    if is_known_device:
        pcie_bandwidth = {"PCIe bandwidth, GB/s (Max/Target)": {
            "CheckResult": f"{device.pcie_bandwidth}/{known_devices[device.id]['pcie_bw']}", "CheckStatus": "PASS"}}  # noqa: E501
        if device.pcie_bandwidth == "unknown":
            pcie_bandwidth["PCIe bandwidth, GB/s (Max/Target)"].update({"CheckStatus": "ERROR"})
            pcie_bandwidth["PCIe bandwidth, GB/s (Max/Target)"].update(
                {"Message": "Intel® oneAPI Level Zero driver cannot provide information about PCIe bandwidth.",  # noqa E501
                "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for oneAPI repository: https://github.com/intel/diagnostics-utility."})  # noqa
        elif float(device.pcie_bandwidth) < float(known_devices[device.id]['pcie_bw']):
            pcie_bandwidth["PCIe bandwidth, GB/s (Max/Target)"].update({"CheckStatus": "FAIL"})
            pcie_bandwidth["PCIe bandwidth, GB/s (Max/Target)"].update(
                {"Message": "The maximum PCIe bandwidth is less than the target bandwidth.",
                "HowToFix": f"The maximum PCIe bandwidth: {device.pcie_bandwidth}, should be equal or greater "  # noqa E501
                            f"than the target value: {known_devices[device.id]['pcie_bw']}."})
    else:
        pcie_bandwidth = {
            "PCIe bandwidth, GB/s (Max/Target)":
            {"CheckResult": f"{device.pcie_bandwidth}/unknown",
             "CheckStatus": "INFO"}}
        if device.pcie_bandwidth == "unknown" and device.gpu_type == "Discrete":
            pcie_bandwidth["PCIe bandwidth, GB/s (Max/Target)"].update({"CheckStatus": "ERROR"})
            pcie_bandwidth["PCIe bandwidth, GB/s (Max/Target)"].update(
                {"Message": "Intel® oneAPI Level Zero driver cannot provide information about PCIe bandwidth.",  # noqa E501
                "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for oneAPI repository: https://github.com/intel/diagnostics-utility."})  # noqa E501
    return pcie_bandwidth


def timeout_in_gpu_backend_check_occurred(data: Dict) -> bool:
    return data["gpu_backend_check"]["CheckResult"] == "GPU"


def get_api_version() -> str:
    return "0.2"


def get_check_list() -> List[CheckMetadataPy]:
    someCheck = CheckMetadataPy(
        name="gpu_metrics_check",
        type="Data",
        groups="gpu,runtime,target",
        descr="This check verifies that GPU metrics' results are satisfactory.",
        dataReq="{\"gpu_backend_check\": 2, \"intel_gpu_detector_check\": 2}",
        merit=40,
        timeout=10,
        version=2,
        run="run_gpu_metrics_check"
    )
    return [someCheck]
