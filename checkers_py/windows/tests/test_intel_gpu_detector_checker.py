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
import platform
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../'))

import unittest  # noqa: E402
from unittest.mock import patch  # noqa: E402

from checkers_py.windows import intel_gpu_detector_checker  # noqa: E402
from modules.check import CheckSummary, CheckMetadataPy  # noqa: E402


@unittest.skipIf(platform.system(
) == "Linux", "run on windows only")
class TestIntelGpuDetectorCheckerApiTest(unittest.TestCase):

    @patch("checkers_py.windows.intel_gpu_detector_checker.get_gpu_driver_info")
    def test_run_positive(self, mocked_get_gpu_driver_info):
        expected = CheckSummary

        mocked_get_gpu_driver_info.return_value = {
            "Check": {
                "CheckResult": "some data",
                "CheckStatus": "INFO"
            }
        }

        actual = intel_gpu_detector_checker.run_intel_gpu_detector_check({})

        self.assertIsInstance(actual, expected)

    def test_get_api_version_returns_str(self):
        expected = str

        actual = intel_gpu_detector_checker.get_api_version()

        self.assertIsInstance(actual, expected)

    def test_get_check_list_returns_list_metadata(self):
        expected = CheckMetadataPy

        check_list = intel_gpu_detector_checker.get_check_list()

        for metadata in check_list:
            self.assertIsInstance(metadata, expected)


@unittest.skipIf(platform.system(
) == "Linux", "run on windows only")
class TestGetGpuDriverInfo(unittest.TestCase):

    @patch("checkers_py.windows.intel_gpu_detector_checker.fetch_video_controllers")
    def test_one_video_controller(self, mocked_fetch_video_controllers):
        mocked_fetch_video_controllers.return_value = [{
            "Name": "Intel(R) Iris(R) Xe Graphics 1998",
            "Status": "OK",
            "Driver Version": "1.0.0",
            "PCI ID": "4040",
            "GPU type": "Integrated"
        }]
        expected = {
            "GPU information": {
                "CheckResult": {
                    "Intel GPU #1": {
                        "CheckResult": {
                            "Name": {
                                "CheckResult": "Intel(R) Iris(R) Xe Graphics 1998",
                                "CheckStatus": "INFO",
                            },
                            "Status": {
                                "CheckResult": "OK",
                                "CheckStatus": "INFO",
                            },
                            "Driver Version": {
                                "CheckResult": "1.0.0",
                                "CheckStatus": "INFO",
                            },
                            "PCI ID": {
                                "CheckResult": "4040",
                                "CheckStatus": "INFO",
                            },
                            "GPU type": {
                                "CheckResult": "Integrated",
                                "CheckStatus": "INFO",
                            }
                        },
                        "CheckStatus": "INFO"
                    }},
                "CheckStatus": "PASS"}
        }

        actual = intel_gpu_detector_checker.get_gpu_driver_info()
        self.assertEqual(expected, actual)

    @patch("checkers_py.windows.intel_gpu_detector_checker.fetch_video_controllers")
    def test_one_video_controller_exception(self, mocked_fetch_video_controllers):
        mocked_fetch_video_controllers.side_effect = Exception("Oops!")
        expected = {
            "GPU information": {
                "CheckResult": "Undefined",
                "CheckStatus": "ERROR",
                "Message": "Oops!",
                "HowToFix": "This error is unexpected. Please report the issue to "
                "Diagnostics Utility for oneAPI repository: "
                "https://github.com/intel/diagnostics-utility."}
        }
        actual = intel_gpu_detector_checker.get_gpu_driver_info()
        self.assertEqual(expected, actual)

    @patch("checkers_py.windows.intel_gpu_detector_checker.fetch_video_controllers")
    def test_two_video_controller(self, mocked_fetch_video_controllers):
        mocked_fetch_video_controllers.return_value = [{
            "Name": "Intel(R) Iris(R) Xe Graphics 1998",
            "Status": "OK",
            "Driver Version": "1.0.0",
            "PCI ID": "4040",
            "GPU type": "Integrated"
        }, {
            "Name": "Intel® Arc™ A-Series Graphics",
            "Status": "OK",
            "Driver Version": "1.0.0",
            "PCI ID": "56B3",
            "GPU type": "Discrete"}]
        expected = {
            "GPU information": {
                "CheckResult": {
                    "Intel GPU #1": {
                        "CheckResult": {
                            "Name": {
                                "CheckResult": "Intel(R) Iris(R) Xe Graphics 1998",
                                "CheckStatus": "INFO",
                            },
                            "Status": {
                                "CheckResult": "OK",
                                "CheckStatus": "INFO",
                            },
                            "Driver Version": {
                                "CheckResult": "1.0.0",
                                "CheckStatus": "INFO",
                            },
                            "PCI ID": {
                                "CheckResult": "4040",
                                "CheckStatus": "INFO",
                            },
                            "GPU type": {
                                "CheckResult": "Integrated",
                                "CheckStatus": "INFO",
                            }
                        },
                        "CheckStatus": "INFO"
                    },
                    "Intel GPU #2": {
                        "CheckResult": {
                            "Name": {
                                "CheckResult": "Intel® Arc™ A-Series Graphics",
                                "CheckStatus": "INFO",
                            },
                            "Status": {
                                "CheckResult": "OK",
                                "CheckStatus": "INFO",
                            },
                            "Driver Version": {
                                "CheckResult": "1.0.0",
                                "CheckStatus": "INFO",
                            },
                            "PCI ID": {
                                "CheckResult": "56B3",
                                "CheckStatus": "INFO",
                            },
                            "GPU type": {
                                "CheckResult": "Discrete",
                                "CheckStatus": "INFO",
                            }
                        },
                        "CheckStatus": "INFO"
                    }},
                "CheckStatus": "PASS"}
        }
        actual = intel_gpu_detector_checker.get_gpu_driver_info()
        self.assertEqual(expected, actual)

    @patch("checkers_py.windows.intel_gpu_detector_checker.fetch_video_controllers")
    def test_no_controllers(self, mocked_fetch_video_controllers):
        mocked_fetch_video_controllers.return_value = []
        expected = {
            "GPU information": {
                "CheckResult": "Undefined",
                "CheckStatus": "FAIL",
                "Message": "No Intel supported GPU detected."
                " Use of the Intel® oneAPI Toolkits is not supported."}
        }

        actual = intel_gpu_detector_checker.get_gpu_driver_info()
        self.assertEqual(expected, actual)


