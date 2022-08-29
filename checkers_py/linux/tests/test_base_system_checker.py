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
from collections import namedtuple
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../"))

import unittest  # noqa: E402
from unittest.mock import MagicMock, patch, mock_open  # noqa: E402

from checkers_py.linux import base_system_checker  # noqa: E402
from modules.check import CheckSummary, CheckMetadataPy  # noqa: E402


class TestBaseSystemCheckerApiTest(unittest.TestCase):

    @patch("checkers_py.linux.base_system_checker.get_hostname")
    @patch("checkers_py.linux.base_system_checker.get_cpu_info")
    @patch("checkers_py.linux.base_system_checker.get_bios_information")
    @patch("checkers_py.linux.base_system_checker.get_uname")
    def test_run_positive(
            self,
            mocked_get_uname,
            mocked_get_bios_information,
            mocked_get_cpu_info,
            mocked_get_hostname):
        expected = CheckSummary

        mocked_get_hostname.side_effect = lambda node: node.update({
            "Check 1": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })
        mocked_get_cpu_info.side_effect = lambda node: node.update({
            "Check 2": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })
        mocked_get_bios_information.side_effect = lambda node: node.update({
            "Check 3": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })
        mocked_get_uname.side_effect = lambda node: node.update({
            "Check 4": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })

        value = base_system_checker.run_base_check({})

        self.assertIsInstance(value, expected)

    def test_get_api_version_returns_str(self):
        expected = str

        value = base_system_checker.get_api_version()

        self.assertIsInstance(value, expected)

    def test_get_check_list_returns_list_metadata(self):
        expected = CheckMetadataPy

        value = base_system_checker.get_check_list()

        for metadata in value:
            self.assertIsInstance(metadata, expected)


class TestGetHostname(unittest.TestCase):

    @patch("builtins.open", mock_open(read_data="hostname"))
    def test_get_hostname_positive(self):
        expected = {
            "Hostname": {
                "Value": "hostname",
                "RetVal": "INFO",
                "Command": "cat /etc/hostname"
            }
        }

        value = {}
        base_system_checker.get_hostname(value)

        self.assertEqual(expected, value)

    @patch("builtins.open", side_effect=Exception("test message"))
    def test_get_hostname_open_raise_error(self, mocked_open):
        expected = {
            "Hostname": {
                "Value": "Undefined",
                "RetVal": "ERROR",
                "Command": "cat /etc/hostname",
                "Message": "test message",
                "HowToFix": "The system does not contain '/etc/hostname'. Ignore "
                            "this error.",
            }
        }

        value = {}
        base_system_checker.get_hostname(value)

        self.assertEqual(expected, value)


class TestGetBiosVendor(unittest.TestCase):

    @patch("builtins.open", mock_open(read_data="vendor"))
    def test__get_bios_vendor_positive(self):
        expected = {
            "BIOS vendor": {
                "Value": "vendor",
                "RetVal": "INFO",
                "Command": "cat /sys/class/dmi/id/bios_vendor"
            }
        }

        value = {}
        base_system_checker._get_bios_vendor(value)

        self.assertEqual(expected, value)

    @patch("builtins.open", side_effect=Exception("test message"))
    def test__get_bios_vendor_open_raise_error(self, mocked_open):
        expected = {
            "BIOS vendor": {
                "Value": "Undefined",
                "RetVal": "ERROR",
                "Command": "cat /sys/class/dmi/id/bios_vendor",
                "Message": "test message",
                "HowToFix": "The system does not contain information "
                            "about BIOS. Ignore this error.",
            }
        }

        value = {}
        base_system_checker._get_bios_vendor(value)

        self.assertEqual(expected, value)


class TestGetBiosVersion(unittest.TestCase):

    @patch("builtins.open", mock_open(read_data="version"))
    def test__get_bios_version_positive(self):
        expected = {
            "BIOS version": {
                "Value": "version",
                "RetVal": "INFO",
                "Command": "cat /sys/class/dmi/id/bios_version"
            }
        }

        value = {}
        base_system_checker._get_bios_version(value)

        self.assertEqual(expected, value)

    @patch("builtins.open", side_effect=Exception("test message"))
    def test__get_bios_version_open_raise_error(self, mocked_open):
        expected = {
            "BIOS version": {
                "Value": "Undefined",
                "RetVal": "ERROR",
                "Command": "cat /sys/class/dmi/id/bios_version",
                "Message": "test message",
                "HowToFix": "The system does not contain information "
                            "about BIOS. Ignore this error.",
            }
        }

        value = {}
        base_system_checker._get_bios_version(value)

        self.assertEqual(expected, value)


