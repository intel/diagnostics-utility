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

import os.path

import platform
import shutil
from typing import Dict


def get_gdb_base_dir():
    gdb_bin_path = shutil.which("gdb-oneapi")
    if gdb_bin_path:
        gdb_bin_dir = os.path.dirname(gdb_bin_path)
        return os.path.dirname(gdb_bin_dir)
    return None


def get_OS() -> str:
    return platform.uname().system


def check_file_in_gdb_dir(json_node: Dict, rel_path: str, component_name: str) -> None:
    value = {"Value": "Undefined", "RetVal": "PASS"}
    try:
        gdb_base_dir = get_gdb_base_dir()
        if gdb_base_dir and os.path.exists(os.path.join(gdb_base_dir, rel_path)):
            value["Message"] = f"{component_name} found"
            value["RetVal"] = "PASS"
        else:
            value["Message"] = f"{component_name} not found"
            value["RetVal"] = "FAIL"
    except Exception as error:
        value["RetVal"] = "ERROR"
        value["Message"] = f"Error while searching {component_name}: {error}"
    json_node.update({f"{component_name} exist": value})


def check_gdb_exist(json_node: Dict) -> None:
    check_file_in_gdb_dir(json_node, os.path.join("bin", "gdb-oneapi"), "Debugger")


def check_libipt_exist(json_node: Dict) -> None:
    check_file_in_gdb_dir(json_node, os.path.join("lib", "libipt.so"), "libipt")


def check_libiga_exist(json_node: Dict) -> None:
    check_file_in_gdb_dir(json_node, os.path.join("lib", "libiga64.so"), "libiga")
