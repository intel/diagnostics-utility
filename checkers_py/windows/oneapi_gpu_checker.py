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
import platform
from typing import List, Dict

from modules.check import CheckSummary, CheckMetadataPy

platform_os = platform.system()

FULL_PATH_TO_CHECKER = os.path.dirname(os.path.realpath(__file__))
PATH_TO_SOURCE_OFFLOAD = os.path.join(FULL_PATH_TO_CHECKER, "oneapi_check_offloads")
TMP_MATMUL_FILE = os.path.join(tempfile.mkdtemp(), "matmul.exe")
TMP_BINOPTION_FILE = os.path.join(tempfile.mkdtemp(), "binoption.exe")
TMP_SIMPLE_SYCL_CODE_FILE = os.path.join(tempfile.mkdtemp(), "simple-sycl-code.exe")
TMP_PARALLEL_FOR_1D_FILE = os.path.join(tempfile.mkdtemp(), "parallel-for-1D.exe")
MISSING_COMPILER_MESSAGE = "Try to: " \
                           "1) install Intel® C++ Compiler based on " \
                           "https://www.intel.com/content/www/us/en/developer/articles/tool/oneapi-standalone-components.html " \
                           "2) Initialize oneAPI environment:"\
                            " run <ONEAPI_INSTALL_DIR>\\intel\\oneAPI\\setvars.bat on Windows. " \
                           "Default install location is C:\\Program Files (x86)\\intel\\oneAPI"   # noqa E501


def get_api_version() -> str:
    return "0.2"


def get_check_list() -> List[CheckMetadataPy]:
    someCheck = CheckMetadataPy(
        name="oneapi_gpu_check",
        type="Data",
        groups="gpu,sysinfo",
        descr="This check runs GPU workloads and verifies readiness to run applications on GPU(s).",
        dataReq="{\"intel_gpu_detector_check\": 2}",
        merit=60,
        timeout=40,
        version=2,
        run="run_oneapi_gpu_check"
    )
    return [someCheck]


def run_oneapi_gpu_check(data: dict) -> CheckSummary:
    result_json = {"CheckResult": {}}
    if are_intel_gpus_found(data):
        result_json["CheckResult"].update(intel_gpus_not_found())

    result_json["CheckResult"].update(get_openmp_offload_info())
    result_json["CheckResult"].update(get_icpx_offload_info())

    check_summary = CheckSummary(
        result=json.dumps(result_json, indent=4)
    )

    return check_summary


def are_intel_gpus_found(data):
    try:
        if data["intel_gpu_detector_check"]["CheckResult"]["GPU driver information"]["CheckStatus"] != "PASS":
            return True
        else:
            return False
    except Exception:
        return False


def intel_gpus_not_found():
    return {
        "Warning message": {
            "CheckResult": "",
            "CheckStatus": "WARNING",
            "Message": "The check might show irrelevant information for your system because "
                       "the intel_gpu_detector_check failed."
        }
    }


def get_openmp_offload_info():
    error_code = 0
    check_result = {"CheckResult": {}, "CheckStatus": "PASS"}

    compile_matmul_status = _compile_test_matmul(check_result["CheckResult"])
    error_code += _run_test_matmul(compile_matmul_status, check_result["CheckResult"])

    compile_binoption_status = _compile_test_binoption(check_result["CheckResult"])
    error_code += _run_test_binoption(compile_binoption_status, check_result["CheckResult"])

    if error_code != 0:
        check_result["CheckStatus"] = "FAIL"
        check_result["Message"] = "Some checks below failed."
        check_result["HowToFix"] = "Review output of checks for more details."

    return {"OpenMP GPU pipeline tests": check_result}


def get_icpx_offload_info():
    error_code = 0
    check_result = {"CheckResult": {}, "CheckStatus": "PASS"}

    compile_simple_sycl_status = _compile_simple_sycl_code(check_result["CheckResult"])
    error_code += _run_simple_sycl_code(compile_simple_sycl_status, check_result["CheckResult"])
    compile_parallel_for_status = _compile_parallel_for_program(check_result["CheckResult"])
    error_code += _run_parallel_for_program(compile_parallel_for_status, check_result["CheckResult"])

    if error_code != 0:
        check_result["CheckStatus"] = "FAIL"
        check_result["Message"] = "Some checks below failed."
        check_result["HowToFix"] = "Review output of checks for more details."

    return {"DPC++ GPU pipeline tests": check_result}


