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
import faulthandler

from functools import wraps
from multiprocessing import Process, Queue
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
            raise ValueError(f"Error in subtree: {data}. RetVal is required")

        if "Verbosity" in data:
            if not isinstance(data["Verbosity"], int):
                raise ValueError(
                    f"Error in subtree: {data}. Verbosity must be a integer")
            if is_root:
                if 0 < data["Verbosity"]:
                    raise ValueError(
                        f"Error in subtree: {data}. Root verbosity level must to be zero")
        if "Message" in data:
            if not isinstance(data["Message"], str):
                raise ValueError(
                    f"Error in subtree: {data}. Message must be a string")
        if "Command" in data:
            if not isinstance(data["Command"], str):
                raise ValueError(
                    f"Error in subtree: {data}. Command must be a string")
        if "Value" in data:
            if isinstance(data["Value"], dict):
                subcheck_error_code = max(
                    subcheck_error_code,
                    _result_summary_recursive(data["Value"])
                )
        else:
            raise ValueError(f"Error in subtree: {data}. Value is required")
        result_error_code = max(
            result_error_code,
            subcheck_error_code
        )
    return result_error_code


def _result_summary_is_correct(
        summary: Dict) -> int:
    if len(summary) == 0:
        raise ValueError("Value dictionary cannot be empty")
    if "Value" not in summary:
        raise ValueError("Result summary is not correct: Top level should contain Value")
    return _result_summary_recursive(summary_value=summary["Value"], is_root=True)


def _metadata_is_correct(metadata):
    try:
        json.loads(metadata.dataReq)
    except Exception:
        raise ValueError(
            f"Metadata: {metadata} contains wrong 'dataReq' value. Isn't valid json")
    if " " in metadata.name:
        raise ValueError(
            f"Metadata: {metadata} contains wrong 'name' value. Name have to be without spaces")
    tags = [elem.strip() for elem in metadata.tags.split(",")]
    for tag in tags:
        if " " in tag:
            raise ValueError(
                f"Metadata: {metadata} contains wrong 'tag' value. "
                f"Tag have to be without spaces. Tag '{tag}' have a space.")
    correct_rights = ["user", "admin"]
    if metadata.rights not in correct_rights:
        raise ValueError(
            f"Metadata: {metadata} contains wrong 'rights' value. "
            f"Rights can be 'user' and 'admin' only")


class CheckMetadataPy:
    name: str
    type: str
    tags: str
    descr: str
    dataReq: str
    rights: str
    timeout: int
    version: str
    run: str

    def __init__(
            self,
            name: str,
            type: str,
            tags: str,
            descr: str,
            dataReq: str,
            rights: str,
            timeout: int,
            version: str,
            run: str) -> None:
        self.name = name
        self.type = type
        self.tags = tags
        self.descr = descr
        self.dataReq = dataReq
        self.rights = rights
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
            logging.warning("Can't wraps function, because object have not metadata attribute")
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


def timeout_exit(function: Callable[[BaseCheck, Dict], CheckSummary]) -> \
        Callable[[BaseCheck, Dict], CheckSummary]:
    @wraps(function)
    def wrapper(instance: BaseCheck, dataReqDict: Dict) -> CheckSummary:
        faulthandler.enable()
        queue = Queue()

        def queue_wrapper(dataReqDict):
            result = function(dataReqDict)
            queue.put(result)

        process = Process(target=queue_wrapper, args=(dataReqDict,))
        process.start()
        try:
            result = queue.get(block=True, timeout=instance.get_metadata().timeout)
        except Exception:
            if process.exitcode is None:
                process.terminate()
                json_dict = {
                    "RetVal": "ERROR",
                    "Verbosity": 0,
                    "Message": "",
                    "Value": {
                        f"{instance.get_metadata().name}": {
                            "Value": "Timeout was exceeded",
                            "Verbosity": 0,
                            "Message": "",
                            "RetVal": "ERROR"
                        }
                    }
                }
                json_str = json.dumps(json_dict)
                result = CheckSummary(result=json_str)
            else:
                json_dict = {
                    "RetVal": "ERROR",
                    "Verbosity": 0,
                    "Message": "",
                    "Value": {
                        f"{instance.get_metadata().name}": {
                            "Value": "",
                            "Verbosity": 0,
                            "Message": "The check crushed at runtime. No data was received. "
                                       "See call stack above.",
                            "RetVal": "ERROR"
                        }
                    }
                }
                json_str = json.dumps(json_dict)
                result = CheckSummary(result=json_str)
        faulthandler.disable()
        return result
    return wrapper
