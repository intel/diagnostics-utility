#!/usr/bin/env python3
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

# NOTE: workaround to import modules
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../'))

import unittest  # noqa: E402
from unittest.mock import MagicMock, patch, mock_open  # noqa: E402

from checkers_py.linux import intel_gpu_detector_checker  # noqa: E402
from modules.check import CheckSummary, CheckMetadataPy  # noqa: E402


class TestIntelGpuDetectorCheckerApiTest(unittest.TestCase):

    @patch("checkers_py.linux.intel_gpu_detector_checker.get_gpu_info")
    def test_run_positive(self, mocked_get_gpu_info):
        expected = CheckSummary

        mocked_get_gpu_info.side_effect = lambda node: node.update({
            "Check": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })

        value = intel_gpu_detector_checker.run_intel_gpu_detector_check({})

        self.assertIsInstance(value, expected)

    def test_get_api_version_returns_str(self):
        expected = str

        value = intel_gpu_detector_checker.get_api_version()

        self.assertIsInstance(value, expected)

    def test_get_check_list_returns_list_metadata(self):
        expected = CheckMetadataPy

        value = intel_gpu_detector_checker.get_check_list()

        for metadata in value:
            self.assertIsInstance(metadata, expected)


class TestFunctionCmd(unittest.TestCase):

    @patch("subprocess.Popen")
    def test__function_cmd_positive(self, mocked_open):
        expected = 0, "test"
        process_mock = MagicMock()
        process_mock.communicate.return_value = (
            "test",
            None
        )
        process_mock.returncode = 0

        mocked_open.return_value = process_mock

        value = intel_gpu_detector_checker._function_cmd("ls")
        self.assertEqual(expected, value)


class TestGetI915DriverInfo(unittest.TestCase):

    @patch("subprocess.Popen")
    def test_get_i915_driver_loaded_info_positive(self, mocked_open):

        expected = {
            "Intel® Graphics Driver is loaded": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "lsmod | grep i915"
            }
        }
        lsmod_mock = MagicMock()
        lsmod_mock.wait.return_value = 0

        grep_mock = MagicMock()
        grep_mock.communicate.return_value = (
            "i915_spi               24576  0\n"
            "mtd                    69632  6 i915_spi\n"
            "i915                 2949120  4\n"
            "i2c_algo_bit           16384  1 i915\n"
            "drm_kms_helper        245760  1 i915\n"
            "cec                    53248  2 drm_kms_helper,i915\n"
            "drm                   548864  3 drm_kms_helper,i915\n"
            "video                  49152  1 i915\n",
            None
        )
        grep_mock.returncode = 0

        mocked_open.side_effect = [lsmod_mock, grep_mock]

        value = {}
        intel_gpu_detector_checker._get_i915_driver_loaded_info(value)

        self.assertEqual(expected, value)

    @patch("subprocess.Popen")
    def test_get_i915_driver_loaded_info_lsmod_return_code_is_not_zero(self, mocked_open):

        expected = {
            "Intel® Graphics Driver is loaded": {
                "Value": "",
                "RetVal": "ERROR",
                "Command": "lsmod | grep i915",
                "Message": "Cannot get information about kernel modules that are currently loaded.",
                "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."  # noqa E501
            }
        }
        lsmod_mock = MagicMock()
        lsmod_mock.wait.return_value = (None, None)
        lsmod_mock.returncode = 1

        mocked_open.return_value = lsmod_mock

        value = {}

        intel_gpu_detector_checker._get_i915_driver_loaded_info(value)

        self.assertEqual(expected, value)

    @patch("subprocess.Popen")
    def test_get_i915_driver_loaded_info_grep_return_code_is_not_zero_or_one(self, mocked_open):
        expected = {
            "Intel® Graphics Driver is loaded": {
                "Value": "",
                "RetVal": "ERROR",
                "Command": "lsmod | grep i915",
                "Message": "Cannot get information about whether the Intel® Graphics Driver is loaded.",
                "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."  # noqa E501
            }
        }

        lsmod_mock = MagicMock()
        lsmod_mock.wait.return_value = 0

        grep_mock = MagicMock()
        grep_mock.communicate.return_value = (None, None)
        grep_mock.returncode = 2

        mocked_open.side_effect = [lsmod_mock, grep_mock]

        value = {}
        intel_gpu_detector_checker._get_i915_driver_loaded_info(value)

        self.assertEqual(expected, value)

    @patch("subprocess.Popen")
    def test_get_i915_driver_loaded_info_grep_return_empty_line(self, mocked_open):

        expected = {
            "Intel® Graphics Driver is loaded": {
                "Value": "",
                "RetVal": "FAIL",
                "Command": "lsmod | grep i915",
                "Message": "Module i915 is not loaded.",
                "HowToFix": "Try to load i915 module with the following command: modprobe i915.",
                "AutomationFix": "modprobe i915"
            }
        }
        lsmod_mock = MagicMock()
        lsmod_mock.wait.return_value = 0

        grep_mock = MagicMock()
        grep_mock.communicate.return_value = (
            "",
            None
        )
        grep_mock.returncode = 0

        mocked_open.side_effect = [lsmod_mock, grep_mock]

        value = {}
        intel_gpu_detector_checker._get_i915_driver_loaded_info(value)

        self.assertEqual(expected, value)

    @patch("subprocess.Popen", side_effect=Exception("test message"))
    def test_get_i915_driver_loaded_info_subprocess_raise_exception(self, mocked_open):

        expected = {
            "Intel® Graphics Driver is loaded": {
                "Value": "",
                "RetVal": "ERROR",
                "Command": "lsmod | grep i915",
                "Message": "test message",
                "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."  # noqa E501
            }
        }
        value = {}
        intel_gpu_detector_checker._get_i915_driver_loaded_info(value)

        self.assertEqual(expected, value)


