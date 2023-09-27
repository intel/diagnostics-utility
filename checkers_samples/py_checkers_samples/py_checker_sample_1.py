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


def run_checker1(data: dict) -> CheckSummary:
    check_summary = CheckSummary(
        result=json.dumps({
            "CheckResult": {
                "Python sample check 1": {
                    "CheckResult": "Python sample value 1",
                    "CheckStatus": "PASS"
                }
            }})
    )

    return check_summary


def get_api_version() -> str:
    return "0.2"


def get_check_list() -> List[CheckMetadataPy]:
    someCheck = CheckMetadataPy(
        name="py_check_sample_1",
        type="Data",
        groups="sample,python",
        descr="This is a description of python check sample #1.",
        dataReq="{}",
        merit=0,
        timeout=5,
        version=2,
        run="run_checker1"
    )
    return [someCheck]
