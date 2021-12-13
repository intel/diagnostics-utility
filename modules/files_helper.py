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
import logging
import json
import platform

from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple

from modules.check import BaseCheck


def is_file_exist(path: Path) -> None:
    if path.exists():
        if not path.is_file():
            raise ValueError(f"{path} is not a file")
    else:
        raise ValueError(f"{path} doesn't exist")


def get_json_content_from_file(source: Path) -> Dict:
    is_file_exist(source)
    content = {}
    with open(source, mode="r") as file:
        try:
            content = json.load(file)
        except Exception:
            raise ValueError(f"{source} is not json file")
    return content


def read_config_data(source: Path) -> Dict:
    config_data = get_json_content_from_file(source)
    if not isinstance(config_data, list):
        raise ValueError("Configuration file has incorrect structure")
    for checker_data in config_data:
        if "path" not in checker_data:
            raise ValueError("Configuration file has incorrect structure")
    return config_data


def get_files_list_from_folder(path_to_folder: Path) -> List[Path]:
    if path_to_folder.exists():
        return list(path_to_folder.iterdir())
    return []


def save_json_output_file(checks: List[BaseCheck], file: Path) -> None:
    # Save results into log file
    # Need to save command line + results in json + result in text
    # Save into json file
    json_output = {}
    for check in checks:
        try:
            json_output[check.get_metadata().name] = json.loads(check.get_summary().result)
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print("Decoding JSON has failed\n\n")
            continue
    with open(file, 'w') as outfile:
        json.dump(json_output, outfile, indent=4)


def _args_string(args) -> str:
    result = []
    if args.filter != ["not_initialized"]:
        result.append(f"filter_{'_'.join(args.filter)}")
    if args.list:
        result.append("list")
    if args.config:
        result.append(f"config_{args.config.stem}")
    if args.single_checker:
        result.append(f"single_checker_{args.single_checker.stem}")
    if args.force:
        result.append("force")
    if args.verbosity > -1:
        result.append(f"verbosity_{args.verbosity}")
    return "_".join(result)


def configure_output_files(args) -> Tuple[Optional[Path], Optional[Path]]:
    txt_output_file = None
    json_output_file = None
    try:
        if args.output.exists():
            if not args.output.is_dir():
                raise ValueError(f"{args.output} is not a directory.")
            if not os.access(args.output, os.W_OK):
                raise ValueError("Output folder has no write permissions.")
        else:
            args.output.mkdir(parents=True)
    except PermissionError:
        logging.warning("No permissions to create output folder")
    except Exception as error:
        logging.warning(str(error))
    else:
        txt_output_file_name = f"diagnostics_{_args_string(args)}_{platform.node()}_{datetime.now().strftime('%Y%m%d_%H%M%S%f')}.txt"  # noqa: E501
        json_output_file_name = f"diagnostics_{_args_string(args)}_{platform.node()}_{datetime.now().strftime('%Y%m%d_%H%M%S%f')}.json"  # noqa: E501
        txt_output_file = args.output / txt_output_file_name
        json_output_file = args.output / json_output_file_name

    return txt_output_file, json_output_file


def get_examine_data(source: Path) -> Optional[Dict]:
    result: Optional[Dict] = None
    try:
        result = get_json_content_from_file(source)
    except ValueError as error:
        logging.warning(f"Can't get examine data: {str(error)}")
    return result