class TestGetTopologyPath(unittest.TestCase):

    @patch("os.path.relpath", return_value="0000:03:00.0")
    def test__get_topology_path_positive(self, mocked_open):
        expected = {
            "PCI bus-tree": {
                "Value": "0000:03:00.0",
                "RetVal": "INFO",
                "Verbosity": 1,
                "Command": "readlink /sys/bus/pci/devices/03:00.0"
            },
        }

        value = {}
        intel_gpu_detector_checker._get_topology_path(value, "03:00.0")
        self.assertEqual(expected, value)


class TestGetTileCount(unittest.TestCase):

    @patch("subprocess.Popen")
    def test__get_tile_count_positive_one(self, mocked_open):
        expected = {
            "Tile count": {
                "Value": 1,
                "Verbosity": 1,
                "RetVal": "INFO",
                "Command": "ls path | grep -i 'gt[0-9]$' | wc -l",
            }
        }

        ls_mock = MagicMock()
        ls_mock.wait.return_value = 0

        grep_mock = MagicMock()
        grep_mock.communicate.return_value = ("gt0", None)
        grep_mock.returncode = 0

        mocked_open.side_effect = [ls_mock, grep_mock]

        value = {}
        path = "path"
        intel_gpu_detector_checker._get_tile_count(value, path)

        self.assertEqual(expected, value)

    @patch("subprocess.Popen")
    def test__get_tile_count_positive_two(self, mocked_open):
        expected = {
            "Tile count": {
                "Value": 2,
                "Verbosity": 1,
                "RetVal": "INFO",
                "Command": "ls path | grep -i 'gt[0-9]$' | wc -l",
            }
        }

        ls_mock = MagicMock()
        ls_mock.wait.return_value = 0

        grep_mock = MagicMock()
        grep_mock.communicate.return_value = ("gt0\ngt1", None)
        grep_mock.returncode = 0

        mocked_open.side_effect = [ls_mock, grep_mock]

        value = {}
        path = "path"
        intel_gpu_detector_checker._get_tile_count(value, path)

        self.assertEqual(expected, value)

    @patch("subprocess.Popen")
    def test__get_tile_count_grep_return_code_is_not_zero_or_one(self, mocked_open):
        expected = {
            "Tile count": {
                "Value": "Undefined",
                "Verbosity": 0,
                "RetVal": "ERROR",
                "Command": "ls path | grep -i 'gt[0-9]$' | wc -l",
                "Message": "Cannot get information to determine tiles count."
                           "'grep' command returned error code 2.",
                "HowToFix": "There is not a known solution for this error."
            }
        }
        ls_mock = MagicMock()
        ls_mock.wait.return_value = 0

        grep_mock = MagicMock()
        grep_mock.communicate.return_value = (None, None)
        grep_mock.returncode = 2

        mocked_open.side_effect = [ls_mock, grep_mock]

        value = {}
        path = "path"
        intel_gpu_detector_checker._get_tile_count(value, path)

        self.assertEqual(expected, value)

    @patch("subprocess.Popen")
    def test__get_tile_count_ls_return_code_is_not_zero(self, mocked_open):
        expected = {
            "Tile count": {
                "Value": "Undefined",
                "Verbosity": 0,
                "RetVal": "ERROR",
                "Command": "ls path | grep -i 'gt[0-9]$' | wc -l",
                "Message": "Cannot list information about the FILEs in directory: path. "
                           "'ls' command returned error code 1.",
                "HowToFix": "There is not a known solution for this error."
            }
        }

        process = MagicMock()
        process.wait.return_value = (None, None)
        process.returncode = 1
        mocked_open.return_value = process
        value = {}
        path = "path"
        intel_gpu_detector_checker._get_tile_count(value, path)

        self.assertEqual(expected, value)

    @patch("subprocess.Popen", side_effect=Exception("test message"))
    def test__get_tile_count_subprocess_raise_exception(self, mocked_open):
        expected = {
            "Tile count": {
                "Value": "Undefined",
                "Verbosity": 0,
                "RetVal": "ERROR",
                "Command": "ls path | grep -i 'gt[0-9]$' | wc -l",
                "Message": "test message",
                "HowToFix": "There is not a known solution for this error."
            }


        }

        value = {}
        path = "path"
        intel_gpu_detector_checker._get_tile_count(value, path)

        self.assertEqual(expected, value)