class TestGetBiosRelease(unittest.TestCase):

    @patch("builtins.open", mock_open(read_data="release"))
    @patch("os.path.exists", return_value=True)
    def test__get_bios_release_positive(self, mocked_exists):
        expected = {
            "BIOS release": {
                "Value": "release",
                "RetVal": "INFO",
                "Command": "cat /sys/class/dmi/id/bios_release",
                "Verbosity": 1
            }
        }

        value = {}
        base_system_checker._get_bios_release(value)

        self.assertEqual(expected, value)

    @patch("builtins.open", side_effect=Exception("test message"))
    @patch("os.path.exists", return_value=True)
    def test__get_bios_release_open_raise_error(self, mocked_exists, mocked_open):
        expected = {
            "BIOS release": {
                "Value": "Undefined",
                "RetVal": "ERROR",
                "Command": "cat /sys/class/dmi/id/bios_release",
                "Message": "test message",
                "HowToFix": "The system does not contain information "
                            "about BIOS. Ignore this error.",
            }
        }

        value = {}
        base_system_checker._get_bios_release(value)

        self.assertEqual(expected, value)

    @patch("os.path.exists", return_value=False)
    def test__get_bios_release_can_not_provide_info(self, mocked_exists):
        expected = {}

        value = {}
        base_system_checker._get_bios_release(value)

        self.assertEqual(expected, value)


class TestGetBiosDate(unittest.TestCase):

    @patch("builtins.open", mock_open(read_data="date"))
    @patch("os.path.exists", return_value=True)
    def test__get_bios_date_positive(self, mocked_exists):
        expected = {
            "BIOS date": {
                "Value": "date",
                "RetVal": "INFO",
                "Command": "cat /sys/class/dmi/id/bios_date",
                "Verbosity": 2
            }
        }

        value = {}
        base_system_checker._get_bios_date(value)

        self.assertEqual(expected, value)

    @patch("builtins.open", side_effect=Exception("test message"))
    @patch("os.path.exists", return_value=True)
    def test__get_bios_date_open_raise_error(self, mocked_exists, mocked_open):
        expected = {
            "BIOS date": {
                "Value": "Undefined",
                "RetVal": "ERROR",
                "Command": "cat /sys/class/dmi/id/bios_date",
                "Message": "test message",
                "HowToFix": "The system does not contain information "
                            "about BIOS. Ignore this error.",
            }
        }

        value = {}
        base_system_checker._get_bios_date(value)

        self.assertEqual(expected, value)

    @patch("os.path.exists", return_value=False)
    def test__get_bios_date_can_not_provide_info(self, mocked_exists):
        expected = {}

        value = {}
        base_system_checker._get_bios_date(value)

        self.assertEqual(expected, value)


class TestGetBiosInformation(unittest.TestCase):

    @patch("checkers_py.linux.base_system_checker._get_bios_vendor")
    @patch("checkers_py.linux.base_system_checker._get_bios_version")
    @patch("checkers_py.linux.base_system_checker._get_bios_release")
    @patch("checkers_py.linux.base_system_checker._get_bios_date")
    def test_get_bios_information_positive(
            self,
            mocked__get_bios_date,
            mocked__get_bios_release,
            mocked__get_bios_version,
            mocked__get_bios_vendor):
        expected = {
            "BIOS information": {
                "RetVal": "INFO",
                "Value": {
                    "Vendor": {
                        "Value": "Value",
                        "RetVal": "INFO"
                    },
                    "Version": {
                        "Value": "Value",
                        "RetVal": "INFO"
                    },
                    "Release": {
                        "Value": "Value",
                        "RetVal": "INFO"
                    },
                    "Date": {
                        "Value": "Value",
                        "RetVal": "INFO"
                    }
                }
            }
        }

        mocked__get_bios_date.side_effect = lambda node: node.update({
            "Date": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })
        mocked__get_bios_release.side_effect = lambda node: node.update({
            "Release": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })
        mocked__get_bios_version.side_effect = lambda node: node.update({
            "Version": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })
        mocked__get_bios_vendor.side_effect = lambda node: node.update({
            "Vendor": {
                "Value": "Value",
                "RetVal": "INFO"
            }
        })

        value = {}
        base_system_checker.get_bios_information(value)

        self.assertEqual(expected, value)


