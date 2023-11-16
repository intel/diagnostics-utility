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
import platform
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../"))

import unittest  # noqa: E402
from unittest.mock import MagicMock, patch, mock_open  # noqa: E402

from checkers_py.linux import base_system_checker  # noqa: E402
from modules.check import CheckSummary, CheckMetadataPy  # noqa: E402


@unittest.skipIf(platform.system(
        ) == "Windows", "run on linux only")
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
                "CheckResult": "some data",
                "CheckStatus": "INFO"
            }
        })
        mocked_get_cpu_info.side_effect = lambda node: node.update({
            "Check 2": {
                "CheckResult": "some data",
                "CheckStatus": "INFO"
            }
        })
        mocked_get_bios_information.side_effect = lambda node: node.update({
            "Check 3": {
                "CheckResult": "some data",
                "CheckStatus": "INFO"
            }
        })
        mocked_get_uname.side_effect = lambda node: node.update({
            "Check 4": {
                "CheckResult": "some data",
                "CheckStatus": "INFO"
            }
        })

        actual = base_system_checker.run_base_check({})

        self.assertIsInstance(actual, expected)

    def test_get_api_version_returns_str(self):
        expected = str

        actual = base_system_checker.get_api_version()

        self.assertIsInstance(actual, expected)

    def test_get_check_list_returns_list_metadata(self):
        expected = CheckMetadataPy

        check_list = base_system_checker.get_check_list()

        for metadata in check_list:
            self.assertIsInstance(metadata, expected)


@unittest.skipIf(platform.system(
        ) == "Windows", "run on linux only")
class TestGetHostname(unittest.TestCase):

    @patch("builtins.open", mock_open(read_data="hostname"))
    def test_get_hostname_positive(self):
        expected = {
            "Hostname": {
                "CheckResult": "hostname",
                "CheckStatus": "INFO",
                "Command": "cat /etc/hostname"
            }
        }

        actual = {}
        base_system_checker.get_hostname(actual)

        self.assertEqual(expected, actual)

    @patch("builtins.open", side_effect=Exception("test message"))
    def test_get_hostname_open_raise_error(self, mocked_open):
        expected = {
            "Hostname": {
                "CheckResult": "Undefined",
                "CheckStatus": "ERROR",
                "Command": "cat /etc/hostname",
                "Message": "test message",
                "HowToFix": "The system does not contain '/etc/hostname'. Ignore "
                            "this error.",
            }
        }

        actual = {}
        base_system_checker.get_hostname(actual)

        self.assertEqual(expected, actual)


@unittest.skipIf(platform.system(
        ) == "Windows", "run on linux only")
class TestGetBiosVendor(unittest.TestCase):

    @patch("builtins.open", mock_open(read_data="vendor"))
    def test__get_bios_vendor_positive(self):
        expected = {
            "BIOS vendor": {
                "CheckResult": "vendor",
                "CheckStatus": "INFO",
                "Command": "cat /sys/class/dmi/id/bios_vendor"
            }
        }

        actual = {}
        base_system_checker._get_bios_vendor(actual)

        self.assertEqual(expected, actual)

    @patch("builtins.open", side_effect=Exception("test message"))
    def test__get_bios_vendor_open_raise_error(self, mocked_open):
        expected = {
            "BIOS vendor": {
                "CheckResult": "Undefined",
                "CheckStatus": "ERROR",
                "Command": "cat /sys/class/dmi/id/bios_vendor",
                "Message": "test message",
                "HowToFix": "The system does not contain information "
                            "about BIOS. Ignore this error.",
            }
        }

        actual = {}
        base_system_checker._get_bios_vendor(actual)

        self.assertEqual(expected, actual)


@unittest.skipIf(platform.system(
        ) == "Windows", "run on linux only")