class TestCountInitializedGPU(unittest.TestCase):

    @patch("checkers_py.linux.intel_gpu_detector_checker._function_cmd", return_value=(0, "file1\nfile2\n"))
    def test__count_initializedGPU_positive_zero(self, mocked_function_cmd):
        expected = 0
        value = intel_gpu_detector_checker._count_initializedGPU()
        self.assertEqual(expected, value)

    @patch("checkers_py.linux.intel_gpu_detector_checker._function_cmd",
           return_value=(0, "file\nrender128\n"))
    def test__count_initializedGPU_positive_one(self, mocked_function_cmd):
        expected = 1
        value = intel_gpu_detector_checker._count_initializedGPU()
        self.assertEqual(expected, value)

    @patch("checkers_py.linux.intel_gpu_detector_checker._function_cmd",
           return_value=(0, "render128\nrender129\n"))
    def test__count_initializedGPU_positive_two(self, mocked_function_cmd):
        expected = 2
        value = intel_gpu_detector_checker._count_initializedGPU()
        self.assertEqual(expected, value)


class TestCheckGPUInfoPath(unittest.TestCase):

    @patch("os.access", return_value=True)
    @patch("os.walk", return_value=[("/0", (), ("test1", "test2")), ("/1", (), ("test3", "i915_gpu_info"))])
    def test__check_gpu_info_path_permissions_positive(self, mocked_access, mocked_walk):
        expected = ["/1"]

        value = intel_gpu_detector_checker._check_gpu_info_path()
        value_list = list(value)
        self.assertEqual(expected, value_list)

    @patch("os.access", return_value=False)
    def test__check_gpu_info_path_permissions_negative(self, mocked_access):
        expected_msg = "Unable to get information about initialized devices because "
        "the user doesn't have read access to /sys/kernel/debug/dri/. "
        "Try to run the diagnostics with administrative priviliges."

        with self.assertRaisesRegex(Exception, expected_msg):
            intel_gpu_detector_checker._check_gpu_info_path()


