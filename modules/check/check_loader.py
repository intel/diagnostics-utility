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
import os
import platform

from pathlib import Path
from typing import List, Dict

from modules.check.check import BaseCheck, CheckMetadataPy
from modules.check.check_c import getChecksC
from modules.check.check_exe import getChecksExe
from modules.check.check_py import getChecksPy

from modules.files_helper import read_config_data, get_checkers_to_load_from_config_data, \
                                    get_files_list_from_folder
from modules.log import trace  # type: ignore


_FULL_PATH_TO_CURRENT_FILE = Path(__file__).resolve().parent
DEFAULT_CHECKERS_PATHS = [
    _FULL_PATH_TO_CURRENT_FILE / ".." / ".." / "checkers_c",
    _FULL_PATH_TO_CURRENT_FILE / ".." / ".." / "checkers_exe",
    _FULL_PATH_TO_CURRENT_FILE / ".." / ".." / "checkers_py",
    _FULL_PATH_TO_CURRENT_FILE / ".." / ".." / "checkers_c" / platform.system().lower(),
    _FULL_PATH_TO_CURRENT_FILE / ".." / ".." / "checkers_exe" / platform.system().lower(),
    _FULL_PATH_TO_CURRENT_FILE / ".." / ".." / "checkers_py" / platform.system().lower()
]


@trace(log_args=True)
def load_checks_from_checker(
        checker_path: Path, version: str, loaded_checks_map: Dict[Path, CheckMetadataPy]) -> List[BaseCheck]:
    check_list = []
    if not checker_path.exists():
        logging.warning(f"Checker not found at this path: {checker_path}.")
        return check_list
    if checker_path.suffix == ".so" or checker_path.suffix == ".dll":
        check_list = getChecksC(checker_path, version)
    elif checker_path.suffix == ".py" and not checker_path.name.startswith("__"):
        check_list = getChecksPy(checker_path, version)
    elif checker_path.suffix == ".sh":
        if not os.access(checker_path, os.X_OK):
            logging.warning(f"A checker does not have execute permissions: {checker_path}.")
            return check_list
        check_list = getChecksExe(checker_path, version)
    elif checker_path.suffix == ".bat":  # TODO: Add more executable types
        check_list = getChecksExe(checker_path, version)
    loaded_checks_map.update({checker_path: check.get_metadata() for check in check_list})
    return check_list


@trace(log_args=True)
def load_checks(
        paths: List[Path], version: str, loaded_checks_map: Dict[Path, CheckMetadataPy]) -> List[BaseCheck]:
    checks = []
    for file in paths:
        checks.extend(load_checks_from_checker(file, version, loaded_checks_map))
    return checks


@trace(log_args=True)
def load_checks_from_config(
        config: Path, version: str, loaded_checks_map: Dict[Path, CheckMetadataPy]) -> List[BaseCheck]:
    result: List[BaseCheck] = []
    try:
        config_data = read_config_data(config)
        checkers_to_load = get_checkers_to_load_from_config_data(config_data)
        for checker in checkers_to_load:
            loaded_checks = load_checks_from_checker(Path(checker), version, loaded_checks_map)
            if len(loaded_checks) == 0:
                raise ValueError(f"No checks were found from checker file: {checker}")
            result.extend(loaded_checks)
    except Exception as error:
        print(error)
        exit(1)
    return result


@trace(log_args=True)
def load_default_checks(
        version: str, loaded_checks_map: Dict[Path, CheckMetadataPy]) -> List[BaseCheck]:
    # TODO: customization of directories to search
    # TODO: recursive search
    result: List[BaseCheck] = []
    try:
        for path in DEFAULT_CHECKERS_PATHS:
            result.extend(load_checks(
                get_files_list_from_folder(path),
                version,
                loaded_checks_map
            ))
    except Exception as error:
        print(error)
        exit(1)
    return result


@trace(log_args=True)
def load_checks_from_env(
        version: str, loaded_checks_map: Dict[Path, CheckMetadataPy]) -> List[BaseCheck]:
    result: List[BaseCheck] = []
    try:
        DIAGUTIL_PATH_ENV = os.getenv("DIAGUTIL_PATH")
        sep = ";" if platform.system() == "Windows" else ":"
        env_paths = DIAGUTIL_PATH_ENV.split(sep=sep) if DIAGUTIL_PATH_ENV else []
        for str_path in env_paths:
            if not str_path:
                continue
            path = Path(str_path)
            if not path.exists():
                raise ValueError(f"{path} does not exist.")
            if path.is_dir():
                result.extend(load_checks(get_files_list_from_folder(path), version, loaded_checks_map))
            elif path.is_file():
                result.extend(load_checks_from_checker(path, version, loaded_checks_map))
            else:
                raise ValueError(f"{path} is not a file or directory.")
    except Exception as error:
        print(error)
        exit(1)
    return result
