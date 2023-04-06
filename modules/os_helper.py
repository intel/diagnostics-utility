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

import platform
from typing import Dict, List, Tuple


SUPPORTED_OS: Dict[str, List[str]] = {
    "Ubuntu": ["20.04", "22.04"],
    "Red Hat Enterprise Linux": ["8.2", "8.3", "9.0"],
    "SLES": ["15.2", "15.3", "15.4"],
    "SLED": ["15.2", "15.3", "15.4"],
    "Windows": ["10", "11", "Server 2022"],
    "Rocky Linux": ["8.5", "9.0"]
}


def _get_windows_version() -> str:  # pragma: no cover
    import winreg  # pylint: disable=E0401
    product_name_reg_key = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, product_name_reg_key) as key:
        product_name = winreg.QueryValueEx(key, "ProductName")[0].split(" ")
    version = " ".join(product_name[1:-1])
    return version


def _get_linux_distribution() -> Tuple[str, str]:
    os_release_path = "/etc/os-release"
    with open(os_release_path, "r") as file:
        os_release = file.readlines()
    name = [line.strip().split("=")[1][1:-1] for line in os_release if line.startswith("NAME")][0]
    version = [line.strip().split("=")[1][1:-1] for line in os_release if line.startswith("VERSION_ID")][0]
    return name, version


def _get_os() -> Tuple[str, str]:
    os_name = platform.system()
    if os_name == "Windows":
        name, version = os_name, _get_windows_version()
    elif os_name == "Linux":
        name, version = _get_linux_distribution()
    else:
        raise Exception("The operating system is not supported.")
    return name, version


def is_os_supported() -> bool:
    result = False
    try:
        name, version = _get_os()
        if name in SUPPORTED_OS and version in SUPPORTED_OS[name]:
            result = True
    except Exception:
        result = False
    return result


def check_that_os_is_supported() -> None:
    if not is_os_supported():
        print("Your operating system is not supported by the Diagnostics Utility\n"
              "for Intel® oneAPI Toolkits. You can force the program to run using the --force flag.")
        exit(1)
