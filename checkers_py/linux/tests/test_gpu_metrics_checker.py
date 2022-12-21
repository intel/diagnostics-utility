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
import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../'))

import unittest  # noqa: E402
from unittest.mock import MagicMock, patch  # noqa: E402

from checkers_py.linux import gpu_metrics_checker  # noqa: E402
from modules.check import CheckSummary, CheckMetadataPy  # noqa: E402


class TestCheckGPUInfoPath(unittest.TestCase):

    @patch("os.access", return_value=False)
    def test__get_permissions_negative(self, mocked_access):
        expected_msg = "Unable to get information about uninitialized devices because "
        "the user does not have read access to /sys/kernel/debug/dri/."

        with self.assertRaisesRegex(Exception, expected_msg):
            gpu_metrics_checker.have_administrative_priviliges()


class TestGpuMetricsCheckerApiTest(unittest.TestCase):

    @patch("checkers_py.linux.gpu_metrics_checker.have_administrative_priviliges")
    @patch("checkers_py.linux.gpu_metrics_checker.parse_devices", return_value=["Device 1", "Device 2"])
    @patch("checkers_py.linux.gpu_metrics_checker.process_device")
    @patch("checkers_py.linux.gpu_metrics_checker.timeout_in_gpu_backend_check_occurred", return_value=False)
    def test_run_positive(self, mocked_timeout_in_gpu_backend_check_occurred, mocked_process_device,
                          mocked_parse_devices, mocked_have_administrative_priviliges):
        expected = CheckSummary

        mocked_process_device.side_effect = lambda node, device: node.update({
            device: {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })

        value = gpu_metrics_checker.run_gpu_metrics_check({})

        self.assertIsInstance(value, expected)
        self.assertEqual(value.error_code, 0)

    @patch("checkers_py.linux.gpu_metrics_checker.have_administrative_priviliges")
    @patch("checkers_py.linux.gpu_metrics_checker.parse_devices", return_value=[])
    @patch("checkers_py.linux.gpu_metrics_checker.timeout_in_gpu_backend_check_occurred", return_value=False)
    def test_run_parsed_no_devices(self, mocked_timeout_in_gpu_backend_check_occurred, mocked_parse_devices,
                                   mocked_have_administrative_priviliges):
        expected_type = CheckSummary
        expected_error_code = 3
        expected_message = "Level Zero driver did not provide information about GPUs."

        value = gpu_metrics_checker.run_gpu_metrics_check({})

        self.assertIsInstance(value, expected_type)
        self.assertEqual(value.error_code, expected_error_code)
        result = json.loads(value.result)
        self.assertEqual(result['Value']["GPU metrics check"]["Message"], expected_message)

    @patch("checkers_py.linux.gpu_metrics_checker.have_administrative_priviliges")
    @patch("checkers_py.linux.gpu_metrics_checker.timeout_in_gpu_backend_check_occurred", return_value=True)
    def test_run_timeout_occured(self, mocked_timeout_in_gpu_backend_check_occurred,
                                 mocked_have_administrative_priviliges):
        expected_type = CheckSummary
        expected_error_code = 3
        expected_message = "The GPU backend check failed or timed out. You may see irrelevant GPU "\
                           "information as a result."

        value = gpu_metrics_checker.run_gpu_metrics_check({})

        self.assertIsInstance(value, expected_type)
        self.assertEqual(value.error_code, expected_error_code)
        result = json.loads(value.result)
        self.assertEqual(result['Value']["GPU metrics check"]["Message"], expected_message)

    def test_get_api_version_returns_str(self):
        expected = str

        value = gpu_metrics_checker.get_api_version()

        self.assertIsInstance(value, expected)

    def test_get_check_list_returns_list_metadata(self):
        expected = CheckMetadataPy

        value = gpu_metrics_checker.get_check_list()

        for metadata in value:
            self.assertIsInstance(metadata, expected)


class TestProcessDevice(unittest.TestCase):

    @patch("checkers_py.linux.gpu_metrics_checker.compare_metrics_for_known_device")
    @patch("checkers_py.linux.gpu_metrics_checker.show_metrics_for_unknown_device")
    def test_process_device_known_device(self, mocked_unknown_device, mocked_known_device):
        device_mock = MagicMock()
        device_mock.id = "0x4905"

        gpu_metrics_checker.process_device({}, device_mock)

        mocked_known_device.assert_called_once()
        mocked_unknown_device.assert_not_called()

    @patch("checkers_py.linux.gpu_metrics_checker.compare_metrics_for_known_device")
    @patch("checkers_py.linux.gpu_metrics_checker.show_metrics_for_unknown_device")
    def test_process_device_unknown_device(self, mocked_unknown_device, mocked_known_device):
        device_mock = MagicMock()
        device_mock.id = "0"

        gpu_metrics_checker.process_device({}, device_mock)

        mocked_known_device.assert_not_called()
        mocked_unknown_device.assert_called_once()


class TestDevice(unittest.TestCase):

    def test_device_init_does_not_raise_error(self):
        gpu_metrics_checker.Device(
            name="test",
            id="test",
            max_freq="1000",
            min_freq="1000",
            cur_freq="1000",
            mem_bandwidth="1",
            pcie_bandwidth="1",
            gpu_type="test",
            enumeration="0"
        )


class TestParseDevices(unittest.TestCase):

    def test_parse_devices_positive(self):
        expected = [
            gpu_metrics_checker.Device(
                name="test_device_1",
                id="1",
                max_freq="1000",
                min_freq="1000",
                cur_freq="1000",
                mem_bandwidth="2",
                pcie_bandwidth="2",
                gpu_type="Discrete",
                enumeration="0"
            ),
            gpu_metrics_checker.Device(
                name="test_device_2",
                id="2",
                max_freq="500",
                min_freq="500",
                cur_freq="500",
                mem_bandwidth="1",
                pcie_bandwidth="1",
                gpu_type="Discrete",
                enumeration="1"
            )
        ]

        input = {
            "gpu_backend_check": {
                "Value": {
                    "GPU": {
                        "Value": {
                            "Intel® oneAPI Level Zero Driver": {
                                "Value": {
                                    "Driver is loaded.": {
                                        "RetVal": "PASS"
                                    },
                                    "Driver information": {
                                        "RetVal": "INFO",
                                        "Value": {
                                            "Installed driver number": {
                                                "Value": "1"
                                            },
                                            "Driver # 0": {
                                                "Value": {
                                                    "Devices": {
                                                        "Value": {
                                                            "Device number": {
                                                                "Value": "3"
                                                            },
                                                            "Device # 0": {
                                                                "Value": {
                                                                    "Device type": {
                                                                        "Value": "Graphics Processing Unit"
                                                                    },
                                                                    "Device name": {
                                                                        "Value": "test_device_1"
                                                                    },
                                                                    "Device ID": {
                                                                        "Value": "1"
                                                                    },
                                                                    "Device maximum frequency, MHz": {
                                                                        "Value": "1000"
                                                                    },
                                                                    "Device minimum frequency, MHz": {
                                                                        "Value": "1000"
                                                                    },
                                                                    "Device current frequency, MHz": {
                                                                        "Value": "1000"
                                                                    },
                                                                    "Memory bandwidth, GB/s": {
                                                                        "Value": "2"
                                                                    },
                                                                    "PCIe bandwidth, GB/s": {
                                                                        "Value": "2"
                                                                    }
                                                                }
                                                            },
                                                            "Device # 1": {
                                                                "Value": {
                                                                    "Device type": {
                                                                        "Value": "Graphics Processing Unit"
                                                                    },
                                                                    "Device name": {
                                                                        "Value": "test_device_2"
                                                                    },
                                                                    "Device ID": {
                                                                        "Value": "2"
                                                                    },
                                                                    "Device maximum frequency, MHz": {
                                                                        "Value": "500"
                                                                    },
                                                                    "Device minimum frequency, MHz": {
                                                                        "Value": "500"
                                                                    },
                                                                    "Device current frequency, MHz": {
                                                                        "Value": "500"
                                                                    },
                                                                    "Memory bandwidth, GB/s": {
                                                                        "Value": "1"
                                                                    },
                                                                    "PCIe bandwidth, GB/s": {
                                                                        "Value": "1"
                                                                    }
                                                                }
                                                            },
                                                            "Device # 2": {
                                                                "Value": {
                                                                    "Device type": {
                                                                        "Value": "CPU"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "intel_gpu_detector_check": {
                "Value": {
                    "GPU information": {
                        "Value": {
                            "Initialized devices": {
                                "RetVal": "INFO",
                                "Value": {
                                    "Intel GPU #1": {
                                        "Value": {
                                            "GPU type": {
                                                "Value": "Discrete"
                                            }
                                        }
                                    },
                                    "Intel GPU #2": {
                                        "Value": {
                                            "GPU type": {
                                                "Value": "Discrete"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        value = gpu_metrics_checker.parse_devices(input)

        for expected_device, value_device in zip(expected, value):
            self.assertEqual(expected_device.__dict__, value_device.__dict__)

    def test_parse_devices_lz_return_not_dict(self):
        expected = []

        input = {
            "gpu_backend_check": {
                "Value": {
                    "GPU": {
                        "Value": {
                            "Intel® oneAPI Level Zero Driver": {
                                "Value": {
                                    "Driver is loaded.": {
                                        "RetVal": "PASS"
                                    },
                                    "Driver information": {
                                        "RetVal": "INFO",
                                        "Value": []
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "intel_gpu_detector_check": {
                "Value": {
                    "GPU information": {
                        "Value": {
                            "Initialized devices": {
                                "RetVal": "INFO",
                                "Value": {
                                    "Intel GPU #1": {
                                        "Value": {
                                            "GPU type": {
                                                "Value": "Discrete"
                                            }
                                        }
                                    },
                                    "Intel GPU #2": {
                                        "Value": {
                                            "GPU type": {
                                                "Value": "Discrete"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        value = gpu_metrics_checker.parse_devices(input)

        self.assertEqual(expected, value)

    @patch("checkers_py.linux.gpu_metrics_checker.is_level_zero_initialized")
    def test_parse_devices_lz_not_initialized(self, mocked_is_level_zero_initialized):
        input = []
        device_message = "device message"
        mocked_is_level_zero_initialized.return_value = (False, device_message)

        with self.assertRaises(Exception) as raised:
            gpu_metrics_checker.parse_devices(input)

        self.assertEqual(str(raised.exception), device_message)


class TestShowMetricsForUnknownDevice(unittest.TestCase):

    def test_show_metrics_for_unknown_device_unknown_metrics(self):
        expected = {
            "#0 unknown_device": {
                "Value": {
                    "GPU Frequency, MHz (Max/Target)": {
                        "Value": "unknown/unknown",
                        "RetVal": "ERROR",
                        "Message": "The Level Zero driver cannot find out information about frequency.",
                        "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility." # noqa E501
                    },
                    "Memory bandwidth, GB/s (Max/Target)": {
                        "Value": "unknown/unknown",
                        "RetVal": "ERROR",
                        "Message": "The Level Zero driver cannot find out information about memory bandwidth.", # noqa E501
                        "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility." # noqa E501
                    },
                    "PCIe bandwidth, GB/s (Max/Target)": {
                        "Value": "unknown/unknown",
                        "RetVal": "ERROR",
                        "Message": "The Level Zero driver cannot find out information about PCIe bandwidth.",
                        "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility." # noqa E501
                    },
                },
                "RetVal": "WARNING",
                "Message": "For this GPU, good numbers are not known."
            }
        }

        input = gpu_metrics_checker.Device(
            name="unknown_device",
            id="unknown",
            max_freq="unknown",
            min_freq="unknown",
            cur_freq="unknown",
            mem_bandwidth="unknown",
            pcie_bandwidth="unknown",
            gpu_type="Discrete",
            enumeration="0"
        )

        value = {}
        gpu_metrics_checker.show_metrics_for_unknown_device(value, input)

        self.assertEqual(expected, value)

    def test_show_metrics_for_unknown_device_known_metrics(self):
        expected = {
            "#0 unknown_device": {
                "Value": {
                    "GPU Frequency, MHz (Max/Target)": {
                        "Value": "1000/unknown",
                        "RetVal": "INFO"
                    },
                    "Memory bandwidth, GB/s (Max/Target)": {
                        "Value": "1/unknown",
                        "RetVal": "INFO"
                    },
                    "PCIe bandwidth, GB/s (Max/Target)": {
                        "Value": "1/unknown",
                        "RetVal": "INFO"
                    },
                },
                "RetVal": "WARNING",
                "Message": "For this GPU, good numbers are not known."
            }
        }

        input = gpu_metrics_checker.Device(
            name="unknown_device",
            id="unknown",
            max_freq="1000",
            min_freq="1000",
            cur_freq="1000",
            mem_bandwidth="1",
            pcie_bandwidth="1",
            gpu_type="Discrete",
            enumeration="0"
        )

        value = {}
        gpu_metrics_checker.show_metrics_for_unknown_device(value, input)

        self.assertEqual(expected, value)


class TestCompareMetricsForKnownDevice(unittest.TestCase):

    def test_compare_metrics_for_known_device_unknown_metrics(self):
        expected = {
            "#0 known_device": {
                "Value": {
                    "GPU Frequency, MHz (Max/Target)": {
                        "Value": "unknown/1200",
                        "RetVal": "ERROR",
                        "Message": "The Level Zero driver cannot find out information about frequency.",  # noqa E501
                        "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility." # noqa E501
                    },
                    "Memory bandwidth, GB/s (Max/Target)": {
                        "Value": "unknown/30",
                        "RetVal": "ERROR",
                        "Message": "The Level Zero driver cannot find out information about memory bandwidth.", # noqa E501
                        "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility." # noqa E501
                    },
                    "PCIe bandwidth, GB/s (Max/Target)": {
                        "Value": "unknown/10",
                        "RetVal": "ERROR",
                        "Message": "The Level Zero driver cannot find out information about PCIe bandwidth.",  # noqa E501
                        "HowToFix": "This error is unexpected. Please report the issue to Diagnostics Utility for Intel® oneAPI Toolkits repository: https://github.com/intel/diagnostics-utility." # noqa E501
                    },
                },
                "RetVal": "PASS"
            }
        }

        input = gpu_metrics_checker.Device(
            name="known_device",
            id="0x3e98",
            max_freq="unknown",
            min_freq="unknown",
            cur_freq="unknown",
            mem_bandwidth="unknown",
            pcie_bandwidth="unknown",
            gpu_type="Discrete",
            enumeration="0"
        )

        value = {}
        gpu_metrics_checker.compare_metrics_for_known_device(value, input)

        self.assertEqual(expected, value)

    def test_compare_metrics_for_known_device_known_good_metrics(self):
        expected = {
            "#0 known_device": {
                "Value": {
                    "GPU Frequency, MHz (Max/Target)": {
                        "Value": "1200/1200",
                        "RetVal": "PASS"
                    },
                    "Memory bandwidth, GB/s (Max/Target)": {
                        "Value": "30/30",
                        "RetVal": "PASS"
                    },
                    "PCIe bandwidth, GB/s (Max/Target)": {
                        "Value": "10/10",
                        "RetVal": "PASS"
                    },
                },
                "RetVal": "PASS"
            }
        }

        input = gpu_metrics_checker.Device(
            name="known_device",
            id="0x3e98",
            max_freq="1200",
            min_freq="1200",
            cur_freq="1200",
            mem_bandwidth="30",
            pcie_bandwidth="10",
            gpu_type="Discrete",
            enumeration="0"
        )

        value = {}
        gpu_metrics_checker.compare_metrics_for_known_device(value, input)

        self.assertEqual(expected, value)

    def test_compare_metrics_for_known_device_known_bad_metrics(self):
        expected = {
            "#0 known_device": {
                "Value": {
                    "GPU Frequency, MHz (Max/Target)": {
                        "Value": "1000/1200",
                        "RetVal": "FAIL",
                        "Message": "The maximum GPU frequency is less than the target bandwidth.",
                        "HowToFix": "The maximum GPU frequency: 1000, should be equal or greater than "
                                    "the target value: 1200."
                    },
                    "Memory bandwidth, GB/s (Max/Target)": {
                        "Value": "3/30",
                        "RetVal": "FAIL",
                        "Message": "The maximum memory bandwidth is less than the target bandwidth.",
                        "HowToFix": "The maximum memory bandwidth: 3, should be equal or greater "
                                    "than the target value: 30."
                    },
                    "PCIe bandwidth, GB/s (Max/Target)": {
                        "Value": "1/10",
                        "RetVal": "FAIL",
                        "Message": "The maximum PCIe bandwidth is less than the target bandwidth.",
                        "HowToFix": "The maximum PCIe bandwidth: 1, should be equal or greater "
                                    "than the target value: 10."
                    },
                },
                "RetVal": "PASS"
            }
        }

        input = gpu_metrics_checker.Device(
            name="known_device",
            id="0x3e98",
            max_freq="1000",
            min_freq="1000",
            cur_freq="1000",
            mem_bandwidth="3",
            pcie_bandwidth="1",
            gpu_type="Discrete",
            enumeration="0"
        )

        value = {}
        gpu_metrics_checker.compare_metrics_for_known_device(value, input)

        self.assertEqual(expected, value)


class TestCheckIfTimeoutInGpuBackendCheck(unittest.TestCase):

    def test_timeout_in_gpu_backend_check_occured_positive(self):
        expected = True

        input = {
            "gpu_backend_check": {
                "Value": "GPU"
                }
            }

        value = gpu_metrics_checker.timeout_in_gpu_backend_check_occurred(input)

        self.assertEqual(expected, value)

    def test_timeout_in_gpu_backend_check_occured_negative(self):
        expected = False

        input = {
            "gpu_backend_check": {
                "Value": " "
                }
            }

        value = gpu_metrics_checker.timeout_in_gpu_backend_check_occurred(input)

        self.assertEqual(expected, value)


if __name__ == '__main__':
    unittest.TestCase.maxDiff = None
    unittest.main()