def _compile_test_matmul(json_node: Dict) -> int:
    error_code = 0
    result = {"Compile test matmul": {
        "CheckResult": "",
        "CheckStatus": "PASS",
        "Command": f"icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                   f"{PATH_TO_SOURCE_OFFLOAD}\\matmul_offload.cpp -o {TMP_MATMUL_FILE}"
    }}
    try:
        compile = subprocess.Popen(
            ["icpx", "-fiopenmp", "-fopenmp-targets=spir64", "-D__STRICT_ANSI__",
             f"{PATH_TO_SOURCE_OFFLOAD}\\matmul_offload.cpp", "-o", TMP_MATMUL_FILE],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)

        if compile.wait() != 0:
            error_code += 1
            result["Compile test matmul"]["CheckStatus"] = "FAIL"
            result["Compile test matmul"]["Message"] = \
                "Non zero return code from command: " \
                "'icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ " \
                f"{PATH_TO_SOURCE_OFFLOAD}\\matmul_offload.cpp -o {TMP_MATMUL_FILE}'"
            result["Compile test matmul"]["HowToFix"] = \
                "Check compiled source file for syntax errors."
    except Exception:
        error_code += 1
        result["Compile test matmul"]["CheckStatus"] = "ERROR"
        result["Compile test matmul"]["Message"] = "Matmul compilation failed - icpx compiler is not found."
        result["Compile test matmul"]["HowToFix"] = MISSING_COMPILER_MESSAGE
    json_node.update(result)
    return error_code


