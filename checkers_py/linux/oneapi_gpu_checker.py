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
import subprocess
import tempfile
from typing import List, Dict

from modules.check import CheckSummary, CheckMetadataPy
from checkers_py.linux.common.gpu_helper import are_intel_gpus_found, intel_gpus_not_found_handler
from checkers_py.linux.common.gpu_helper import get_card_devices, get_render_devices

FULL_PATH_TO_CHECKER = os.path.dirname(os.path.realpath(__file__))
PATH_TO_SOURCE_OFFLOAD = os.path.join(FULL_PATH_TO_CHECKER, "oneapi_check_offloads")
TMP_MATMUL_FILE = os.path.join(tempfile.mkdtemp(), "matmul")
TMP_BINOPTION_FILE = os.path.join(tempfile.mkdtemp(), "binoption")
TMP_SIMPLE_SYCL_CODE_FILE = os.path.join(tempfile.mkdtemp(), "simple-sycl-code")
TMP_PARALLEL_FOR_1D_FILE = os.path.join(tempfile.mkdtemp(), "parallel-for-1D")
MISSING_COMPILER_MESSAGE = "Try to: " \
                           "1) install Intel® C++ Compiler based on " \
                           "https://www.intel.com/content/www/us/en/developer/articles/tool/oneapi-standalone-components.html " \
                           "2) set required variable by running: source /opt/intel/oneapi/setvars.sh"  # noqa E501


