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
from typing import List, Set

from modules.check import BaseCheck


def process_select(selection: List[str]) -> Set[str]:
    """Set default select if select has not been initialized."""
    result = set(selection)
    if len(selection) == 1 and selection[0] == "not_initialized":
        result = {"default"}
    return result


def get_selected_checks(checks: List[BaseCheck], selection: List[str]) -> List[BaseCheck]:
    if "all" in selection:
        return checks
    return list(filterfalse(
        lambda x: not list(
            set(selection) &
            (set(x.get_metadata().groups.split(",")) | set([x.get_metadata().name]))),
        checks
    ))