class TestGetBiosVersion(unittest.TestCase):

    @patch("builtins.open", mock_open(read_data="version"))
    def test__get_bios_version_positive(self):
        expected = {
            "BIOS version": {
                "CheckResult": "version",
                "CheckStatus": "INFO",
                "Command": "cat /sys/class/dmi/id/bios_version"
            }
        }

        actual = {}
        base_system_checker._get_bios_version(actual)

        self.assertEqual(expected, actual)

    @patch("builtins.open", side_effect=Exception("test message"))
    def test__get_bios_version_open_raise_error(self, mocked_open):
        expected = {
            "BIOS version": {
                "CheckResult": "Undefined",
                "CheckStatus": "ERROR",
                "Command": "cat /sys/class/dmi/id/bios_version",
                "Message": "test message",
                "HowToFix": "The system does not contain information "
                            "about BIOS. Ignore this error.",
            }
        }

        actual = {}
        base_system_checker._get_bios_version(actual)

        self.assertEqual(expected, actual)


@unittest.skipIf(platform.system(
        ) == "Windows", "run on linux only")
class TestGetBiosRelease(unittest.TestCase):

    @patch("builtins.open", mock_open(read_data="release"))
    @patch("os.path.exists", return_value=True)
    def test__get_bios_release_positive(self, mocked_exists):
        expected = {
            "BIOS release": {
                "CheckResult": "release",
                "CheckStatus": "INFO",
                "Command": "cat /sys/class/dmi/id/bios_release",
                "Verbosity": 1
            }
        }

        actual = {}
        base_system_checker._get_bios_release(actual)

        self.assertEqual(expected, actual)

    @patch("builtins.open", side_effect=Exception("test message"))
    @patch("os.path.exists", return_value=True)
    def test__get_bios_release_open_raise_error(self, mocked_exists, mocked_open):
        expected = {
            "BIOS release": {
                "CheckResult": "Undefined",
                "CheckStatus": "ERROR",
                "Command": "cat /sys/class/dmi/id/bios_release",
                "Message": "test message",
                "HowToFix": "The system does not contain information "
                            "about BIOS. Ignore this error.",
            }
        }

        actual = {}
        base_system_checker._get_bios_release(actual)

        self.assertEqual(expected, actual)

    @patch("os.path.exists", return_value=False)
    def test__get_bios_release_can_not_provide_info(self, mocked_exists):
        expected = {}

        actual = {}
        base_system_checker._get_bios_release(actual)

        self.assertEqual(expected, actual)


@unittest.skipIf(platform.system(
        ) == "Windows", "run on linux only")
class TestGetBiosDate(unittest.TestCase):

    @patch("builtins.open", mock_open(read_data="date"))
    @patch("os.path.exists", return_value=True)
    def test__get_bios_date_positive(self, mocked_exists):
        expected = {
            "BIOS date": {
                "CheckResult": "date",
                "CheckStatus": "INFO",
                "Command": "cat /sys/class/dmi/id/bios_date",
                "Verbosity": 2
            }
        }

        actual = {}
        base_system_checker._get_bios_date(actual)

        self.assertEqual(expected, actual)

    @patch("builtins.open", side_effect=Exception("test message"))
    @patch("os.path.exists", return_value=True)
    def test__get_bios_date_open_raise_error(self, mocked_exists, mocked_open):
        expected = {
            "BIOS date": {
                "CheckResult": "Undefined",
                "CheckStatus": "ERROR",
                "Command": "cat /sys/class/dmi/id/bios_date",
                "Message": "test message",
                "HowToFix": "The system does not contain information "
                            "about BIOS. Ignore this error.",
            }
        }

        actual = {}
        base_system_checker._get_bios_date(actual)

        self.assertEqual(expected, actual)

    @patch("os.path.exists", return_value=False)
    def test__get_bios_date_can_not_provide_info(self, mocked_exists):
        expected = {}

        actual = {}
        base_system_checker._get_bios_date(actual)

        self.assertEqual(expected, actual)


