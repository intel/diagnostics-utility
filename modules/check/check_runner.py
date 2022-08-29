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

import json
import logging

from typing import Dict, List, Set, Tuple
from multiprocessing import Process, Pipe

from modules.check.check import BaseCheck, CheckSummary


def _check_run(connection, check, data) -> None:
    try:
        result = check.run(data)
        connection.send(result)
    except Exception as e:
        connection.send(e)
    finally:
        connection.close


def check_run(check, data) -> CheckSummary:
    parent_connection, child_connection = Pipe(duplex=False)
    process = Process(target=_check_run, args=(child_connection, check, data))
    process.start()
    if parent_connection.poll(timeout=check.get_metadata().timeout):
        result = parent_connection.recv()
        if isinstance(result, Exception):
            json_dict = {
                "RetVal": "ERROR",
                "Verbosity": 0,
                "Message": "",
                "Value": {
                    f"{check.get_metadata().name}": {
                        "Value": "",
                        "Verbosity": 0,
                        "Message": "The check crashed at runtime. No data was received. "
                                   "See call stack above.",
                        "RetVal": "ERROR"
                    }
                }
            }
            json_str = json.dumps(json_dict)
            result = CheckSummary(result=json_str)
        parent_connection.close()
    else:
        process.terminate()
        json_dict = {
            "RetVal": "ERROR",
            "Verbosity": 0,
            "Message": "",
            "Value": {
                f"{check.get_metadata().name}": {
                    "Value": "Timeout was exceeded.",
                    "Verbosity": 0,
                    "Message": "",
                    "RetVal": "ERROR"
                }
            }
        }
        json_str = json.dumps(json_dict)
        result = CheckSummary(result=json_str)
    return result


def _get_dependency_checks_map(checks: List[BaseCheck], dataReq: Dict) -> Dict[str, BaseCheck]:
    required_dependencies_map: Dict[str, BaseCheck] = {}
    for name, version in dataReq.items():
        is_found = False
        for check in checks:
            metadata = check.get_metadata()
            if metadata.name == name:
                if metadata.version == version:
                    required_dependencies_map.update({name: check})
                    is_found = True
                    break
                else:
                    logging.error(f"Another version of the required dependency {name} is loaded.")
            else:
                continue
        if not is_found:
            logging.error(f"Cannot find the {name} in the loaded list of checks.")
    return required_dependencies_map


def create_dependency_order(
        loaded_checks: List[BaseCheck], filter: Set[str]) -> Tuple[List[str], List[BaseCheck]]:
    checks_to_print: List[str] = []
    ordered_checks_map: Dict[str, BaseCheck] = {}
    for check in loaded_checks:
        check_metadata = check.get_metadata()
        if "all" not in filter and \
           len((set(check_metadata.tags.split(",")) | {check_metadata.name}) & filter) == 0:
            continue
        checks_to_print.append(check_metadata.name)
        dependency_checks = _get_dependency_checks_map(loaded_checks, json.loads(check_metadata.dataReq))
        for name, dependency in dependency_checks.items():
            if name not in ordered_checks_map:
                ordered_checks_map[name] = dependency

        if check_metadata.name not in ordered_checks_map:
            ordered_checks_map[check_metadata.name] = check

    return checks_to_print, list(ordered_checks_map.values())


def run_checks(checks_to_run: List[BaseCheck]) -> None:
    # TODO: Add more debug information
    json_full_results = {}
    if len(checks_to_run) == 0:
        print("No checks found to run.")
        exit(1)

    for check in checks_to_run:
        metadata = check.get_metadata()
        required_dependencies = json.loads(metadata.dataReq)
        required_dependencies_data = {
            check_name: summary
            for check_name, summary in json_full_results.items()
            if check_name in required_dependencies.keys()
        }
        if len(required_dependencies) != len(required_dependencies_data):
            logging.error(f"The {metadata.name} depends on results of other checks that cannot be obtained. "
                          f"Please load checks with names: {','.join(list(required_dependencies.keys()))}.")
            continue
        check_summary = check_run(check, required_dependencies_data)
        check.set_summary(check_summary)
        json_full_results[check.get_metadata().name] = json.loads(check.get_summary().result)