def _run_test_matmul(compile_status: int, json_node: Dict) -> int:
    test_env = os.environ.copy()
    error_code = 0
    test_env["OMP_TARGET_OFFLOAD"] = "MANDATORY"
    result = {
        "Test simple matrix multiplication with Intel® oneAPI Level Zero.": {
            "CheckResult": "",
            "CheckStatus": "PASS",
            "Command": f"OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 {TMP_MATMUL_FILE}"
        },
        "Test simple matrix multiplication with OpenCL™.": {
            "CheckResult": "",
            "CheckStatus": "PASS",
            "Command": f"OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL {TMP_MATMUL_FILE}"
        }
    }
    if compile_status != 0:
        error_code += 1
        result["Test simple matrix multiplication with Intel® oneAPI Level Zero."]["CheckStatus"] = "FAIL"
        result["Test simple matrix multiplication with Intel® oneAPI Level Zero."]["Message"] = \
            "Check failed because compile test matmul failed."
        result["Test simple matrix multiplication with Intel® oneAPI Level Zero."]["HowToFix"] = \
            "Check compiled source file for syntax errors."
        result["Test simple matrix multiplication with OpenCL™."]["CheckStatus"] = "FAIL"
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
            result["Test simple matrix multiplication with Intel® oneAPI Level Zero."]["CheckStatus"] = "FAIL"
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
            result["Test simple matrix multiplication with OpenCL™."]["CheckStatus"] = "FAIL"
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
        "CheckResult": "",
        "CheckStatus": "PASS",
        "Command": f"icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                   f"{PATH_TO_SOURCE_OFFLOAD}\\binoption_standalone.cpp -o {TMP_BINOPTION_FILE}"
    }}
    try:
        compile = subprocess.Popen(
            ["icpx", "-fiopenmp", "-fopenmp-targets=spir64", "-D__STRICT_ANSI__",
             f"{PATH_TO_SOURCE_OFFLOAD}\\binoption_standalone.cpp", "-o", TMP_BINOPTION_FILE],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
        if compile.wait() != 0:
            error_code += 1
            result["Compile test binoption"]["CheckStatus"] = "FAIL"
            result["Compile test binoption"]["Message"] = \
                "Non zero return code from command: " \
                "'icpx -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ " \
                f"{PATH_TO_SOURCE_OFFLOAD}\\binoption_standalone.cpp -o {TMP_BINOPTION_FILE}'"
            result["Compile test binoption"]["HowToFix"] = \
                "Check compiled source file for syntax errors."
    except Exception:
        error_code += 1
        result["Compile test binoption"]["CheckStatus"] = "ERROR"
        result["Compile test binoption"]["Message"] = "Binoption compilation failed - icpx compiler is not found."  # noqa E501
        result["Compile test binoption"]["HowToFix"] = MISSING_COMPILER_MESSAGE
    json_node.update(result)
    return error_code


def _run_test_binoption(compile_status: int, json_node: Dict) -> int:
    test_env = os.environ.copy()
    error_code = 0
    test_env["OMP_TARGET_OFFLOAD"] = "MANDATORY"
    result = {
        "Test simple binary options program with Intel® oneAPI Level Zero.": {
            "CheckResult": "",
            "CheckStatus": "PASS",
            "Command": f"OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=LEVEL0 {TMP_BINOPTION_FILE}"
        },
        "Test simple binary options program with OpenCL™.": {
            "CheckResult": "",
            "CheckStatus": "PASS",
            "Command": f"OMP_TARGET_OFFLOAD=MANDATORY LIBOMPTARGET_PLUGIN=OPENCL {TMP_BINOPTION_FILE}"
        }
    }
    if compile_status != 0:
        error_code += 1
        result["Test simple binary options program with Intel® oneAPI Level Zero."]["CheckStatus"] = "FAIL"
        result["Test simple binary options program with Intel® oneAPI Level Zero."]["Message"] = \
            "Check failed because compile test binoption failed."
        result["Test simple binary options program with Intel® oneAPI Level Zero."]["HowToFix"] = \
            "Check compiled source file for syntax errors."
        result["Test simple binary options program with OpenCL™."]["CheckStatus"] = "FAIL"
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
            result["Test simple binary options program with Intel® oneAPI Level Zero."]["CheckStatus"] = "FAIL"  # noqa: E501
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
            result["Test simple binary options program with OpenCL™."]["CheckStatus"] = "FAIL"
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


def _compile_simple_sycl_code(json_node: Dict) -> int:
    error_code = 0
    result = {"Compile simple SYCL code": {
        "CheckResult": "",
        "CheckStatus": "PASS",
        "Command": f"icpx -fsycl -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                   f"{PATH_TO_SOURCE_OFFLOAD}\\simple-sycl-code.cpp -o {TMP_SIMPLE_SYCL_CODE_FILE}"
    }}
    try:
        compile = subprocess.Popen(
            ["icpx", "-fsycl", "-fiopenmp", "-fopenmp-targets=spir64",
             "-D__STRICT_ANSI__ ", f"{PATH_TO_SOURCE_OFFLOAD}\\simple-sycl-code.cpp",
             "-o", TMP_SIMPLE_SYCL_CODE_FILE],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
        if compile.wait() != 0:
            error_code += 1
            result["Compile simple SYCL code"]["CheckStatus"] = "FAIL"
            result["Compile simple SYCL code"]["Message"] = \
                f"icpx -fsycl -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ " \
                f"{PATH_TO_SOURCE_OFFLOAD}\\simple-sycl-code.cpp " \
                f"-o {TMP_SIMPLE_SYCL_CODE_FILE}'"
            result["Compile simple SYCL code"]["HowToFix"] = \
                "Check compiled source file for syntax errors."
    except Exception:
        error_code += 1
        result["Compile simple SYCL code"]["CheckStatus"] = "ERROR"
        result["Compile simple SYCL code"]["Message"] = "SYCL code compilation failed - icpx compiler is not found."  # noqa E501
        result["Compile simple SYCL code"]["HowToFix"] = MISSING_COMPILER_MESSAGE
    json_node.update(result)
    return error_code


def _run_simple_sycl_code(compile_status: int, json_node: Dict) -> int:
    test_env = os.environ.copy()
    error_code = 0
    result = {
        "Test simple DPC++ program with Intel® oneAPI Level Zero.": {
            "CheckResult": "",
            "CheckStatus": "PASS",
            "Command": f"ONEAPI_DEVICE_SELECTOR=level_zero:gpu {TMP_SIMPLE_SYCL_CODE_FILE}"
        },
        "Test simple DPC++ program with OpenCL™.": {
            "CheckResult": "",
            "CheckStatus": "PASS",
            "Command": f"ONEAPI_DEVICE_SELECTOR=opencl:gpu {TMP_SIMPLE_SYCL_CODE_FILE}"
        }
    }
    if compile_status != 0:
        error_code += 1
        result["Test simple DPC++ program with Intel® oneAPI Level Zero."]["CheckStatus"] = "FAIL"
        result["Test simple DPC++ program with Intel® oneAPI Level Zero."]["Message"] = \
            "Check failed because compile simple SYCL code failed."
        result["Test simple DPC++ program with Intel® oneAPI Level Zero."]["HowToFix"] = \
            "Check compiled source file for syntax errors."
        result["Test simple DPC++ program with OpenCL™."]["CheckStatus"] = "FAIL"
        result["Test simple DPC++ program with OpenCL™."]["Message"] = \
            "Check failed because compile simple SYCL code failed."
        result["Test simple DPC++ program with OpenCL™."]["HowToFix"] = \
            "Check compiled source file for syntax errors."
    else:
        test_env["ONEAPI_DEVICE_SELECTOR"] = "level_zero:gpu"
        run_level_zero = subprocess.Popen(
            [TMP_SIMPLE_SYCL_CODE_FILE], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            encoding="utf-8", env=test_env)
        run_level_zero_stdout, _ = run_level_zero.communicate()
        if run_level_zero.returncode != 0 or run_level_zero_stdout.strip() != "PASSED":
            error_code += 1
            result["Test simple DPC++ program with Intel® oneAPI Level Zero."]["CheckStatus"] = "FAIL"
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

        test_env["ONEAPI_DEVICE_SELECTOR"] = "opencl:gpu"
        run_opencl = subprocess.Popen(
            [TMP_SIMPLE_SYCL_CODE_FILE], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            encoding="utf-8", env=test_env)
        run_opencl_stdout, _ = run_opencl.communicate()
        if run_opencl.returncode != 0 or run_opencl_stdout.strip() != "PASSED":
            error_code += 1
            result["Test simple DPC++ program with OpenCL™."]["CheckStatus"] = "FAIL"
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
        "CheckResult": "",
        "CheckStatus": "PASS",
        "Command": f"icpx -fsycl -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ "
                   f"{PATH_TO_SOURCE_OFFLOAD}\\parallel-for-1D.cpp -o {TMP_PARALLEL_FOR_1D_FILE}"
    }}
    try:
        compile = subprocess.Popen(
            ["icpx", "-fsycl", "-fiopenmp", "-fopenmp-targets=spir64",
             "-D__STRICT_ANSI__ ", f"{PATH_TO_SOURCE_OFFLOAD}\\simple-sycl-code.cpp",
             "-o", TMP_PARALLEL_FOR_1D_FILE],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
        if compile.wait() != 0:
            error_code += 1
            result["Compile parallel for program"]["CheckStatus"] = "FAIL"
            result["Compile parallel for program"]["Message"] = \
                f"icpx -fsycl -fiopenmp -fopenmp-targets=spir64 -D__STRICT_ANSI__ " \
                f"{PATH_TO_SOURCE_OFFLOAD}\\parallel-for-1D.cpp " \
                f"-o {TMP_PARALLEL_FOR_1D_FILE}"
            result["Compile parallel for program"]["HowToFix"] = \
                "Check compiled source file for syntax errors."
    except Exception:
        error_code += 1
        result["Compile parallel for program"]["CheckStatus"] = "ERROR"
        result["Compile parallel for program"]["Message"] = "Parallel code compilation failed - icpx compiler is not found."  # noqa
        result["Compile parallel for program"]["HowToFix"] = MISSING_COMPILER_MESSAGE
    json_node.update(result)
    return error_code


def _run_parallel_for_program(compile_status: int, json_node: Dict) -> int:
    test_env = os.environ.copy()
    error_code = 0
    result = {
        "Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero.": {
            "CheckResult": "",
            "CheckStatus": "PASS",
            "Command": f"ONEAPI_DEVICE_SELECTOR=level_zero:gpu {TMP_PARALLEL_FOR_1D_FILE}"
        },
        "Test simple DPC++ parallel-for program with OpenCL™.": {
            "CheckResult": "",
            "CheckStatus": "PASS",
            "Command": f"ONEAPI_DEVICE_SELECTOR=opencl:gpu {TMP_PARALLEL_FOR_1D_FILE}"
        }
    }
    if compile_status != 0:
        error_code += 1
        result["Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero."]["CheckStatus"] = "FAIL"   # noqa: E501
        result["Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero."]["Message"] = \
            "Check failed because compile parallel for program failed."
        result["Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero."]["HowToFix"] = \
            "Check compiled source file for syntax errors."
        result["Test simple DPC++ parallel-for program with OpenCL™."]["CheckStatus"] = "FAIL"
        result["Test simple DPC++ parallel-for program with OpenCL™."]["Message"] = \
            "Check failed because compile parallel for program failed."
        result["Test simple DPC++ parallel-for program with OpenCL™."]["HowToFix"] = \
            "Check compiled source file for syntax errors."
    else:
        test_env["ONEAPI_DEVICE_SELECTOR"] = "level_zero:gpu"
        run_level_zero = subprocess.Popen(
            [TMP_PARALLEL_FOR_1D_FILE], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            encoding="utf-8", env=test_env)
        run_level_zero_stdout, _ = run_level_zero.communicate()
        if run_level_zero.returncode != 0 or run_level_zero_stdout.strip() != "PASSED":
            error_code += 1
            result["Test simple DPC++ parallel-for program with Intel® oneAPI Level Zero."]["CheckStatus"] = "FAIL"   # noqa: E501
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

        test_env["ONEAPI_DEVICE_SELECTOR"] = "opencl:gpu"
        run_opencl = subprocess.Popen(
            [TMP_PARALLEL_FOR_1D_FILE], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            encoding="utf-8", env=test_env)
        run_opencl_stdout, _ = run_opencl.communicate()
        if run_opencl.returncode != 0 or run_opencl_stdout.strip() != "PASSED":
            error_code += 1
            result["Test simple DPC++ parallel-for program with OpenCL™."]["CheckStatus"] = "FAIL"
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