class TestGetUname(unittest.TestCase):

    @patch("platform.uname")
    def test_get_uname_positive(self, mocked_uname):
        expected = {
            "Operating system information": {
                "Value": {
                    "System": {"Value": "Linux", "RetVal": "INFO"},
                    "Node": {"Value": "test", "RetVal": "INFO"},
                    "Release": {"Value": "5.13.0-27-generic", "RetVal": "INFO"},
                    "Version": {
                        "Value": "#29~20.04.1-Ubuntu SMP Fri Jan 14 00:32:30 UTC 2022", "RetVal": "INFO"},
                    "Machine": {"Value": "x86_64", "RetVal": "INFO"},
                    "Processor": {"Value": "x86_64", "RetVal": "INFO"}
                },
                "RetVal": "INFO",
                "Command": "uname -a"
            }
        }

        Mocked_Uname = namedtuple(
            "Mocked_Uname", ["system", "node", "release", "version", "machine", "processor"])
        mocked_uname.return_value = Mocked_Uname(
            "Linux",
            "test",
            "5.13.0-27-generic",
            "#29~20.04.1-Ubuntu SMP Fri Jan 14 00:32:30 UTC 2022",
            "x86_64",
            "x86_64"
        )

        value = {}
        base_system_checker.get_uname(value)

        self.assertEqual(expected, value)


class TestGetCpuFrequency(unittest.TestCase):

    @patch("builtins.open", mock_open(read_data="model name      : Intel(R) Core(TM) i7-8700K CPU @ 3.70GHz\n"
                                                "cpu MHz         : 3700.000\n"
                                                "model name      : Intel(R) Core(TM) i7-8700K CPU @ 3.70GHz\n"
                                                "cpu MHz         : 3700.000\n"))
    def test_get_cpu_frequency_positive(self):
        expected = {
            "CPU frequency": {
                "Value": {
                    "Core 0": {
                        "RetVal": "INFO",
                        "Value": "3700.000 MHz",
                        "Verbosity": 1
                    },
                    "Core 1": {
                        "RetVal": "INFO",
                        "Value": "3700.000 MHz",
                        "Verbosity": 1
                    }
                },
                "RetVal": "INFO",
                "Verbosity": 1,
                "Command": "cat /proc/cpuinfo"
            }
        }

        value = {}
        base_system_checker.get_cpu_frequency(value)

        self.assertEqual(expected, value)

    @patch("builtins.open", side_effect=Exception("test message"))
    def test_get_cpu_frequency_open_raise_value_error(self, mocked_open):
        expected = {
            "CPU frequency": {
                "Value": "Undefined",
                "RetVal": "ERROR",
                "Verbosity": 1,
                "Command": "cat /proc/cpuinfo",
                "Message": "test message",
                "HowToFix": "The system does not contain information "
                            "about CPU frequency. Ignore this error.",
            }
        }

        value = {}
        base_system_checker.get_cpu_frequency(value)

        self.assertEqual(expected, value)


