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
import subprocess
from typing import Dict

LINUX = "Linux"
WINDOWS = "Windows"


def get_OS() -> str:
    return platform.uname().system


def check_perf_stream_paranoid(json_node: Dict) -> None:
    value = {"Value": "Undefined", "RetVal": "PASS", "Command": "sysctl -n dev.i915.perf_stream_paranoid"}
    try:
        proc = subprocess.Popen(
            ['sysctl', '-n', 'dev.i915.perf_stream_paranoid'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        stdout, _ = proc.communicate()
        if proc.returncode != 0:
            raise Exception("Cannot get information about operating sysctl option")
        value["Value"] = stdout.splitlines()[0]
        if stdout.splitlines()[0] == '1':
            value["RetVal"] = "FAIL"
            value["Message"] = "Set the value of the dev.i915.perf_stream_paranoid sysctl option to 0."
    except Exception as error:
        value["RetVal"] = "ERROR"
        value["Message"] = str(error)
    json_node.update({"Perf stream paranoid": value})