@unittest.skipIf(platform.system(
        ) == "Windows", "run on linux only")
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
                "CheckStatus": "INFO",
                "CheckResult": {
                    "Vendor": {
                        "CheckResult": "some data",
                        "CheckStatus": "INFO"
                    },
                    "Version": {
                        "CheckResult": "some data",
                        "CheckStatus": "INFO"
                    },
                    "Release": {
                        "CheckResult": "some data",
                        "CheckStatus": "INFO"
                    },
                    "Date": {
                        "CheckResult": "some data",
                        "CheckStatus": "INFO"
                    }
                }
            }
        }

        mocked__get_bios_date.side_effect = lambda node: node.update({
            "Date": {
                "CheckResult": "some data",
                "CheckStatus": "INFO"
            }
        })
        mocked__get_bios_release.side_effect = lambda node: node.update({
            "Release": {
                "CheckResult": "some data",
                "CheckStatus": "INFO"
            }
        })
        mocked__get_bios_version.side_effect = lambda node: node.update({
            "Version": {
                "CheckResult": "some data",
                "CheckStatus": "INFO"
            }
        })
        mocked__get_bios_vendor.side_effect = lambda node: node.update({
            "Vendor": {
                "CheckResult": "some data",
                "CheckStatus": "INFO"
            }
        })

        actual = {}
        base_system_checker.get_bios_information(actual)

        self.assertEqual(expected, actual)


@unittest.skipIf(platform.system(
        ) == "Windows", "run on linux only")
