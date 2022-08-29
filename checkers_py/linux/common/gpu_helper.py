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
import re
from pathlib import Path
from typing import Dict, List


def get_card_devices() -> List[Path]:
    path_to_devices = Path("/dev/dri/")
    result = []
    if path_to_devices.exists():
        card_pattern = re.compile(r"card[0-9]+")
        result = [path_to_devices / file for file in os.listdir(path_to_devices)
                  if card_pattern.fullmatch(file)]
    return result


def get_render_devices() -> List[Path]:
    path_to_devices = Path("/dev/dri/")
    result = []
    if path_to_devices.exists():
        render_pattern = re.compile(r"renderD[0-9]+")
        result = [path_to_devices / file for file in os.listdir(path_to_devices)
                  if render_pattern.fullmatch(file)]
    return result


def are_intel_gpus_found(data: Dict) -> bool:
    intel_gpu_slice = data["intel_gpu_detector_check"]["Value"]["GPU information"]["Value"]["Intel GPU(s) is present on the bus"]  # noqa: E501
    is_intel_gpu_found = intel_gpu_slice["RetVal"] == "PASS"
    return is_intel_gpu_found


def intel_gpus_not_found_handler(json_node: Dict) -> None:
    json_node.update({
        "Warning message": {
            "Value": "",
            "RetVal": "WARNING",
            "Message": "The checker might show irrelevant information for your system because "
                       "the intel_gpu_detector_check failed."
        }
    })