class TestGetInitializedGPU(unittest.TestCase):

    @patch("checkers_py.linux.intel_gpu_detector_checker._get_tile_count")
    @patch("checkers_py.linux.intel_gpu_detector_checker._get_topology_path")
    @patch("builtins.open", new_callable=mock_open, read_data="PCI ID          : 0x4905\n"
                                                              "EU total        : 96\n"
                                                              "Platform        : DG1\n"
                                                              "GuC firmware    : dg1_guc_62.0.3.bin\n"
                                                              "HuC firmware    : dg1_huc_7.9.3.bin\n"
                                                              "is_dgfx         : yes\n")
    @patch("checkers_py.linux.intel_gpu_detector_checker._check_gpu_info_path")
    def test__get_initializedGPU_positive(self, mocked_gpu_info_path, mocked_open, mocked_topology_path,
                                          mocked_tile_count):
        expected = {"Intel GPU #1": {
                        "Value": {
                            "GPU id": {
                                "Value": "0x4905",
                                "RetVal": "INFO",
                                "Command": "cat /sys/kernel/debug/dri/0/i915_gpu_info | grep -i 'pci id' | "
                                           "awk '{print $3}'"
                            },
                            "Bus info": {
                                "Value": "0000:03:00.0",
                                "RetVal": "INFO",
                                "Verbosity": 1,
                                "Command": "cat /sys/kernel/debug/dri/0/name | awk '{print $2}'"
                            },
                            "EU Counts": {
                                "Value": "96",
                                "RetVal": "INFO",
                                "Verbosity": 1,
                                "Command": "cat /sys/kernel/debug/dri/0/i915_gpu_info | grep -i 'EU total' | "
                                           "awk '{print $3}'"
                            },
                            "Platform": {
                                "Value": "DG1",
                                "RetVal": "INFO",
                                "Verbosity": 1,
                                "Command": "cat /sys/kernel/debug/dri/0/i915_gpu_info | grep -i '^platform' |"
                                           " awk '{print $2}' | uniq"
                            },
                            "GuC firmware": {
                                "Value": "dg1_guc_62.0.3.bin",
                                "RetVal": "INFO",
                                "Verbosity": 1,
                                "Command": "cat /sys/kernel/debug/dri/0/i915_gpu_info | "
                                           "grep -i 'GuC firmware' | awk '{print $3}' | xargs basename"
                            },
                            "HuC firmware": {
                                "Value": "dg1_huc_7.9.3.bin",
                                "RetVal": "INFO",
                                "Verbosity": 1,
                                "Command": "cat /sys/kernel/debug/dri/0/i915_gpu_info | "
                                "grep -i 'HuC firmware' | awk '{print $3}' | xargs basename"

                            },
                            "GPU type": {
                                "Value": "Discrete",
                                "RetVal": "INFO",
                                "Verbosity": 1,
                                "Command": "cat /sys/kernel/debug/dri/0/i915_gpu_info | grep -i 'is_dgfx' | "
                                           "awk '{print $0}'"
                            },
                            "PCI bus-tree": {
                                "Value": "0000:03:00.0",
                                "RetVal": "INFO",
                                "Verbosity": 1,
                                "Command": "readlink link"
                            },
                            "Tile count": {
                                "Value": 1,
                                "RetVal": "INFO",
                                "Verbosity": 1,
                                "Command": "ls path | grep -i 'gt[0-9]$' | wc -l"
                            }
                        },
                        "RetVal": "INFO"
                    }}

        paths = ["/sys/kernel/debug/dri/0"]
        mocked_gpu_info_path.return_value = filter(None, paths)

        handlers = (mocked_open.return_value, mock_open(read_data="i915 dev=0000:03:00.0").return_value, )
        mocked_open.side_effect = handlers

        mocked_topology_path.side_effect = lambda node, _: node.update({
            "PCI bus-tree": {
                "Value": "0000:03:00.0",
                "RetVal": "INFO",
                "Verbosity": 1,
                "Command": "readlink link"
            }
        })
        mocked_tile_count.side_effect = lambda node, _: node.update({
            "Tile count": {
                "Value": 1,
                "RetVal": "INFO",
                "Verbosity": 1,
                "Command": "ls path | grep -i 'gt[0-9]$' | wc -l"
            }
        })
        value = {}
        intel_gpu_detector_checker._get_initializedGPU(value)
        self.assertEqual(expected, value)