def get_i915_driver_loaded_info(json_node: Dict) -> None:
    value = {"Value": "", "RetVal": "PASS", "Command": "lsmod | grep i915"}
    try:
        lsmod_process = subprocess.Popen(
            ["lsmod"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        if lsmod_process.wait() != 0:
            raise Exception("Cannot get information about kernel modules that are currently loaded")

        grep_process = subprocess.Popen(
            ["grep", "i915"],
            stdin=lsmod_process.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        lsmod_process.stdout.close()

        stdout, _ = grep_process.communicate()
        if grep_process.returncode not in [0, 1]:
            raise Exception("Cannot get information about whether the Intel® Graphics Driver is loaded.")
        if not stdout.splitlines():
            value["RetVal"] = "FAIL"
            value["Message"] = "Module i915 is not loaded."
            value["HowToFix"] = "Try to load the i915 module with the following command: modprobe i915."
            value["AutomationFix"] = "modprobe i915"

    except Exception as error:
        value["RetVal"] = "ERROR"
        value["Message"] = str(error)
        value["HowToFix"] = "This error is unexpected. Please report the issue to " \
                            "Diagnostics Utility for Intel® oneAPI Toolkits repository: " \
                            "https://github.com/intel/diagnostics-utility."
    json_node.update({"Intel® Graphics Driver is loaded.": value})


def get_intel_device_is_available_info(json_node: Dict) -> None:
    value = {"Value": "", "RetVal": "PASS", "Command": "ls /dev/dri/ | grep renderD"}

    render_devices = get_render_devices()

    if len(render_devices) == 0:
        value["RetVal"] = "FAIL"
        value["Message"] = "Intel Graphics Device is not detected."
        value["HowToFix"] = "Check if the graphics driver is installed."

    json_node.update({"Intel Graphics Device is available": value})


def get_permissions_to_render_info(json_node: Dict) -> None:
    value = {"Value": "", "RetVal": "PASS", "Command": "ls -l /dev/dri/ | grep renderD"}

    render_devices = get_render_devices()

    access_to_render = False
    for render_device in render_devices:
        access_to_render = access_to_render or os.access(render_device, os.R_OK)

    if not access_to_render:
        value["RetVal"] = "FAIL"
        value["Message"] = "Current user does not have access to any render device."
        value["HowToFix"] = "Try to run the diagnostics with administrative privileges " \
                            "or add user to render group."
        value["AutomationFix"] = "sudo gpasswd -a ${{USER}} render && newgrp render"

    json_node.update({"Render device accessible to current user.": value})


def get_permissions_to_card_info(json_node: Dict) -> None:
    value = {"Value": "", "RetVal": "PASS", "Command": "ls -l /dev/dri/ | grep card"}

    card_devices = get_card_devices()

    access_to_card = False
    for card_device in card_devices:
        access_to_card = access_to_card or os.access(card_device, os.R_OK)

    if not access_to_card:
        value["RetVal"] = "FAIL"
        value["Message"] = "Current user does not have access to any card device."
        value["HowToFix"] = "Try to run the diagnostics with administrative privileges " \
                            "or check if the graphics driver is installed."

    json_node.update({"Card device accessible to current user": value})


def get_dmesg_i915_init_errors_info(json_node: Dict) -> None:
    value = {"Value": "", "RetVal": "PASS", "Command": "dmesg -T | grep i915 | grep failed"}
    try:
        dmesg_process = subprocess.Popen(
            ["dmesg", "-T"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        grep_i915_process = subprocess.Popen(
            ["grep", "i915"],
            stdin=dmesg_process.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        dmesg_process.stdout.close()

        if dmesg_process.wait() != 0:
            raise Exception("Cannot get information about timestamp from the kernel ring buffer.")

        stdout, _ = grep_i915_process.communicate()
        if grep_i915_process.returncode not in [0, 1]:
            raise Exception("Cannot get information about i915 initialization errors.")
        lines_with_errors = [line for line in stdout.splitlines() if "failed" in line]
        if lines_with_errors:
            value["RetVal"] = "FAIL"
            value["Message"] = "Initialization errors seen in i915 driver."
            value["Logs"] = lines_with_errors
            value["HowToFix"] = "Check related dmesg logs above for more details."

    except Exception as error:
        value["RetVal"] = "ERROR"
        value["Message"] = str(error)
        value["HowToFix"] = "This error is unexpected. Please report the issue to " \
                            "Diagnostics Utility for Intel® oneAPI Toolkits repository: " \
                            "https://github.com/intel/diagnostics-utility."

    json_node.update({"dmesg doesn't contain i915 errors": value})


def get_gpu_errors_info(json_node: Dict) -> None:
    value = {
        "Value": "",
        "RetVal": "PASS",
        "Command": "dmesg -T | grep -e HANG -e hang -e dump -e reassign -e blocked -e task: -e "
                   "Please -e segfault | tail -20"
    }
    try:
        dmesg_process = subprocess.Popen(
            ["dmesg", "-T"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        grep_process = subprocess.Popen(
            ["grep", "-e", "HANG", "-e", " hang", "-e", " dump ", "-e", "reassign",
             "-e", "blocked", "-e", "task:", "-e", "Please", "-e", "segfault"],
            stdin=dmesg_process.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        tail_process = subprocess.Popen(
            ["tail", "-20"], stdin=grep_process.stdout, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, encoding="utf-8")
        dmesg_process.stdout.close()
        grep_process.stdout.close()

        if dmesg_process.wait() != 0:
            raise Exception("Cannot get information about timestamp from the kernel ring buffer.")
        if grep_process.wait() not in [0, 1]:
            raise Exception("Cannot get information about i915 usage errors.")

        stdout, _ = tail_process.communicate()
        if tail_process.returncode != 0:
            raise Exception("Cannot get information about the last i915 usage errors.")
        lines_with_errors = stdout.splitlines()
        if lines_with_errors:
            value["RetVal"] = "FAIL"
            value["Message"] = "Found i915 usage errors."
            value["Logs"] = lines_with_errors
            value["HowToFix"] = "Check related dmesg logs above for more details."

    except Exception as error:
        value["RetVal"] = "ERROR"
        value["Message"] = str(error)
        value["HowToFix"] = "This error is unexpected. Please report the issue to " \
                            "Diagnostics Utility for Intel® oneAPI Toolkits repository: " \
                            "https://github.com/intel/diagnostics-utility."

    json_node.update({"dmesg doesn't contain user errors related to GPU operations": value})


def _compile_test_matmul(json_node: Dict) -> int:
    error_code = 0
    result = {"Compile test matmul": {
        "Value": "",
        "RetVal": "PASS",
        "Command": f"icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                   f"{PATH_TO_SOURCE_OFFLOAD}/matmul_offload.cpp -o {TMP_MATMUL_FILE}"
    }}
    try:
        compile = subprocess.Popen(
            ["icpx", "-fiopenmp", "-fopenmp-targets=spir64", "-D__STRICT_ANSI__",
             f"{PATH_TO_SOURCE_OFFLOAD}/matmul_offload.cpp", "-o", TMP_MATMUL_FILE],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)

        if compile.wait() != 0:
            error_code += 1
            result["Compile test matmul"]["RetVal"] = "FAIL"
            result["Compile test matmul"]["Message"] = \
                "Non zero return code from command: " \
                "'icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ " \
                f"{PATH_TO_SOURCE_OFFLOAD}/matmul_offload.cpp -o {TMP_MATMUL_FILE}'"
            result["Compile test matmul"]["HowToFix"] = \
                "Check compiled source file for syntax errors."
    except Exception:
        error_code += 1
        result["Compile test matmul"]["RetVal"] = "ERROR"
        result["Compile test matmul"]["Message"] = "Matmul compilation failed - icpx not found."
        result["Compile test matmul"]["HowToFix"] = MISSING_COMPILER_MESSAGE
    json_node.update(result)
    return error_code


def _run_test_matmul(compile_status: int, json_node: Dict) -> int:
    test_env = os.environ.copy()
    error_code = 0
    test_env["OMP_TARGET_OFFLOAD"] = "MANDATORY"
    result = {
        "Test simple matrix multiplication with Intel® oneAPI Level Zero.": {
            "Value": "",
            "RetVal": "PASS",
            "Command": f"OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 {TMP_MATMUL_FILE}"
        },
        "Test simple matrix multiplication with OpenCL™.": {
            "Value": "",
            "RetVal": "PASS",
            "Command": f"OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL {TMP_MATMUL_FILE}"
        }
    }
    if compile_status != 0:
        error_code += 1
        result["Test simple matrix multiplication with Intel® oneAPI Level Zero."]["RetVal"] = "FAIL"
        result["Test simple matrix multiplication with Intel® oneAPI Level Zero."]["Message"] = \
            "Check failed because compile test matmul failed."
        result["Test simple matrix multiplication with Intel® oneAPI Level Zero."]["HowToFix"] = \
            "Check compiled source file for syntax errors."
        result["Test simple matrix multiplication with OpenCL™."]["RetVal"] = "FAIL"
        result["Test simple matrix multiplication with OpenCL™."]["Message"] = \
            "Check failed because compile test matmul failed."
        result["Test simple matrix multiplication with OpenCL™."]["HowToFix"] = \
            "Check compiled source file for syntax errors."
    else:
        test_env["LIBOMPTARGET_PLUGIN"] = "LEVEL0"
        run_level_zero = subprocess.Popen(
            [TMP_MATMUL_FILE], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8", env=test_env)
        run_level_zero_stdout, _ = run_level_zero.communicate()
        if run_level_zero.returncode != 0 or run_level_zero_stdout.strip() != "PASSED":
            error_code += 1
            result["Test simple matrix multiplication with Intel® oneAPI Level Zero."]["RetVal"] = "FAIL"
            if run_level_zero.returncode != 0:
                result["Test simple matrix multiplication with Intel® oneAPI Level Zero."]["Message"] = \
                    f"An error occurred while running {TMP_MATMUL_FILE}. " \
                    f"ExitCode: {run_level_zero.returncode}"
                result["Test simple matrix multiplication with Intel® oneAPI Level Zero."]["HowToFix"] = \
                    f"Look into output for more details: \n{run_level_zero_stdout}"
            else:
                result["Test simple matrix multiplication with Intel® oneAPI Level Zero."]["Message"] = \
                    "Matrix multiplication failed."
                result["Test simple matrix multiplication with Intel® oneAPI Level Zero."]["HowToFix"] = \
                    f"Look into output for more details: \n{run_level_zero_stdout}"

        test_env["LIBOMPTARGET_PLUGIN"] = "OPENCL"
        run_opencl = subprocess.Popen(
            [TMP_MATMUL_FILE], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8", env=test_env)
        run_opencl_stdout, _ = run_opencl.communicate()
        if run_opencl.returncode != 0 or run_opencl_stdout.strip() != "PASSED":
            error_code += 1
            result["Test simple matrix multiplication with OpenCL™."]["RetVal"] = "FAIL"
            if run_opencl.returncode != 0:
                result["Test simple matrix multiplication with OpenCL™."]["Message"] = \
                    f"An error occurred while running {TMP_MATMUL_FILE}. ExitCode: {run_opencl.returncode}"
                result["Test simple matrix multiplication with OpenCL™."]["HowToFix"] = \
                    f"Look into output for more details: \n{run_opencl_stdout}"
            else:
                result["Test simple matrix multiplication with OpenCL™."]["Message"] = \
                    "Matrix multiplication had different results."
                result["Test simple matrix multiplication with OpenCL™."]["HowToFix"] = \
                    f"Look into output for more details: \n{run_opencl_stdout}"
    json_node.update(result)
    return error_code


def _compile_test_binoption(json_node: Dict) -> int:
    error_code = 0
    result = {"Compile test binoption": {
        "Value": "",
        "RetVal": "PASS",
        "Command": f"icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                   f"{PATH_TO_SOURCE_OFFLOAD}/binoption_standalone.cpp -o {TMP_BINOPTION_FILE}"
    }}
    try:
        compile = subprocess.Popen(
            ["icpx", "-fiopenmp", "-fopenmp-targets=spir64", "-D__STRICT_ANSI__",
             f"{PATH_TO_SOURCE_OFFLOAD}/binoption_standalone.cpp", "-o", TMP_BINOPTION_FILE],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
        if compile.wait() != 0:
            error_code += 1
            result["Compile test binoption"]["RetVal"] = "FAIL"
            result["Compile test binoption"]["Message"] = \
                "Non zero return code from command: " \
                "'icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ " \
                f"{PATH_TO_SOURCE_OFFLOAD}/binoption_standalone.cpp -o {TMP_BINOPTION_FILE}'"
            result["Compile test binoption"]["HowToFix"] = \
                "Check compiled source file for syntax errors."
    except Exception:
        error_code += 1
        result["Compile test binoption"]["RetVal"] = "ERROR"
        result["Compile test binoption"]["Message"] = "Binoption compilation failed - icpx not found."  # noqa E501
        result["Compile test binoption"]["HowToFix"] = MISSING_COMPILER_MESSAGE
    json_node.update(result)
    return error_code


def _run_test_binoption(compile_status: int, json_node: Dict) -> int:
    test_env = os.environ.copy()
    error_code = 0
    test_env["OMP_TARGET_OFFLOAD"] = "MANDATORY"
    result = {
        "Test simple binary options program with Intel® oneAPI Level Zero.": {
            "Value": "",
            "RetVal": "PASS",
            "Command": f"OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 {TMP_BINOPTION_FILE}"
        },
        "Test simple binary options program with OpenCL™.": {
            "Value": "",
            "RetVal": "PASS",
            "Command": f"OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL {TMP_BINOPTION_FILE}"
        }
    }
    if compile_status != 0:
        error_code += 1
        result["Test simple binary options program with Intel® oneAPI Level Zero."]["RetVal"] = "FAIL"
        result["Test simple binary options program with Intel® oneAPI Level Zero."]["Message"] = \
            "Check failed because compile test binoption failed."
        result["Test simple binary options program with Intel® oneAPI Level Zero."]["HowToFix"] = \
            "Check compiled source file for syntax errors."
        result["Test simple binary options program with OpenCL™."]["RetVal"] = "FAIL"
        result["Test simple binary options program with OpenCL™."]["Message"] = \
            "Check failed because compile test binoption failed."
        result["Test simple binary options program with OpenCL™."]["HowToFix"] = \
            "Check compiled source file for syntax errors."
    else:
        test_env["LIBOMPTARGET_PLUGIN"] = "LEVEL0"
        run_binoption_level_zero = subprocess.Popen(
            [TMP_BINOPTION_FILE], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            encoding="utf-8", env=test_env)
        run_binoption_level_zero_stdout, _ = run_binoption_level_zero.communicate()
        if run_binoption_level_zero.returncode != 0 or run_binoption_level_zero_stdout.strip() != "PASSED":
            error_code += 1
            result["Test simple binary options program with Intel® oneAPI Level Zero."]["RetVal"] = "FAIL"
            if run_binoption_level_zero.returncode != 0:
                result["Test simple binary options program with Intel® oneAPI Level Zero."]["Message"] = \
                    f"An error occurred while running {TMP_BINOPTION_FILE}. " \
                    f"ExitCode: {run_binoption_level_zero.returncode}"
                result["Test simple binary options program with Intel® oneAPI Level Zero."]["HowToFix"] = \
                    f"Look into output for more details: \n{run_binoption_level_zero_stdout}"
            else:
                result["Test simple binary options program with Intel® oneAPI Level Zero."]["Message"] = \
                    "Binary options program failed."
                result["Test simple binary options program with Intel® oneAPI Level Zero."]["HowToFix"] = \
                    f"Look into output for more details: \n{run_binoption_level_zero_stdout}"

        test_env["LIBOMPTARGET_PLUGIN"] = "OPENCL"
        run_binoption_opencl = subprocess.Popen(
            [TMP_BINOPTION_FILE], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            encoding="utf-8", env=test_env)
        run_binoption_opencl_stdout, _ = run_binoption_opencl.communicate()
        if run_binoption_opencl.returncode != 0 or run_binoption_opencl_stdout.strip() != "PASSED":
            error_code += 1
            result["Test simple binary options program with OpenCL™."]["RetVal"] = "FAIL"
            if run_binoption_opencl.returncode != 0:
                result["Test simple binary options program with OpenCL™."]["Message"] = \
                    f"An error occurred while running {TMP_BINOPTION_FILE}. " \
                    f"ExitCode: {run_binoption_opencl.returncode}"
                result["Test simple binary options program with OpenCL™."]["HowToFix"] = \
                    f"Look into output for more details: \n{run_binoption_opencl_stdout}"
            else:
                result["Test simple binary options program with OpenCL™."]["Message"] = \
                    "Binary options program failed."
                result["Test simple binary options program with OpenCL™."]["HowToFix"] = \
                    f"Look into output for more details: \n{run_binoption_opencl_stdout}"
    json_node.update(result)
    return error_code


def get_openmp_offload_info(json_node: Dict) -> None:
    error_code = 0
    value = {"Value": {}, "RetVal": "PASS"}

    compile_matmul_status = _compile_test_matmul(value["Value"])
    error_code += _run_test_matmul(compile_matmul_status, value["Value"])

    compile_binoption_status = _compile_test_binoption(value["Value"])
    error_code += _run_test_binoption(compile_binoption_status, value["Value"])

    if error_code != 0:
        value["RetVal"] = "FAIL"
        value["Message"] = "Some checks below failed."
        value["HowToFix"] = "Review output of checks for more details."

    json_node.update({"OpenMP GPU pipeline tests": value})


def _compile_simple_sycl_code(json_node: Dict) -> int:
    error_code = 0
    result = {"Compile simple SYCL code": {
        "Value": "",
        "RetVal": "PASS",
        "Command": f"dpcpp -std=c++17 -fsycl {PATH_TO_SOURCE_OFFLOAD}/simple-sycl-code.cpp "
                   f"-o {TMP_SIMPLE_SYCL_CODE_FILE}"
    }}
    try:
        compile = subprocess.Popen(
            ["dpcpp", "-std=c++17", "-fsycl", f"{PATH_TO_SOURCE_OFFLOAD}/simple-sycl-code.cpp",
             "-o", TMP_SIMPLE_SYCL_CODE_FILE],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
        if compile.wait() != 0:
            error_code += 1
            result["Compile simple SYCL code"]["RetVal"] = "FAIL"
            result["Compile simple SYCL code"]["Message"] = \
                f"'dpcpp -std=c++17 -fsycl {PATH_TO_SOURCE_OFFLOAD}/simple-sycl-code.cpp " \
                f"-o {TMP_SIMPLE_SYCL_CODE_FILE}'"
            result["Compile simple SYCL code"]["HowToFix"] = \
                "Check compiled source file for syntax errors."
    except Exception:
        error_code += 1
        result["Compile simple SYCL code"]["RetVal"] = "ERROR"
        result["Compile simple SYCL code"]["Message"] = "Sycl code compilation failed - DPC++ (dpcpp) not found."  # noqa E501
        result["Compile simple SYCL code"]["HowToFix"] = MISSING_COMPILER_MESSAGE
    json_node.update(result)
    return error_code


def _run_simple_sycl_code(compile_status: int, json_node: Dict) -> int:
    test_env = os.environ.copy()
    error_code = 0
    result = {
        "Test simple DPC++ program with Intel® oneAPI Level Zero.": {
            "Value": "",
            "RetVal": "PASS",
            "Command": f"SYCL_DEVICE_FILTER=level_zero:gpu {TMP_SIMPLE_SYCL_CODE_FILE}"
        },
        "Test simple DPC++ program with OpenCL™.": {
            "Value": "",
            "RetVal": "PASS",
            "Command": f"SYCL_DEVICE_FILTER=opencl:gpu {TMP_SIMPLE_SYCL_CODE_FILE}"
        }
    }
    if compile_status != 0:
        error_code += 1
        result["Test simple DPC++ program with Intel® oneAPI Level Zero."]["RetVal"] = "FAIL"
        result["Test simple DPC++ program with Intel® oneAPI Level Zero."]["Message"] = \
            "Check failed because compile simple SYCL code failed."
        result["Test simple DPC++ program with Intel® oneAPI Level Zero."]["HowToFix"] = \
            "Check compiled source file for syntax errors."
        result["Test simple DPC++ program with OpenCL™."]["RetVal"] = "FAIL"
        result["Test simple DPC++ program with OpenCL™."]["Message"] = \
            "Check failed because compile simple SYCL code failed."
        result["Test simple DPC++ program with OpenCL™."]["HowToFix"] = \
            "Check compiled source file for syntax errors."
    else:
        test_env["SYCL_DEVICE_FILTER"] = "level_zero:gpu"
        run_level_zero = subprocess.Popen(
            [TMP_SIMPLE_SYCL_CODE_FILE], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            encoding="utf-8", env=test_env)
        run_level_zero_stdout, _ = run_level_zero.communicate()
        if run_level_zero.returncode != 0 or run_level_zero_stdout.strip() != "PASSED":
            error_code += 1
            result["Test simple DPC++ program with Intel® oneAPI Level Zero."]["RetVal"] = "FAIL"
            if run_level_zero.returncode != 0:
                result["Test simple DPC++ program with Intel® oneAPI Level Zero."]["Message"] = \
                    f"An error occurred while running {TMP_SIMPLE_SYCL_CODE_FILE}. " \
                    f"ExitCode: {run_level_zero.returncode}"
                result["Test simple DPC++ program with Intel® oneAPI Level Zero."]["HowToFix"] = \
                    f"Look into output for more details: \n{run_level_zero_stdout}"
            else:
                result["Test simple DPC++ program with Intel® oneAPI Level Zero."]["Message"] = \
                    "DPC++ program program failed."
                result["Test simple DPC++ program with Intel® oneAPI Level Zero."]["HowToFix"] = \
                    f"Look into output for more details: \n{run_level_zero_stdout}"

        test_env["SYCL_DEVICE_FILTER"] = "opencl:gpu"
        run_opencl = subprocess.Popen(
            [TMP_SIMPLE_SYCL_CODE_FILE], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            encoding="utf-8", env=test_env)
        run_opencl_stdout, _ = run_opencl.communicate()
        if run_opencl.returncode != 0 or run_opencl_stdout.strip() != "PASSED":
            error_code += 1
            result["Test simple DPC++ program with OpenCL™."]["RetVal"] = "FAIL"
            if run_opencl.returncode != 0:
                result["Test simple DPC++ program with OpenCL™."]["Message"] = \
                    f"An error occurred while running {TMP_SIMPLE_SYCL_CODE_FILE}. " \
                    f"ExitCode: {run_opencl.returncode}"
                result["Test simple DPC++ program with OpenCL™."]["HowToFix"] = \
                    f"Look into output for more details: \n{run_opencl_stdout}"
            else:
                result["Test simple DPC++ program with OpenCL™."]["Message"] = \
                    "DPC++ program program failed."
                result["Test simple DPC++ program with OpenCL™."]["HowToFix"] = \
                    f"Look into output for more details: \n{run_opencl_stdout}"
    json_node.update(result)
    return error_code


def _compile_parallel_for_program(json_node: Dict) -> int:
    error_code = 0
    result = {"Compile parallel for program": {
        "Value": "",
        "RetVal": "PASS",
        "Command": f"dpcpp -std=c++17 -fsycl {PATH_TO_SOURCE_OFFLOAD}/parallel-for-1D.cpp "
                   f"-o {TMP_PARALLEL_FOR_1D_FILE}"
    }}
    try:
        compile = subprocess.Popen(
            ["dpcpp", "-std=c++17", "-fsycl", f"{PATH_TO_SOURCE_OFFLOAD}/parallel-for-1D.cpp",
             "-o", TMP_PARALLEL_FOR_1D_FILE],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
        if compile.wait() != 0:
            error_code += 1
            result["Compile parallel for program"]["RetVal"] = "FAIL"
            result["Compile parallel for program"]["Message"] = \
                f"dpcpp -std=c++17 -fsycl {PATH_TO_SOURCE_OFFLOAD}/parallel-for-1D.cpp " \
                f"-o {TMP_PARALLEL_FOR_1D_FILE}"
            result["Compile parallel for program"]["HowToFix"] = \
                "Check compiled source file for syntax errors."
    except Exception:
        error_code += 1
        result["Compile parallel for program"]["RetVal"] = "ERROR"
        result["Compile parallel for program"]["Message"] = "Parallel code compilation failed - DPC++ (dpcpp) not found."  # noqa
        result["Compile parallel for program"]["HowToFix"] = MISSING_COMPILER_MESSAGE
    json_node.update(result)
    return error_code


def _run_parallel_for_program(compile_status: int, json_node: Dict) -> int:
    test_env = os.environ.copy()
    error_code = 0
    result = {
        "Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero.": {
            "Value": "",
            "RetVal": "PASS",
            "Command": f"SYCL_DEVICE_FILTER=level_zero:gpu {TMP_PARALLEL_FOR_1D_FILE}"
        },
        "Test simple DPC++ parallel-for program with OpenCL™.": {
            "Value": "",
            "RetVal": "PASS",
            "Command": f"SYCL_DEVICE_FILTER=opencl:gpu {TMP_PARALLEL_FOR_1D_FILE}"
        }
    }
    if compile_status != 0:
        error_code += 1
        result["Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero."]["RetVal"] = "FAIL"
        result["Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero."]["Message"] = \
            "Check failed because compile parallel for program failed."
        result["Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero."]["HowToFix"] = \
            "Check compiled source file for syntax errors."
        result["Test simple DPC++ parallel-for program with OpenCL™."]["RetVal"] = "FAIL"
        result["Test simple DPC++ parallel-for program with OpenCL™."]["Message"] = \
            "Check failed because compile parallel for program failed."
        result["Test simple DPC++ parallel-for program with OpenCL™."]["HowToFix"] = \
            "Check compiled source file for syntax errors."
    else:
        test_env["SYCL_DEVICE_FILTER"] = "level_zero:gpu"
        run_level_zero = subprocess.Popen(
            [TMP_PARALLEL_FOR_1D_FILE], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            encoding="utf-8", env=test_env)
        run_level_zero_stdout, _ = run_level_zero.communicate()
        if run_level_zero.returncode != 0 or run_level_zero_stdout.strip() != "PASSED":
            error_code += 1
            result["Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero."]["RetVal"] = "FAIL"
            if run_level_zero.returncode != 0:
                result["Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero."]["Message"] \
                    = f"An error occurred while running {TMP_PARALLEL_FOR_1D_FILE}. " \
                      f"ExitCode: {run_level_zero.returncode}"
                result["Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero."]["HowToFix"] \
                    = f"Look into output for more details: \n{run_level_zero_stdout}"
            else:
                result["Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero."]["Message"] \
                    = "DPC++ parallel-for program program failed."
                result["Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero."]["HowToFix"] \
                    = f"Look into output for more details: \n{run_level_zero_stdout}"

        test_env["SYCL_DEVICE_FILTER"] = "opencl:gpu"
        run_opencl = subprocess.Popen(
            [TMP_PARALLEL_FOR_1D_FILE], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            encoding="utf-8", env=test_env)
        run_opencl_stdout, _ = run_opencl.communicate()
        if run_opencl.returncode != 0 or run_opencl_stdout.strip() != "PASSED":
            error_code += 1
            result["Test simple DPC++ parallel-for program with OpenCL™."]["RetVal"] = "FAIL"
            if run_opencl.returncode != 0:
                result["Test simple DPC++ parallel-for program with OpenCL™."]["Message"] = \
                    f"An error occurred while running {TMP_PARALLEL_FOR_1D_FILE}. " \
                    f"ExitCode: {run_opencl.returncode}"
                result["Test simple DPC++ parallel-for program with OpenCL™."]["HowToFix"] = \
                    f"Look into output for more details: \n{run_opencl_stdout}"
            else:
                result["Test simple DPC++ parallel-for program with OpenCL™."]["Message"] = \
                    "DPC++ parallel-for program program failed."
                result["Test simple DPC++ parallel-for program with OpenCL™."]["HowToFix"] = \
                    f"Review output for more details: \n{run_opencl_stdout}"
    json_node.update(result)
    return error_code


def get_dpcpp_offload_info(json_node: Dict) -> None:
    error_code = 0
    value = {"Value": {}, "RetVal": "PASS"}

    compile_simple_sycl_status = _compile_simple_sycl_code(value["Value"])
    error_code += _run_simple_sycl_code(compile_simple_sycl_status, value["Value"])
    compile_parallel_for_status = _compile_parallel_for_program(value["Value"])
    error_code += _run_parallel_for_program(compile_parallel_for_status, value["Value"])

    if error_code != 0:
        value["RetVal"] = "FAIL"
        value["Message"] = "Some checks below failed."
        value["HowToFix"] = "Review output of checks for more details."

    json_node.update({"DPC++ GPU pipeline tests": value})


def run_oneapi_gpu_check(data: dict) -> CheckSummary:
    result_json = {"Value": {}}

    if not are_intel_gpus_found(data):
        intel_gpus_not_found_handler(result_json["Value"])

    get_i915_driver_loaded_info(result_json["Value"])
    get_intel_device_is_available_info(result_json["Value"])
    get_permissions_to_card_info(result_json["Value"])
    get_permissions_to_render_info(result_json["Value"])
    get_dmesg_i915_init_errors_info(result_json["Value"])
    get_gpu_errors_info(result_json["Value"])
    get_openmp_offload_info(result_json["Value"])
    get_dpcpp_offload_info(result_json["Value"])

    check_summary = CheckSummary(
        result=json.dumps(result_json, indent=4)
    )

    return check_summary


def get_api_version() -> str:
    return "0.1"


def get_check_list() -> List[CheckMetadataPy]:
    someCheck = CheckMetadataPy(
        name="oneapi_gpu_check",
        type="Data",
        tags="gpu,sysinfo",
        descr="This check runs GPU workloads and verifies readiness to run applications on GPU(s).",
        dataReq="{\"intel_gpu_detector_check\": 1}",
        merit=60,
        timeout=30,
        version=1,
        run="run_oneapi_gpu_check"
    )
    return [someCheck]
