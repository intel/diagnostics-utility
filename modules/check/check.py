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

from functools import wraps
from typing import Callable, Dict, Optional


def _result_summary_recursive(summary_value: Dict, is_root: bool = False) -> int:
    result_error_code = 0
    for _, data in summary_value.items():
        subcheck_error_code = 0
        if "RetVal" in data:
            if data["RetVal"] not in ["PASS", "WARNING", "FAIL", "ERROR", "INFO"]:
                raise ValueError(
                    f"Error in subtree: {data}. RetVal value can be only PASS, WARNING, FAIL, ERROR, INFO")
            elif data["RetVal"] == "WARNING":
                subcheck_error_code = 1
            elif data["RetVal"] == "FAIL":
                subcheck_error_code = 2
            elif data["RetVal"] == "ERROR":
                subcheck_error_code = 3
        else:
            raise ValueError(f"Error in subtree: {data}. RetVal is required.")

        if "Verbosity" in data:
            if not isinstance(data["Verbosity"], int):
                raise ValueError(
                    f"Error in subtree: {data}. Verbosity must be an integer.")
            if is_root:
                if 0 < data["Verbosity"]:
                    raise ValueError(
                        f"Error in subtree: {data}. Root verbosity level must be set to zero.")
        if "Message" in data:
            if not isinstance(data["Message"], str):
                raise ValueError(
                    f"Error in subtree: {data}. Message must be a string.")
        if "Command" in data:
            if not isinstance(data["Command"], str):
                raise ValueError(
                    f"Error in subtree: {data}. Command must be a string.")
        if "Value" in data:
            if isinstance(data["Value"], dict):
                subcheck_error_code = max(
                    subcheck_error_code,
                    _result_summary_recursive(data["Value"])
                )
        else:
            raise ValueError(f"Error in subtree: {data}. Value is required.")
        result_error_code = max(
            result_error_code,
            subcheck_error_code
        )
    return result_error_code


def _result_summary_is_correct(
        summary: Dict) -> int:
    if len(summary) == 0:
        raise ValueError("Value dictionary cannot be empty.")
    if "Value" not in summary:
        raise ValueError("Result summary is not correct: Top level should contain Value.")
    return _result_summary_recursive(summary_value=summary["Value"], is_root=True)


def _metadata_is_correct(metadata):
    try:
        json.loads(metadata.dataReq)
    except Exception:
        raise ValueError(
            f"Metadata: {metadata} contains wrong 'dataReq' value. This is not a valid json file.")
    if " " in metadata.name:
        raise ValueError(
            f"Metadata: {metadata} contains wrong 'name' value. Remove spaces from the name.")
    tags = [elem.strip() for elem in metadata.tags.split(",")]
    for tag in tags:
        if " " in tag:
            raise ValueError(
                f"Metadata: {metadata} contains wrong 'tag' value. "
                f"Remove spaces from '{tag}'.")