@unittest.skipIf(platform.system(
) == "Linux", "run on windows only")
class TestFetchVideoControllers(unittest.TestCase):

    @patch("checkers_py.windows.intel_gpu_detector_checker.run_powershell_command")
    def test_one_intel_controller(self, mocked_run_powershell_command):
        mocked_run_powershell_command.return_value = (
            "Name          : Intel(R) Iris(R) Xe Graphics 1998\n"
            "Status        : OK\nDriverVersion : 10.10.10.10\n"
            "PNPDeviceID   : PCI\\VEN_8086&DEV_9A49&SUBSYS_880D103C&REV_01\\3&11583659&0&10",
            "", 0)
        expected = [{
            "Name": "Intel(R) Iris(R) Xe Graphics 1998",
            "Status": "OK",
            "Driver Version": "10.10.10.10",
            "PCI ID": "9A49"
        }]
        actual = intel_gpu_detector_checker.fetch_video_controllers()
        self.assertEqual(expected, actual)

    @patch("checkers_py.windows.intel_gpu_detector_checker.run_powershell_command")
    def test_two_intel_controller(self, mocked_run_powershell_command):
        mocked_run_powershell_command.return_value = (
            "Name          : Intel(R) Iris(R) Xe Graphics 1998\n"
            "Status        : OK\nDriverVersion : 10.10.10.10\n"
            "PNPDeviceID   : PCI\\VEN_8086&DEV_9A49&SUBSYS_880D103C&REV_01\\3&11583659&0&10\n\n"
            "Name          : Intel® Arc™ A-Series Graphics\nStatus        : OK\n"
            "DriverVersion : 10.10\n"
            "PNPDeviceID   : some string without pci id", "", 0)
        expected = [{
            "Name": "Intel(R) Iris(R) Xe Graphics 1998",
            "Status": "OK",
            "Driver Version": "10.10.10.10",
            "PCI ID": "9A49"
        },
            {
            "Name": "Intel® Arc™ A-Series Graphics",
            "Status": "OK",
            "Driver Version": "10.10",
            "PCI ID": None
        }]
        actual = intel_gpu_detector_checker.fetch_video_controllers()
        self.assertEqual(expected, actual)

    @patch("checkers_py.windows.intel_gpu_detector_checker.run_powershell_command")
    def test_one_non_intel_controller(self, mocked_run_powershell_command):
        mocked_run_powershell_command.return_value = (
            "Name          : SOME CONTROLLER\n"
            "Status        : OK\nDriverVersion : 10.10.10.10\n"
            "PNPDeviceID   : PCI\\VEN_8086&DEV_9A49&SUBSYS_880D103C&REV_01\\3&11583659&0&10",
            "", 0)
        expected = []
        actual = intel_gpu_detector_checker.fetch_video_controllers()
        self.assertEqual(expected, actual)

    @patch("checkers_py.windows.intel_gpu_detector_checker.run_powershell_command")
    def test_one_intel_one_non_intel_controller(self, mocked_run_powershell_command):
        mocked_run_powershell_command.return_value = (
            "Name          : Intel(R) Iris(R) Xe Graphics 1998\n"
            "Status        : OK\nDriverVersion : 10.10.10.10\n"
            "PNPDeviceID   : PCI\\VEN_8086&DEV_9A49&SUBSYS_880D103C&REV_01\\3&11583659&0&10\n\n"
            "Name          : SOME CONTROLLER\nStatus        : OK\n"
            "DriverVersion : 10.10\n"
            "PNPDeviceID   : some string without pci id", "", 0)
        expected = [{
            "Name": "Intel(R) Iris(R) Xe Graphics 1998",
            "Status": "OK",
            "Driver Version": "10.10.10.10",
            "PCI ID": "9A49"
        }]
        actual = intel_gpu_detector_checker.fetch_video_controllers()
        self.assertEqual(expected, actual)

    @patch("checkers_py.windows.intel_gpu_detector_checker.run_powershell_command")
    def test_empty_run_powershell_command_output(self, mocked_run_powershell_command):
        mocked_run_powershell_command.return_value = ("", "", 0)
        expected = []
        actual = intel_gpu_detector_checker.fetch_video_controllers()
        self.assertEqual(expected, actual)

    @patch("checkers_py.windows.intel_gpu_detector_checker.run_powershell_command")
    def test_run_powershell_command_return_error(self, mocked_run_powershell_command):
        mocked_run_powershell_command.return_value = ("", "some error", 1)
        self.assertRaises(Exception, intel_gpu_detector_checker.fetch_video_controllers)