class TestGetUname(unittest.TestCase):

    @patch("platform.uname")
    def test_get_uname_positive(self, mocked_uname):
        expected = {
            "Operating system information": {
                "CheckResult": {
                    "System": {"CheckResult": "Linux", "CheckStatus": "INFO"},
                    "Node": {"CheckResult": "test", "CheckStatus": "INFO"},
                    "Release": {"CheckResult": "5.13.0-27-generic", "CheckStatus": "INFO"},
                    "Version": {
                        "CheckResult": "#29~20.04.1-Ubuntu SMP Fri Jan 14 00:32:30 UTC 2022",  # noqa: E501
                        "CheckStatus": "INFO"},
                    "Machine": {"CheckResult": "x86_64", "CheckStatus": "INFO"},
                    "Processor": {"CheckResult": "x86_64", "CheckStatus": "INFO"}
                },
                "CheckStatus": "INFO",
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

        actual = {}
        base_system_checker.get_uname(actual)

        self.assertEqual(expected, actual)


@unittest.skipIf(platform.system(
        ) == "Windows", "run on linux only")
class TestGetCpuFrequency(unittest.TestCase):

    @patch("builtins.open", mock_open(read_data="model name      : Intel(R) Core(TM) i7-8700K CPU @ 3.70GHz\n"
                                                "cpu MHz         : 3700.000\n"
                                                "model name      : Intel(R) Core(TM) i7-8700K CPU @ 3.70GHz\n"
                                                "cpu MHz         : 3700.000\n"))
    def test_get_cpu_frequency_positive(self):
        expected = {
            "CPU frequency": {
                "CheckResult": {
                    "Core 0": {
                        "CheckStatus": "INFO",
                        "CheckResult": "3700.000 MHz",
                        "Verbosity": 1
                    },
                    "Core 1": {
                        "CheckStatus": "INFO",
                        "CheckResult": "3700.000 MHz",
                        "Verbosity": 1
                    }
                },
                "CheckStatus": "INFO",
                "Verbosity": 1,
                "Command": "cat /proc/cpuinfo"
            }
        }

        actual = {}
        base_system_checker.get_cpu_frequency(actual)

        self.assertEqual(expected, actual)

    @patch("builtins.open", side_effect=Exception("test message"))
    def test_get_cpu_frequency_open_raise_value_error(self, mocked_open):
        expected = {
            "CPU frequency": {
                "CheckResult": "Undefined",
                "CheckStatus": "ERROR",
                "Verbosity": 1,
                "Command": "cat /proc/cpuinfo",
                "Message": "test message",
                "HowToFix": "The system does not contain information "
                            "about CPU frequency. Ignore this error.",
            }
        }

        actual = {}
        base_system_checker.get_cpu_frequency(actual)

        self.assertEqual(expected, actual)


@unittest.skipIf(platform.system(
        ) == "Windows", "run on linux only")
class TestGetCpuInfo(unittest.TestCase):

    @patch("subprocess.Popen")
    @patch("checkers_py.linux.base_system_checker.get_cpu_frequency")
    def test_get_cpu_info_positive(self, mocked_get_cpu_frequency, mocked_open):
        expected = {
            "CPU information": {
                "CheckResult": {
                    "Model name": {
                        "CheckResult": "Intel(R) Core(TM) i7-8700K CPU @ 3.70GHz",
                        "CheckStatus": "INFO"
                    },
                    "Architecture": {
                        "CheckResult": "x86_64",
                        "CheckStatus": "INFO"
                    },
                    "Vendor": {
                        "CheckResult": "GenuineIntel",
                        "CheckStatus": "INFO",
                        "Verbosity": 1
                    },
                    "CPU count": {
                        "CheckResult": "12",
                        "CheckStatus": "INFO"
                    },
                    "Thread(s) per core": {
                        "CheckResult": "2",
                        "CheckStatus": "INFO",
                        "Verbosity": 2
                    },
                    "Core(s) per socket": {
                        "CheckResult": "6",
                        "CheckStatus": "INFO",
                        "Verbosity": 2
                    },
                    "Socket(s)": {
                        "CheckResult": "1",
                        "CheckStatus": "INFO",
                        "Verbosity": 2
                    },
                    "CPU frequency": {
                        "CheckResult": {
                            "Core 0": {
                                "CheckStatus": "INFO",
                                "CheckResult": "3700.000 MHz",
                                "Verbosity": 1
                            },
                            "Core 1": {
                                "CheckStatus": "INFO",
                                "CheckResult": "3700.000 MHz",
                                "Verbosity": 1
                            }
                        },
                        "CheckStatus": "INFO",
                        "Verbosity": 1,
                        "Command": "cat /proc/cpuinfo"
                    }
                },
                "CheckStatus": "INFO",
                "Command": "lscpu"
            }
        }

        mocked_get_cpu_frequency.side_effect = lambda node: node.update({
            "CPU frequency": {
                "CheckResult": {
                    "Core 0": {
                        "CheckStatus": "INFO",
                        "CheckResult": "3700.000 MHz",
                        "Verbosity": 1
                    },
                    "Core 1": {
                        "CheckStatus": "INFO",
                        "CheckResult": "3700.000 MHz",
                        "Verbosity": 1
                    }
                },
                "CheckStatus": "INFO",
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

        actual = {}
        base_system_checker.get_cpu_info(actual)

        self.assertEqual(expected, actual)

    @patch("subprocess.Popen")
    def test_get_cpu_info_process_return_code_is_not_zero(self, mocked_open):
        expected = {
            "CPU information": {
                "CheckResult": "Undefined",
                "CheckStatus": "ERROR",
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

        actual = {}
        base_system_checker.get_cpu_info(actual)

        self.assertEqual(expected, actual)

    @patch("subprocess.Popen", side_effect=Exception("test message"))
    def test_get_cpu_info_subprocess_raise_exception(self, mocked_open):
        expected = {
            "CPU information": {
                "CheckResult": "Undefined",
                "CheckStatus": "ERROR",
                "Command": "lscpu",
                "Message": "test message",
                "HowToFix": "The system does not contain information "
                            "about CPU. Ignore this error.",
            }
        }

        actual = {}
        base_system_checker.get_cpu_info(actual)

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