class TestCountUninitializedGPU(unittest.TestCase):

    @patch("checkers_py.linux.intel_gpu_detector_checker._function_cmd")
    @patch("checkers_py.linux.intel_gpu_detector_checker.exists", return_value=True)
    def test__count_uninitializedGPU_with_sbin_lspci(self, mocked_exists, mocked__fuction_cmd):
        expected = 1

        def side_effect(*args, **kwargs):
            if args[0] == ["/sbin/lspci"]:
                return 0,  "03:00.0 VGA compatible controller: Intel Corporation Device 4905 (rev 01)\n"
            elif args[0] == ["lspci"]:
                return 1, "test"
            else:
                return 1, "test2"

        mocked__fuction_cmd.side_effect = side_effect
        value = intel_gpu_detector_checker._count_uninitializedGPU()

        self.assertEqual(expected, value)

    @patch("checkers_py.linux.intel_gpu_detector_checker._function_cmd")
    @patch("checkers_py.linux.intel_gpu_detector_checker.exists", return_value=False)
    def test__count_uninitializedGPU_without_sbin_lspci(self, mocked_exists, mocked__fuction_cmd):
        expected = 1

        def side_effect(*args, **kwargs):
            if args[0] == ["/sbin/lspci"]:
                return 1, "test"
            elif args[0] == ["lspci"]:
                return 0, "03:00.0 VGA compatible controller: Intel Corporation Device 4905 (rev 01)\n"
            else:
                return 1, "test2"

        mocked__fuction_cmd.side_effect = side_effect

        value = intel_gpu_detector_checker._count_uninitializedGPU()

        self.assertEqual(expected, value)

    @patch("checkers_py.linux.intel_gpu_detector_checker._function_cmd", return_value=(1, "test"))
    @patch("checkers_py.linux.intel_gpu_detector_checker.exists", return_value=True)
    def test__count_uninitializedGPU_raise_exception(self, mocked_exists, mocked__fuction_cmd):

        expected_msg = "Cannot get information about GPU(s)."

        with self.assertRaises(Exception) as msg:
            intel_gpu_detector_checker._count_uninitializedGPU()

        self.assertEqual(expected_msg, str(msg.exception))


class TestGetUninitializedGPU(unittest.TestCase):

    @patch("checkers_py.linux.intel_gpu_detector_checker._function_cmd")
    @patch("checkers_py.linux.intel_gpu_detector_checker.exists", return_value=True)
    @patch("os.access", return_value=True)
    def test__get_uninitializedGPU_without_initialized(self, mocked_access, mocked_exists,
                                                       mocked__function_cmd):
        expected_count = 1
        expected_value = {
            "Intel GPU #1": {
                "Value": {
                    "Bus info": {
                        "Value":  "03:00.0",
                        "RetVal": "INFO"
                    },
                    "Name": {
                        "Value": "VGA compatible controller: "
                                 "Intel Corporation Device 4905 (rev 01)",
                        "RetVal": "INFO"
                    },
                },
                "RetVal": "INFO",
                "Command": 'lspci | grep -e "VGA compatible controller" -e "Display controller"'
                           ' | grep -i "Intel Corporation"'
            }
        }
        mocked__function_cmd.return_value = (
            0,
            "03:00.0 VGA compatible controller: Intel Corporation Device 4905 (rev 01)\n"
        )
        value = {}
        count = intel_gpu_detector_checker._get_uninitializedGPU([], value)
        self.assertEqual(expected_count, count)
        self.assertEqual(expected_value, value)

    @patch("checkers_py.linux.intel_gpu_detector_checker._function_cmd", return_value=(1, "test"))
    @patch("checkers_py.linux.intel_gpu_detector_checker.exists", return_value=True)
    @patch("os.access", return_value=True)
    def test__get_uninitializedGPU_raise_exception(self, mocked_access, mocked_exists,
                                                   mocked__function_cmd):
        expected_msg = "Cannot get information about GPU(s)."

        with self.assertRaises(Exception) as msg:
            intel_gpu_detector_checker._get_uninitializedGPU([], {})

        self.assertEqual(expected_msg, str(msg.exception))

    @patch("os.access", return_value=False)
    def test__get_uninitializedGPU_permissions_negative(self, mocked_access):
        expected_msg = "Unable to get information about uninitialized devices because "
        "the user doesn't have read access to /sys/kernel/debug/dri/."

        with self.assertRaisesRegex(Exception, expected_msg):
            intel_gpu_detector_checker._get_uninitializedGPU([], {})


