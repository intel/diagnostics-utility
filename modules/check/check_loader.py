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

import logging

from pathlib import Path
from typing import List, Optional

from modules.check.check import BaseCheck
from modules.check.check_c import getChecksC
from modules.check.check_exe import getChecksExe
from modules.check.check_py import getChecksPy
from modules.check.sys_check import getSysChecks, search_sys_checks

from modules.files_helper import is_file_exist, read_config_data, get_files_list_from_folder
from modules.log import trace  # type: ignore


_FULL_PATH_TO_CURRENT_FILE = Path(__file__).resolve().parent
PATH_TO_DEFAULT_C_CHECKERS = _FULL_PATH_TO_CURRENT_FILE / ".." / ".." / "checkers_c"
PATH_TO_DEFAULT_EXE_CHECKERS = _FULL_PATH_TO_CURRENT_FILE / ".." / ".." / "checkers_exe"
PATH_TO_DEFAULT_PY_CHECKERS = _FULL_PATH_TO_CURRENT_FILE / ".." / ".." / "checkers_py"


@trace(log_args=True)
def load_checks_from_checker(checker_path: Path, check_name: Optional[str] = None) -> List[BaseCheck]:
    if not checker_path.exists():
        logging.warning(f"A module path does not exists: {checker_path}")
        return []
    if checker_path.suffix == ".so":
        return [check for check in getChecksC(checker_path)
                if check.get_metadata().name == check_name] \
            if check_name is not None else getChecksC(checker_path)
    elif checker_path.suffix == ".py" and not checker_path.name.startswith("__"):
        return [check for check in getChecksPy(checker_path)
                if check.get_metadata().name == check_name] \
            if check_name is not None else getChecksPy(checker_path)
    # TODO: Workaround until the sys_checks are rewritten
    # to the Diagnostics Utility for Intel® oneAPI Toolkits internal interface
    elif checker_path.name == "sys_check.sh":
        return [check for check in getSysChecks(checker_path)
                if check.get_metadata().name == check_name] \
            if check_name is not None else getSysChecks(checker_path)
    elif checker_path.suffix == ".sh":  # TODO: Add more executable types
        return [check for check in getChecksExe(checker_path)
                if check.get_metadata().name == check_name] \
            if check_name is not None else getChecksExe(checker_path)
    return []


@trace(log_args=True)
def load_checks(paths_list: List[Path], check_name: Optional[str] = None) -> List[BaseCheck]:
    checks = []
    for file in paths_list:
        checks.extend(load_checks_from_checker(file, check_name))
    return checks


@trace(log_args=True)
def load_single_checker(single_checker: Path) -> List[BaseCheck]:
    result: List[BaseCheck] = []
    try:
        is_file_exist(single_checker)
        result.extend(load_checks_from_checker(single_checker))
    except Exception as error:
        print(error)
        exit(1)
    return result


@trace(log_args=True)
def load_checks_from_config(config: Path) -> List[BaseCheck]:
    result: List[BaseCheck] = []
    try:
        config_data = read_config_data(config)
        for checker_data in config_data:
            check_name = checker_data["name"] if "name" in checker_data else None
            loaded_checks = load_checks_from_checker(Path(checker_data["path"]), check_name)
            if len(loaded_checks) == 0:
                raise ValueError(f"No checks were found from checker file: {checker_data['path']}")
            result.extend(loaded_checks)
    except Exception as error:
        print(error)
        exit(1)
    return result


@trace(log_args=True)
def load_default_checks() -> List[BaseCheck]:
    # TODO: customization of directories to search
    # TODO: recursive search
    result: List[BaseCheck] = []
    try:
        result.extend(load_checks(search_sys_checks()))
        result.extend(load_checks(get_files_list_from_folder(PATH_TO_DEFAULT_C_CHECKERS)))
        result.extend(load_checks(get_files_list_from_folder(PATH_TO_DEFAULT_PY_CHECKERS)))
        result.extend(load_checks(get_files_list_from_folder(PATH_TO_DEFAULT_EXE_CHECKERS)))
    except Exception as error:
        print(error)
        exit(1)
    return result
