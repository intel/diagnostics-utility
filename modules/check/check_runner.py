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
import json
import logging
import stat

from typing import Dict, List

from modules.check.check import BaseCheck, timeout_exit


def merge_dict(dst: Dict, to_merge: Dict) -> None:
    for k, v2 in to_merge.items():
        v1 = dst.get(k)
        if (isinstance(v1, dict) and isinstance(v2, dict)):
            merge_dict(v1, v2)
        else:
            if v1 is None:
                dst[k] = v2
            else:
                logging.debug(
                    "Destination dictionary contains information about check. Value will be overridden")
                dst[k] = v2


def get_sub_dict(data: Dict, to_get: Dict) -> int:
    if not bool(to_get):
        return 0
    err_num = 0
    for k, v2 in to_get.items():
        try:
            v1 = data.get('Value').get(k)
        except AttributeError:
            return err_num + 1
        if not bool(v2):
            to_get[k] = v1
        if (isinstance(v1, dict) and isinstance(v2, dict)):
            err_num += get_sub_dict(v1, v2)
        else:
            err_num += 1
    return err_num


def run_checks(checks: List[BaseCheck]) -> None:
    # TODO: Add more debug information
    json_full_results = {}
    to_run = len(checks)

    mode = stat.S_IWOTH | stat.S_IXOTH
    is_shm_available = os.stat("/dev/shm").st_mode & mode >= mode
    if not is_shm_available:
        logging.warning(
            "Other users doesn't have access to /dev/shm. "
            "Checks will be performed in the current process due "
            "to the impossibility of interprocess communication.")
    if to_run == 0:
        print("No checks found to run")
        exit(1)
    while to_run > 0:
        curr_run = to_run
        for check in checks:
            if check.get_summary() is None:
                metadata = check.get_metadata()
                if metadata.rights == "admin" and os.getuid() != 0:
                    logging.warning(
                        f"The check {metadata.name} needs root privileges. Please run with sudo.")
                    checks.remove(check)
                    to_run = to_run - 1
                    continue
                dataReqDict = json.loads(metadata.dataReq)
                if 0 == get_sub_dict(json_full_results, dataReqDict):
                    check_summary = timeout_exit(check.run)(check, dataReqDict) \
                        if is_shm_available else check.run(dataReqDict)
                    check.set_summary(check_summary)
                    merge_dict(json_full_results, json.loads(check.get_summary().result))
                    to_run = to_run - 1
        if curr_run - to_run == 0:
            print("The results of the required check dependencies were not received "
                  "before running the corresponding check.")
            exit(1)