class CheckMetadataPy:
    """
    Create a new `CheckMetadataPy` object. `CheckMetadataPy` takes several arguments:

    * `name`: A string value containing the check name without spaces.

    * `type`: A string value containing the check type.

    * `tags`: A string value containing a tag or a sequence of tags separated by commas.
       Used to change the set of run checks be `--filter` option.
       For example, `python3 diagnostics.py --filter mytag` will run checks which contain
       `mytag` tag only. String values are case sensitive.

    * `descr`: A string value containing a check description.

    * `dataReq`: A string value in JSON format containing dict with name and version of dependencies.
      For example, if JSON string contains `{"my_check": 1, "my_check_2": 1}` it means that the current
      check depends on two checks: `my check` version 1 and `my_check_2` version 1. This check should be
      run with dependencies. The data dictionaries from these checks will be sent to the `run` function
      as the only argument. If check does not have a dependencies string should have empty JSON `{}`.

    * `merit`: An integer value containing a check merit. The higher the value, the higher the check
      result will be printed. We recommend that you follow the following guidelines for merit value:
      ` 0` - `19` - Checks that provide information about system configuration.
      `20` - `39` - Checks that provide information from drivers or tools.
      `40` - `59` - Checks that performance.
      `60` - `79` - Checks that check tools readiness.
      `80` - `99` - Checks that check system requirements.

    * `timeout`: An integer value containing the timeout in seconds. If check time exceeds the timeout,
       check will be forcibly completed without saving data.

    * `version`: An integer value containing the check version. We recommend to increase check version
      when you change `CheckSummary` `Value` dict tree.

    * `run`: A string value containing the name of a function to be called. A function should have the
      following declaration: `def my_func(data)` and should return `CheckSummary` object.
      If `dataReq` field is not empty, JSON dict data is used, along with data from dependencies checks.
      If `dataReq` is empty, JSON data is empty dict.
    """
    name: str
    type: str
    tags: str
    descr: str
    dataReq: str
    merit: int
    timeout: int
    version: int
    run: str

    def __init__(
            self,
            name: str,
            type: str,
            tags: str,
            descr: str,
            dataReq: str,
            merit: int,
            timeout: int,
            version: int,
            run: str) -> None:
        self.name = name
        self.type = type
        self.tags = tags
        self.descr = descr
        self.dataReq = dataReq
        self.merit = merit
        self.timeout = timeout
        self.version = version
        self.run = run
        self.__post_init__()

    def __post_init__(self) -> None:
        _metadata_is_correct(self)
        sorted_tags = [elem.strip() for elem in self.tags.split(",")]
        sorted_tags.sort()
        self.tags = ",".join(sorted_tags)

    def __str__(self) -> str:
        result = f"{type(self).__name__}("
        for key, value in self.__dict__.items():
            result += f"'{key}'='{value}',"
        result = f"{result[:-1]})"
        return result

    def __repr__(self) -> str:
        return str(self)


class CheckSummary:
    error_code: int
    result: str

    def __init__(self, result: str) -> None:
        self.error_code = _result_summary_is_correct(json.loads(result))
        self.result = result

    def __str__(self) -> str:
        result = f"{type(self).__name__}("
        for key, value in self.__dict__.items():
            result += f"'{key}'='{value}',"
        result = f"{result[:-1]})"
        return result

    def __repr__(self) -> str:
        return str(self)


def check_correct_metadata(function: Callable) -> Callable:
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        ret = function(self, *args, **kwargs)
        if hasattr(self, "metadata"):
            _metadata_is_correct(self.metadata)
        else:
            logging.warning("Cannot wrap function, because the object does not have a metadata attribute.")
        return ret
    return wrapper


def check_correct_summary(function: Callable) -> Callable:
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        ret = function(self, *args, **kwargs)
        _result_summary_is_correct(json.loads(ret.result))
        return ret
    return wrapper


class BaseCheck:
    metadata: Optional[CheckMetadataPy] = None
    summary: Optional[CheckSummary] = None

    def __init__(
            self,
            metadata: Optional[CheckMetadataPy] = None,
            summary: Optional[CheckSummary] = None) -> None:
        self.metadata = metadata
        self.summary = summary

    # It is necessary to return summary to ensure interprocessor communication
    def run(self, data: Dict) -> CheckSummary:
        raise NotImplementedError()

    # It is necessary to return api version
    def get_api_version(self) -> str:
        raise NotImplementedError()

    def get_metadata(self) -> Optional[CheckMetadataPy]:
        return self.metadata

    @check_correct_metadata
    def update_metadata(self, update: Dict) -> None:
        for key, value in update.items():
            if key in self.metadata.__dict__.keys():
                setattr(self.metadata, key, value)

    def set_summary(self, summary: CheckSummary) -> None:
        self.summary = summary

    def get_summary(self) -> Optional[CheckSummary]:
        return self.summary

    def __str__(self) -> str:
        result = f"{type(self).__name__}("
        for key, value in self.__dict__.items():
            result += f"'{key}'='{value}',"
        result = f"{result[:-1]})"
        return result

    def __repr__(self) -> str:
        return str(self)
