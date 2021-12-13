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

from itertools import filterfalse
from typing import List

from modules.check import BaseCheck


def process_filter(filter: List[str]) -> List[str]:
    """Set default filter if filter has not been initialized"""
    result = filter
    if len(filter) == 1 and filter[0] == "not_initialized":
        result = ["default"]
    return result


def get_filtered_checks(checks: List[BaseCheck], filter: List[str]) -> List[BaseCheck]:
    if "all" in filter:
        return checks
    return list(filterfalse(
        lambda x: not list(
            set(filter) &
            (set(x.get_metadata().tags.split(",")) | set([x.get_metadata().name]))),
        checks
    ))
