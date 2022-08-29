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
from unittest.mock import MagicMock, patch  # noqa: E402

from checkers_py.linux import gpu_metrics_checker  # noqa: E402
from modules.check import CheckSummary, CheckMetadataPy  # noqa: E402


class TestGpuMetricsCheckerApiTest(unittest.TestCase):

    @patch("checkers_py.linux.gpu_metrics_checker.parse_devices", return_value=["Device 1", "Device 2"])
    @patch("checkers_py.linux.gpu_metrics_checker.process_device")
    def test_run_positive(self, mocked_process_device, mocked_parse_devices):
        expected = CheckSummary

        mocked_process_device.side_effect = lambda node, device: node.update({
            device: {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })

        value = gpu_metrics_checker.run_gpu_metrics_check({})

        self.assertIsInstance(value, expected)

    @patch("checkers_py.linux.gpu_metrics_checker.parse_devices", return_value=[])
    def test_run_exception_positive(self, mocked_parse_devices):
        expected = CheckSummary

        value = gpu_metrics_checker.run_gpu_metrics_check({})

        self.assertIsInstance(value, expected)

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
            pcie_bandwidth="1"
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
                pcie_bandwidth="2"
            ),
            gpu_metrics_checker.Device(
                name="test_device_2",
                id="2",
                max_freq="500",
                min_freq="500",
                cur_freq="500",
                mem_bandwidth="1",
                pcie_bandwidth="1"
            )
        ]

        input = {
            "gpu_backend_check": {
                "Value": {
                    "GPU": {
                        "Value": {
                            "Intel® oneAPI Level Zero Driver": {
                                "Value": {
                                    "Driver information": {
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
                                    "Driver information": {
                                        "Value": []
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


class TestShowMetricsForUnknownDevice(unittest.TestCase):

    def test_show_metrics_for_unknown_device_unknown_metrics(self):
        expected = {
            "unknown_device": {
                "Value": {
                    "GPU Frequency, MHz (Max/Target)": {
                        "Value": "unknown/unknown",
                        "RetVal": "ERROR",
                        "Message": "The Level Zero driver cannot find out information about frequency."
                    },
                    "Memory bandwidth, GB/s (Max/Target)": {
                        "Value": "unknown/unknown",
                        "RetVal": "ERROR",
                        "Message": "The Level Zero driver cannot find out information about memory bandwidth."
                    },
                    "PCIe bandwidth, GB/s (Max/Target)": {
                        "Value": "unknown/unknown",
                        "RetVal": "ERROR",
                        "Message": "The Level Zero driver cannot find out information about PCIe bandwidth."
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
            pcie_bandwidth="unknown"
        )

        value = {}
        gpu_metrics_checker.show_metrics_for_unknown_device(value, input)

        self.assertEqual(expected, value)

    def test_show_metrics_for_unknown_device_known_metrics(self):
        expected = {
            "unknown_device": {
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
            pcie_bandwidth="1"
        )

        value = {}
        gpu_metrics_checker.show_metrics_for_unknown_device(value, input)

        self.assertEqual(expected, value)


class TestCompareMetricsForKnownDevice(unittest.TestCase):

    def test_compare_metrics_for_known_device_unknown_metrics(self):
        expected = {
            "known_device": {
                "Value": {
                    "GPU Frequency, MHz (Max/Target)": {
                        "Value": "unknown/1200",
                        "RetVal": "ERROR",
                        "Message": "The Level Zero driver cannot find out information about frequency."
                    },
                    "Memory bandwidth, GB/s (Max/Target)": {
                        "Value": "unknown/30",
                        "RetVal": "ERROR",
                        "Message": "The Level Zero driver cannot find out information about memory bandwidth."
                    },
                    "PCIe bandwidth, GB/s (Max/Target)": {
                        "Value": "unknown/10",
                        "RetVal": "ERROR",
                        "Message": "The Level Zero driver cannot find out information about PCIe bandwidth."
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
            pcie_bandwidth="unknown"
        )

        value = {}
        gpu_metrics_checker.compare_metrics_for_known_device(value, input)

        self.assertEqual(expected, value)

    def test_compare_metrics_for_known_device_known_good_metrics(self):
        expected = {
            "known_device": {
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
            pcie_bandwidth="10"
        )

        value = {}
        gpu_metrics_checker.compare_metrics_for_known_device(value, input)

        self.assertEqual(expected, value)

    def test_compare_metrics_for_known_device_known_bad_metrics(self):
        expected = {
            "known_device": {
                "Value": {
                    "GPU Frequency, MHz (Max/Target)": {
                        "Value": "1000/1200",
                        "RetVal": "FAIL",
                        "Message": "The maximum GPU frequency is less than the target bandwidth."
                    },
                    "Memory bandwidth, GB/s (Max/Target)": {
                        "Value": "3/30",
                        "RetVal": "FAIL",
                        "Message": "The maximum memory bandwidth is less than the target bandwidth."
                    },
                    "PCIe bandwidth, GB/s (Max/Target)": {
                        "Value": "1/10",
                        "RetVal": "FAIL",
                        "Message": "The maximum PCIe bandwidth is less than the target bandwidth."
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
            pcie_bandwidth="1"
        )

        value = {}
        gpu_metrics_checker.compare_metrics_for_known_device(value, input)

        self.assertEqual(expected, value)


if __name__ == '__main__':
    unittest.TestCase.maxDiff = None
    unittest.main()
