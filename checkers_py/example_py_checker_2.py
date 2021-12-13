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
from typing import List


def run_checker2(data: dict) -> CheckSummary:
    # #We can check that we have required data
    check_summary = CheckSummary(
        result=json.dumps({
            "Value": {
                "Python example check 2": {
                    "RetVal": "PASS",
                    "Value": {
                        "Python example subcheck 1": {
                            "Value": "Python example value 1",
                            "RetVal": "PASS"
                        },
                        "Python example subcheck 2": {
                            "Value": "Python example value 2",
                            "RetVal": "PASS"
                        }
                    }
                }
            }})
    )

    return check_summary


def get_api_version() -> str:
    return "0.1"


def get_check_list() -> List[CheckMetadataPy]:
    someCheck = CheckMetadataPy(
        name="example_py_checker_2",
        type="Data",
        tags="example,python",
        descr="It is a description for #2.",
        dataReq="{\"GPU (OpenCL™ Vendors)\": {\"Intel\": {},\"AMD\": {}}}",
        rights="user",
        timeout=5,
        version="0.1",
        run="run_checker2"
    )
    return [someCheck]
