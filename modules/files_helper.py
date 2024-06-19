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
import json
import platform

from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Set, Tuple

from modules.check import BaseCheck


def is_file_exist(path: Path) -> None:
    if path.exists():
        if not path.is_file():
            raise ValueError(f"{path} is not a file.")
    else:
        raise ValueError(f"{path} does not exist.")


def get_json_content_from_file(source: Path) -> Dict:
    is_file_exist(source)
    content = {}
    with open(source, mode="r") as file:
        try:
            content = json.load(file)
        except Exception:
            raise ValueError(f"{source} is not a JSON file.")
    return content


def read_config_data(source: Path) -> Dict:
    expexted_data_fileds = ["path", "name"]
    config_data = get_json_content_from_file(source)
    if not isinstance(config_data, list):
        raise ValueError("Configuration file has incorrect structure.")
    for checker_data in config_data:
        if not all(item in expexted_data_fileds for item in list(checker_data.keys())) or \
           not any(item == "name" for item in list(checker_data.keys())):
            raise ValueError("Configuration file has incorrect structure.")
    return config_data


def get_checkers_to_load_from_config_data(config_data: Dict) -> List[str]:
    result_checkers = []
    for checker_data in config_data:
        if "path" in checker_data:
            result_checkers.append(checker_data["path"])
    return result_checkers


def get_checks_to_run_from_config_data(config_data: Dict) -> Set[str]:
    result_checks = set()
    for checker_data in config_data:
        result_checks = result_checks | {checker_data["name"]}
    return result_checks


def get_files_list_from_folder(path_to_folder: Path) -> List[Path]:
    if path_to_folder.exists():
        return list(path_to_folder.iterdir())
    return []


def save_json_output_file(checks: List[BaseCheck], file: Path, print_json: bool) -> None:
    # Save results into log file
    # Need to save command line + results in json + result in text
    # Save into json file
    json_output = {}
    for check in checks:
        try:
            if check.get_summary() is None:
                continue
            json_output[check.get_metadata().name] = json.loads(check.get_summary().result)
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print("Decoding JSON has failed\n\n")
            continue
    if file:
        with open(file, 'w') as outfile:
            json.dump(json_output, outfile, indent=4)
    if print_json:
        print(json_output)


def _args_string(args) -> str:
    result = []
    if args.select != ["not_initialized"]:
        result.append("select")
    if args.list:
        result.append("list")
    if args.config:
        result.append("config")
    if args.force:
        result.append("force")
    if args.verbosity > -1:
        result.append("verbosity")
    return "_".join(result)


def configure_output_files(args) -> Tuple[Optional[Path], Optional[Path]]:
    txt_output_file = None
    json_output_file = None
    resolved_output = args.output.resolve()
    try:
        if resolved_output.exists():
            if not resolved_output.is_dir():
                raise ValueError(f"{resolved_output} is not a directory.")
            # NOTE: Workaround for non POSIX OSes because
            #       os.access(resolved_output, os.W_OK) always returns True
            test_file_name = f"test{datetime.now().strftime('%Y%m%d_%H%M%S%f')}.txt"
            test_file = resolved_output / test_file_name
            with open(test_file, "w") as test:
                test.write("test")
            test_file.unlink()
        else:
            resolved_output.mkdir(parents=True)
    except PermissionError:
        logging.warning("No permissions to create output files.")
    except Exception as error:
        logging.warning(str(error))
    else:
        txt_output_file_name = f"diagnostics_{_args_string(args)}_{platform.node()}_{datetime.now().strftime('%Y%m%d_%H%M%S%f')}.txt"  # noqa: E501
        json_output_file_name = f"diagnostics_{_args_string(args)}_{platform.node()}_{datetime.now().strftime('%Y%m%d_%H%M%S%f')}.json"  # noqa: E501
        txt_output_file = resolved_output / txt_output_file_name
        json_output_file = resolved_output / json_output_file_name

    return txt_output_file, json_output_file


def get_examine_data(source: Path) -> Optional[Dict]:
    result: Optional[Dict] = None
    try:
        result = get_json_content_from_file(source)
    except ValueError as error:
        logging.warning(f"Cannot get examine data: {str(error)}")
    return result