@unittest.skipIf(platform.system(
) == "Linux", "run on windows only")
class TestGetVideoControllerName(unittest.TestCase):

    def test_positive(self):
        video_controller = {"Name": "Intel(R) Iris(R) Xe Graphics"}
        expected = {
            "Name": {
                "CheckResult": "Intel(R) Iris(R) Xe Graphics",
                "CheckStatus": "INFO",
            }}
        actual = intel_gpu_detector_checker.get_video_controller_name(video_controller)
        self.assertEqual(expected, actual)


@unittest.skipIf(platform.system(
) == "Linux", "run on windows only")
class TestGetVideoControllerDriverVersion(unittest.TestCase):

    def test_positive(self):
        video_controller = {"Driver Version": "10.10.10"}
        expected = {
            "Driver Version": {
                "CheckResult": "10.10.10",
                "CheckStatus": "INFO",
            }}
        actual = intel_gpu_detector_checker.get_video_controller_driver_version(video_controller)
        self.assertEqual(expected, actual)


@unittest.skipIf(platform.system(
) == "Linux", "run on windows only")
class TestGetVideoControllerStatus(unittest.TestCase):

    def test_positive(self):
        video_controller = {"Status": "OK"}
        expected = {
            "Status": {
                "CheckResult": "OK",
                "CheckStatus": "INFO",
            }}
        actual = intel_gpu_detector_checker.get_video_controller_status(video_controller)
        self.assertEqual(expected, actual)


@unittest.skipIf(platform.system(
) == "Linux", "run on windows only")
class TestGetVideoControllerPciID(unittest.TestCase):

    def test_positive(self):
        video_controller = {"PCI ID": "4020"}
        expected = {
            "PCI ID": {
                "CheckResult": "4020",
                "CheckStatus": "INFO",
            }}
        actual = intel_gpu_detector_checker.get_video_controller_pci_id(video_controller)
        self.assertEqual(expected, actual)


@unittest.skipIf(platform.system(
) == "Linux", "run on windows only")
class TestGetGpuType(unittest.TestCase):

    def test_discrete(self):
        video_controller = {"PCI ID": "OBDA"}
        expected = {
            "GPU type": {
                "CheckResult": "Discrete",
                "CheckStatus": "INFO",
            }}
        actual = intel_gpu_detector_checker.get_gpu_type(video_controller)
        self.assertEqual(expected, actual)

    def test_integrated(self):
        video_controller = {"PCI ID": "9A49"}
        expected = {
            "GPU type": {
                "CheckResult": "Integrated",
                "CheckStatus": "INFO",
            }}
        actual = intel_gpu_detector_checker.get_gpu_type(video_controller)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.TestCase.maxDiff = None
    unittest.main()