class TestGetGpuInfo(unittest.TestCase):

    @patch("checkers_py.linux.intel_gpu_detector_checker._get_i915_driver_loaded_info")
    @patch("checkers_py.linux.intel_gpu_detector_checker._count_initializedGPU", return_value=1)
    @patch("checkers_py.linux.intel_gpu_detector_checker._count_uninitializedGPU", return_value=1)
    @patch("checkers_py.linux.intel_gpu_detector_checker._get_initializedGPU")
    def test_get_gpu_info_run_positive_without_uninitialized(self,
                                                             mocked__get_initializedGPU,
                                                             mocked__count_uninitializedGPU,
                                                             mocked__count_initializedGPU,
                                                             mocked__get_i915_driver_loaded_info):
        expected = {
            "GPU information": {
                "RetVal": "INFO",
                "Value": {
                    "Intel® Graphics Driver is loaded": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "lsmod | grep i915"
                    },
                    "Intel GPU(s) is present on the bus": {
                        "RetVal": "PASS",
                        "Value": ""
                    },
                    "Number of Intel GPU(s) on the system": {
                        "RetVal": "INFO",
                        "Value": 1
                    },
                    "Initialized devices": {
                        "Value": {
                            "Intel GPU #1": {
                                "Value": {
                                    "GPU id": {
                                        "Value": "0x4905",
                                        "RetVal": "INFO",
                                        "Command": "cat path/i915_gpu_info | grep -i 'pci id' | "
                                                   "awk '{print $3}'"
                                    },
                                    "Bus info": {
                                        "Value": "0000:03:00.0",
                                        "RetVal": "INFO",
                                        "Verbosity": 1,
                                        "Command": "cat path/name | awk '{print $2}'"
                                    },
                                    "EU Counts": {
                                        "Value": 96,
                                        "RetVal": "INFO",
                                        "Verbosity": 1,
                                        "Command": "cat path/i915_gpu_info | grep -i 'EU total' | "
                                                   "awk '{print $3}'"
                                    },
                                    "Platform": {
                                        "Value": "DG1",
                                        "RetVal": "INFO",
                                        "Verbosity": 1,
                                        "Command": "cat path/i915_gpu_info | grep -i '^platform' | "
                                                   "awk '{print $2}' | uniq"
                                    },
                                    "GuC firmware": {
                                        "Value": "dg1_guc_62.0.3.bin",
                                        "RetVal": "INFO",
                                        "Verbosity": 1,
                                        "Command": "cat path/i915_gpu_info | grep -i 'GuC firmware' |"
                                                   " awk '{print $3}' | xargs basename"
                                    },
                                    "HuC firmware": {
                                        "Value": "dg1_huc_7.9.3.bin",
                                        "RetVal": "INFO",
                                        "Verbosity": 1,
                                        "Command": "cat path/i915_gpu_info | grep -i 'HuC firmware' |"
                                        " awk '{print $3}' | xargs basename"

                                    },
                                    "PCI bus-tree": {
                                        "Value": "0000:03:00.0",
                                        "RetVal": "INFO",
                                        "Verbosity": 1,
                                        "Command": "readlink link"
                                    },
                                    "Tile count": {
                                        "Value": 1,
                                        "RetVal": "INFO",
                                        "Verbosity": 1,
                                        "Command": "ls path | grep -i 'gt[0-9]$' | wc -l"
                                    }
                                },
                                "RetVal": "INFO"
                            },
                        },
                        "RetVal": "INFO"
                    }
                },

            }
        }

        mocked__get_i915_driver_loaded_info.side_effect = lambda node: node.update({
            "Intel® Graphics Driver is loaded": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "lsmod | grep i915"
            }

        })

        mocked__get_initializedGPU.side_effect = lambda node: node.update({
            "Intel GPU #1": {
                "Value": {
                    "GPU id": {
                        "Value": "0x4905",
                        "RetVal": "INFO",
                        "Command": "cat path/i915_gpu_info | grep -i 'pci id' | "
                                   "awk '{print $3}'"
                    },
                    "Bus info": {
                        "Value": "0000:03:00.0",
                        "RetVal": "INFO",
                        "Verbosity": 1,
                        "Command": "cat path/name | awk '{print $2}'"
                    },
                    "EU Counts": {
                        "Value": 96,
                        "RetVal": "INFO",
                        "Verbosity": 1,
                        "Command": "cat path/i915_gpu_info | grep -i 'EU total' | "
                                   "awk '{print $3}'"
                    },
                    "Platform": {
                        "Value": "DG1",
                        "RetVal": "INFO",
                        "Verbosity": 1,
                        "Command": "cat path/i915_gpu_info | grep -i '^platform' | "
                                   "awk '{print $2}' | uniq"
                    },
                    "GuC firmware": {
                        "Value": "dg1_guc_62.0.3.bin",
                        "RetVal": "INFO",
                        "Verbosity": 1,
                        "Command": "cat path/i915_gpu_info | grep -i 'GuC firmware' |"
                                   " awk '{print $3}' | xargs basename"
                    },
                    "HuC firmware": {
                        "Value": "dg1_huc_7.9.3.bin",
                        "RetVal": "INFO",
                        "Verbosity": 1,
                        "Command": "cat path/i915_gpu_info | grep -i 'HuC firmware' |"
                        " awk '{print $3}' | xargs basename"

                    },
                    "PCI bus-tree": {
                        "Value": "0000:03:00.0",
                        "RetVal": "INFO",
                        "Verbosity": 1,
                        "Command": "readlink link"
                    },
                    "Tile count": {
                        "Value": 1,
                        "RetVal": "INFO",
                        "Verbosity": 1,
                        "Command": "ls path | grep -i 'gt[0-9]$' | wc -l"
                    }
                },
                "RetVal": "INFO"
            }

        })

        value = {}
        intel_gpu_detector_checker.get_gpu_info(value)
        self.assertEqual(expected, value)

    @patch("checkers_py.linux.intel_gpu_detector_checker._get_i915_driver_loaded_info")
    @patch("checkers_py.linux.intel_gpu_detector_checker._count_initializedGPU", return_value=0)
    @patch("checkers_py.linux.intel_gpu_detector_checker._count_uninitializedGPU", return_value=1)
    @patch("checkers_py.linux.intel_gpu_detector_checker._get_uninitializedGPU")
    def test_get_gpu_info_run_positive_without_initialized(self,
                                                           mocked__get_uninitializedGPU,
                                                           mocked__count_uninitializedGPU,
                                                           mocked__count_initializedGPU,
                                                           mocked__get_i915_driver_loaded_info):
        expected = {
            "GPU information": {
                "RetVal": "INFO",
                "Value": {
                    "Intel® Graphics Driver is loaded": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "lsmod | grep i915"
                    },
                    "Intel GPU(s) is present on the bus": {
                        "RetVal": "PASS",
                        "Value": ""
                    },
                    "Number of Intel GPU(s) on the system": {
                        "RetVal": "INFO",
                        "Value": 1
                    },
                    "Uninitialized devices": {
                        "Value": {
                             "Intel GPU #1": {
                                "Value": {
                                    "Bus info": {
                                        "Value":  "03:00.0",
                                        "RetVal": "INFO"
                                    },
                                    "Name": {
                                        "Value": "VGA compatible controller: "
                                                 "Intel Corporation Device 4905 (rev 01)",
                                        "RetVal": "INFO"
                                    },
                                },
                                "RetVal": "INFO",
                                "Command": 'lspci | grep -e "VGA compatible controller" '
                                           '-e "Display controller" | grep -i "Intel Corporation"'
                             }
                        },
                        "RetVal": "ERROR",
                        "Message": "Some GPU(s) are not initialized.",
                        "HowToFix": "To initialize GPU(s), please run the following command: "
                                    "modprobe i915.",
                        "AutomationFix": "modprobe i915"
                    }
                }
            }
        }

        mocked__get_i915_driver_loaded_info.side_effect = lambda node: node.update({
            "Intel® Graphics Driver is loaded": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "lsmod | grep i915"
            }

        })

        mocked__get_uninitializedGPU.side_effect = lambda _, node: node.update({
            "Intel GPU #1": {
                "Value": {
                    "Bus info": {
                        "Value":  "03:00.0",
                        "RetVal": "INFO"
                    },
                    "Name": {
                        "Value": "VGA compatible controller: "
                                 "Intel Corporation Device 4905 (rev 01)",
                        "RetVal": "INFO"
                    },
                },
                "RetVal": "INFO",
                "Command": 'lspci | grep -e "VGA compatible controller" '
                           '-e "Display controller" | grep -i "Intel Corporation"'
                }
        })

        value = {}
        intel_gpu_detector_checker.get_gpu_info(value)
        self.assertEqual(expected, value)

    @patch("checkers_py.linux.intel_gpu_detector_checker._get_i915_driver_loaded_info")
    @patch("checkers_py.linux.intel_gpu_detector_checker._count_initializedGPU", return_value=0)
    @patch("checkers_py.linux.intel_gpu_detector_checker._count_uninitializedGPU", return_value=0)
    @patch("checkers_py.linux.intel_gpu_detector_checker._get_uninitializedGPU")
    def test_get_gpu_info_without_initialized_and_uninitialized(self,
                                                                mocked__get_uninitializedGPU,
                                                                mocked__count_uninitializedGPU,
                                                                mocked__count_initializedGPU,
                                                                mocked__get_i915_driver_loaded_info):

        expected = {
            "GPU information": {
                "RetVal": "INFO",
                "Value": {
                    "Intel® Graphics Driver is loaded": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "lsmod | grep i915"
                    },
                    "Intel GPU(s) is present on the bus": {
                        "RetVal": "FAIL",
                        "Message": "There are no Intel GPU(s) on the system.",
                        "HowToFix": "Plug Intel GPU(s) into an empty PCI slot.",
                        "Value": ""
                    }
                }
            }
        }

        mocked__get_i915_driver_loaded_info.side_effect = lambda node: node.update({
            "Intel® Graphics Driver is loaded": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "lsmod | grep i915"
            }

        })

        value = {}
        intel_gpu_detector_checker.get_gpu_info(value)

        self.assertEqual(expected, value)

    @patch("checkers_py.linux.intel_gpu_detector_checker._get_i915_driver_loaded_info")
    @patch("checkers_py.linux.intel_gpu_detector_checker._count_initializedGPU", return_value=0)
    @patch("checkers_py.linux.intel_gpu_detector_checker._count_uninitializedGPU", return_value=1)
    @patch("checkers_py.linux.intel_gpu_detector_checker._get_uninitializedGPU",
           side_effect=Exception('test message'))
    def test_get_gpu_info_without_initialized_and_with_uninitialized_exception(self,
                                                                               mocked__get_uninitializedGPU,
                                                                               mocked__count_uninitializedGPU,
                                                                               mocked__count_initializedGPU,
                                                                               mocked__get_i915_driver_loaded_info):  # noqa E501 

        expected = {
            "GPU information": {
                "RetVal": "INFO",
                "Value": {
                    "Intel® Graphics Driver is loaded": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "lsmod | grep i915"
                    },
                    "Intel GPU(s) is present on the bus": {
                        "RetVal": "PASS",
                        "Value": ""
                    },
                    "Number of Intel GPU(s) on the system": {
                        "RetVal": "INFO",
                        "Value": 1
                    },
                    "Uninitialized devices": {
                        "Value": "",
                        "RetVal": "ERROR",
                        "Message": "test message",
                        "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."  # noqa E501
                    }
                }
            }
        }

        mocked__get_i915_driver_loaded_info.side_effect = lambda node: node.update({
            "Intel® Graphics Driver is loaded": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "lsmod | grep i915"
            }

        })

        value = {}
        intel_gpu_detector_checker.get_gpu_info(value)
        self.assertEqual(expected, value)

    @patch("checkers_py.linux.intel_gpu_detector_checker._get_i915_driver_loaded_info")
    @patch("checkers_py.linux.intel_gpu_detector_checker._count_initializedGPU", return_value=1)
    @patch("checkers_py.linux.intel_gpu_detector_checker._count_uninitializedGPU", return_value=1)
    @patch("checkers_py.linux.intel_gpu_detector_checker._get_initializedGPU",
           side_effect=Exception('test message'))
    def test_get_gpu_info_with_initialized_exception_without_uninitialized(self,
                                                                           mocked__get_initializedGPU,
                                                                           mocked__count_uninitializedGPU,
                                                                           mocked__count_initializedGPU,
                                                                           mocked__get_i915_driver_loaded_info):  # noqa E501 
        expected = {
            "GPU information": {
                "RetVal": "INFO",
                "Value": {
                    "Intel® Graphics Driver is loaded": {
                        "Value": "",
                        "RetVal": "PASS",
                        "Command": "lsmod | grep i915"
                    },
                    "Intel GPU(s) is present on the bus": {
                        "RetVal": "PASS",
                        "Value": ""
                    },
                    "Number of Intel GPU(s) on the system": {
                        "RetVal": "INFO",
                        "Value": 1
                    },
                    "Initialized devices": {
                        "Value": "",
                        "RetVal": "ERROR",
                        "Message": "test message",
                        "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility."  # noqa E501
                    }
                }
            }
        }

        mocked__get_i915_driver_loaded_info.side_effect = lambda node: node.update({
            "Intel® Graphics Driver is loaded": {
                "Value": "",
                "RetVal": "PASS",
                "Command": "lsmod | grep i915"
            }

        })

        value = {}
        intel_gpu_detector_checker.get_gpu_info(value)
        self.assertEqual(expected, value)


if __name__ == '__main__':
    unittest.TestCase.maxDiff = None
    unittest.main()
