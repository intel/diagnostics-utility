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

from pathlib import Path
import platform
from modules.check import CheckSummary, CheckMetadataPy

import os
import re
import json
from typing import List
from modules.files_helper import get_json_content_from_file


default_setvars_location = "C:\\Program Files (x86)\\Intel\\oneAPI\\setvars.bat" if platform.system(
) == "Windows" else "/opt/intel/oneapi/setvars.sh"


def get_api_version() -> str:
    return "0.2"


def get_check_list() -> List[CheckMetadataPy]:
    someCheck = CheckMetadataPy(
        name="oneapi_env_check",
        type="Data",
        groups="default,sysinfo,compile,runtime,host,target",
        descr="This check shows if the oneAPI environment is configured and provides "
        "a list of oneAPI components with their versions if they are present in the environment",
        dataReq="{}",
        merit=20,
        timeout=55,
        version=2,
        run="run_oneapi_env_check"
    )
    return [someCheck]


def run_oneapi_env_check(data: dict) -> CheckSummary:
    result_json = {"CheckResult": {}}

    result_json["CheckResult"].update(check_if_env_is_configured())
    if result_json["CheckResult"]["Presence of oneAPI environment"]["CheckStatus"] == "PASS":
        result_json["CheckResult"].update(get_versions_of_oneapi_products_installed_in_env())
    check_summary = CheckSummary(
        result=json.dumps(result_json, indent=4)
    )

    return check_summary


def check_if_env_is_configured():
    check_result = {"CheckResult": "", "CheckStatus": "PASS"}
    PATH_ENV = os.getenv('SETVARS_COMPLETED')
    if PATH_ENV is None:
        check_result["CheckStatus"] = "FAIL"
        check_result["Message"] = "oneAPI environment not configured."
        check_result["HowToFix"] = "Run the setvars script " \
            f"(default location is {default_setvars_location})"
    return {"Presence of oneAPI environment": check_result}


def get_versions_of_oneapi_products_installed_in_env():
    check_result = {"CheckResult": {}, "CheckStatus": "INFO"}
    if is_new_layout():
        return {}
    try:
        oneapi_product_names_map = get_json_content_from_file(Path(__file__).parent.resolve() / "data" / "oneapi_names_map.json")  # noqa: E501
        if not oneapi_product_names_map:
            raise Exception("oneAPI product names map is empty.")

        for long_name, short_name in oneapi_product_names_map.items():
            product_versions = get_product_versions_from_env(short_name)
            if len(product_versions) == 0:
                continue

            product_check_result = get_product_check_result(long_name, product_versions)
            check_result["CheckResult"].update({long_name: product_check_result})

        if not check_result["CheckResult"]:
            check_result["CheckStatus"] = "WARNING"
            check_result["Message"] = "There are no oneAPI products found in the current environment."

    except Exception as error:
        check_result["CheckStatus"] = "ERROR"
        check_result["Message"] = str(error)
        check_result["HowToFix"] = "This error is unexpected. Please report the issue to " \
            "Diagnostics Utility for oneAPI repository: " \
            "https://github.com/intel/diagnostics-utility."

    return {"oneAPI products installed in the environment": check_result}


def is_new_layout():
    PATH_ENV = os.getenv('ONEAPI_ROOT')
    if os.path.exists(os.path.join(PATH_ENV, "bin")):
        return True
    return False


def get_product_versions_from_env(component_name):
    env_paths = get_possible_paths_from_env()
    product_versions_pattern = re.compile(fr".+/{component_name}/([0-9.]+)/.+")
    product_versions = set()
    for path in env_paths:
        product_version_match = re.search(product_versions_pattern, path)
        if product_version_match:
            product_versions.add(product_version_match.group(1))
    return product_versions


def get_possible_paths_from_env():
    LD_LIBRARY_PATH_ENV = os.getenv('LD_LIBRARY_PATH')
    LIBRARY_PATH_ENV = os.getenv('LIBRARY_PATH')
    PATH_ENV = os.getenv('PATH')
    env_paths = []
    separator = ";" if platform.system() == "Windows" else ":"
    env_paths += LD_LIBRARY_PATH_ENV.split(sep=separator) if LD_LIBRARY_PATH_ENV else []
    env_paths += LIBRARY_PATH_ENV.split(sep=separator) if LIBRARY_PATH_ENV else []
    env_paths += PATH_ENV.split(sep=separator) if PATH_ENV else []
    norm_paths = [os.path.realpath(path).replace('\\', '/') for path in env_paths]
    return norm_paths


def get_product_check_result(long_name, product_versions):
    product_check_result = {
        "CheckResult": {
            "Version": {
                "CheckResult": "",
                "CheckStatus": "INFO"
            }
        },
        "CheckStatus": "INFO"
    }
    if len(product_versions) == 1:
        product_check_result["CheckResult"]["Version"]["CheckResult"] = list(product_versions)[0]
    else:
        product_check_result["CheckResult"]["Version"]["CheckResult"] = ",".join(sorted(product_versions))
        product_check_result["CheckResult"]["Version"]["CheckStatus"] = "WARNING"
        product_check_result["CheckResult"]["Version"]["Message"] = f"Several versions of {long_name} were found in the current environment."  # noqa: E501
    return product_check_result