class TestGetCpuInfo(unittest.TestCase):

    @patch("subprocess.Popen")
    @patch("checkers_py.linux.base_system_checker.get_cpu_frequency")
    def test_get_cpu_info_positive(self, mocked_get_cpu_frequency, mocked_open):
        expected = {
            "CPU information": {
                "Value": {
                    "Model name": {
                        "Value": "Intel(R) Core(TM) i7-8700K CPU @ 3.70GHz",
                        "RetVal": "INFO"
                    },
                    "Architecture": {
                        "Value": "x86_64",
                        "RetVal": "INFO"
                    },
                    "Vendor": {
                        "Value": "GenuineIntel",
                        "RetVal": "INFO",
                        "Verbosity": 1
                    },
                    "CPU count": {
                        "Value": "12",
                        "RetVal": "INFO"
                    },
                    "Thread(s) per core": {
                        "Value": "2",
                        "RetVal": "INFO",
                        "Verbosity": 2
                    },
                    "Core(s) per socket": {
                        "Value": "6",
                        "RetVal": "INFO",
                        "Verbosity": 2
                    },
                    "Socket(s)": {
                        "Value": "1",
                        "RetVal": "INFO",
                        "Verbosity": 2
                    },
                    "CPU frequency": {
                        "Value": {
                            "Core 0": {
                                "RetVal": "INFO",
                                "Value": "3700.000 MHz",
                                "Verbosity": 1
                            },
                            "Core 1": {
                                "RetVal": "INFO",
                                "Value": "3700.000 MHz",
                                "Verbosity": 1
                            }
                        },
                        "RetVal": "INFO",
                        "Verbosity": 1,
                        "Command": "cat /proc/cpuinfo"
                    }
                },
                "RetVal": "INFO",
                "Command": "lscpu"
            }
        }

        mocked_get_cpu_frequency.side_effect = lambda node: node.update({
            "CPU frequency": {
                "Value": {
                    "Core 0": {
                        "RetVal": "INFO",
                        "Value": "3700.000 MHz",
                        "Verbosity": 1
                    },
                    "Core 1": {
                        "RetVal": "INFO",
                        "Value": "3700.000 MHz",
                        "Verbosity": 1
                    }
                },
                "RetVal": "INFO",
                "Verbosity": 1,
                "Command": "cat /proc/cpuinfo"
            }
        })

        process = MagicMock()
        process.communicate.return_value = (
            "Architecture:                    x86_64\n"
            "CPU op-mode(s):                  32-bit, 64-bit\n"
            "Byte Order:                      Little Endian\n"
            "Address sizes:                   39 bits physical, 48 bits virtual\n"
            "CPU(s):                          12\n"
            "On-line CPU(s) list:             0-11\n"
            "Thread(s) per core:              2\n"
            "Core(s) per socket:              6\n"
            "Socket(s):                       1\n"
            "NUMA node(s):                    1\n"
            "Vendor ID:                       GenuineIntel\n"
            "CPU family:                      6\n"
            "Model:                           158\n"
            "Model name:                      Intel(R) Core(TM) i7-8700K CPU @ 3.70GHz\n"
            "Stepping:                        10\n"
            "CPU MHz:                         3700.000\n"
            "CPU max MHz:                     4700.0000\n"
            "CPU min MHz:                     800.0000\n"
            "BogoMIPS:                        7399.70\n"
            "Virtualization:                  VT-x\n"
            "L1d cache:                       192 KiB\n"
            "L1i cache:                       192 KiB\n"
            "L2 cache:                        1.5 MiB\n"
            "L3 cache:                        12 MiB\n"
            "NUMA node0 CPU(s):               0-11\n",
            None
        )
        process.returncode = 0

        mocked_open.return_value = process

        value = {}
        base_system_checker.get_cpu_info(value)

        self.assertEqual(expected, value)

    @patch("subprocess.Popen")
    def test_get_cpu_info_process_return_code_is_not_zero(self, mocked_open):
        expected = {
            "CPU information": {
                "Value": "Undefined",
                "RetVal": "ERROR",
                "Command": "lscpu",
                "Message": "Cannot get information about CPU",
                "HowToFix": "The system does not contain information "
                            "about CPU. Ignore this error.",
            }
        }

        process = MagicMock()
        process.communicate.return_value = (None, None)
        process.returncode = 1

        mocked_open.return_value = process

        value = {}
        base_system_checker.get_cpu_info(value)

        self.assertEqual(expected, value)

    @patch("subprocess.Popen", side_effect=Exception("test message"))
    def test_get_cpu_info_subprocess_raise_exception(self, mocked_open):
        expected = {
            "CPU information": {
                "Value": "Undefined",
                "RetVal": "ERROR",
                "Command": "lscpu",
                "Message": "test message",
                "HowToFix": "The system does not contain information "
                            "about CPU. Ignore this error.",
            }
        }

        value = {}
        base_system_checker.get_cpu_info(value)

        self.assertEqual(expected, value)


if __name__ == "__main__":
    unittest.main()
