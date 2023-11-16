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
import platform
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../"))

import unittest  # noqa: E402
from unittest.mock import patch  # noqa: E402

try:
    from checkers_py.windows import base_system_checker  # noqa: E402
except ImportError:
    pass
from modules.check import CheckSummary, CheckMetadataPy  # noqa: E402


@unittest.skipIf(platform.system(
) == "Linux", "run on windows only")
class TestBaseSystemCheckerApiTest(unittest.TestCase):

    @patch("checkers_py.windows.base_system_checker.get_hostname")
    @patch("checkers_py.windows.base_system_checker.get_cpu_info")
    @patch("checkers_py.windows.base_system_checker.get_bios_information")
    def test_run_positive(
            self,
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

        actual = base_system_checker.run_base_check({})

        self.assertIsInstance(actual, expected)

    def test_get_api_version_returns_str(self):
        expected = str

        actual = base_system_checker.get_api_version()

        self.assertIsInstance(actual, expected)

    def test_get_check_list_returns_list_metadata(self):
        expected = CheckMetadataPy

        actual = base_system_checker.get_check_list()

        for metadata in actual:
            self.assertIsInstance(metadata, expected)

    @patch("platform.node", return_value="data")
    def test_get_hostname(self, mocked_node):
        expected = {
            'Hostname': {'CheckResult': 'data', 'CheckStatus': 'INFO'}
        }

        actual = {}
        base_system_checker.get_hostname(actual)

        self.assertEqual(expected, actual)


@unittest.skipIf(platform.system(
) == "Linux", "run on Windows only")
class TestGetBiosVendor(unittest.TestCase):

    @patch("winreg.QueryValueEx", return_value=["vendor"])
    def test__get_bios_vendor_positive(self, mocked_QueryValueEx):
        expected = {
            "BIOS vendor": {
                "CheckResult": "vendor",
                "CheckStatus": "INFO"
            }
        }

        actual = {}
        base_system_checker._get_bios_vendor(actual)

        self.assertEqual(expected, actual)

    @patch("winreg.QueryValueEx", side_effect=Exception("test message"))
    def test__get_bios_vendor_error(self, mocked_QueryValueEx):
        expected = {
            "BIOS vendor": {
                "CheckResult": "Undefined",
                "CheckStatus": "ERROR",
                "Message": "test message",
                "HowToFix": "The Windows registry does not contain information about BIOS. "
                "Ignore this error."
            }
        }

        actual = {}
        base_system_checker._get_bios_vendor(actual)

        self.assertEqual(expected, actual)


@unittest.skipIf(platform.system(
) == "Linux", "run on Windows only")
class TestGetBiosVersion(unittest.TestCase):

    @patch("winreg.QueryValueEx", return_value=["version"])
    def test_get_bios_version_positive(self, mocked_QueryValueEx):
        expected = {
            "BIOS version": {
                "CheckResult": "version",
                "CheckStatus": "INFO"
            }
        }

        actual = {}
        base_system_checker._get_bios_version(actual)

        self.assertEqual(expected, actual)

    @patch("winreg.QueryValueEx", side_effect=Exception("test message"))
    def test_get_bios_version_open_raise_error(self, mocked_QueryValueEx):
        expected = {
            "BIOS version": {
                "CheckResult": "Undefined",
                "CheckStatus": "ERROR",
                "Message": "test message",
                "HowToFix": "The Windows registry does not contain information about BIOS. "
                "Ignore this error."
            }
        }

        actual = {}
        base_system_checker._get_bios_version(actual)

        self.assertEqual(expected, actual)


@unittest.skipIf(platform.system(
) == "Linux", "run on Windows only")
class TestGetBiosRelease(unittest.TestCase):

    @patch("winreg.QueryValueEx", return_value=["release"])
    def test_get_bios_release_positive(self, mocked_QueryValueEx):
        expected = {
            "BIOS release": {
                'CheckResult': {
                    'Major': {
                        'CheckResult': 'release',
                        'CheckStatus': 'INFO'
                    },
                    'Minor': {
                        'CheckResult': 'release',
                        'CheckStatus': 'INFO'
                    }
                },
                'CheckStatus': 'INFO'
            }
        }

        actual = {}
        base_system_checker._get_bios_release(actual)

        self.assertEqual(expected, actual)

    @patch("winreg.QueryValueEx", side_effect=Exception("test message"))
    def test_get_bios_release_error(self, mocked_QueryValueEx):
        expected = {
            "BIOS release": {
                "CheckResult": "Undefined",
                "CheckStatus": "ERROR",
                "Message": "test message",
                "HowToFix": "The Windows registry does not contain information about BIOS. "
                "Ignore this error."
            }
        }

        actual = {}
        base_system_checker._get_bios_release(actual)

        self.assertEqual(expected, actual)


@unittest.skipIf(platform.system(
) == "Linux", "run on Windows only")
class TestGetBiosDate(unittest.TestCase):

    @patch("winreg.QueryValueEx", return_value=["date"])
    def test_get_bios_date_positive(self, mocked_QueryValueEx):
        expected = {
            "BIOS date": {'CheckResult': 'date', 'CheckStatus': 'INFO', 'Verbosity': 2}
        }

        actual = {}
        base_system_checker._get_bios_date(actual)

        self.assertEqual(expected, actual)

    @patch("winreg.QueryValueEx", side_effect=Exception("test message"))
    def test_get_bios_date_error(self, mocked_QueryValueEx):
        expected = {
            "BIOS date": {
                "CheckResult": "Undefined",
                "CheckStatus": "ERROR",
                "Message": "test message",
                "HowToFix": "The Windows registry does not contain information about BIOS. "
                "Ignore this error."
            }
        }

        actual = {}
        base_system_checker._get_bios_date(actual)

        self.assertEqual(expected, actual)


@unittest.skipIf(platform.system(
) == "Linux", "run on Windows only")
class TestGetBiosInformation(unittest.TestCase):

    @patch("checkers_py.windows.base_system_checker._get_bios_vendor")
    @patch("checkers_py.windows.base_system_checker._get_bios_version")
    @patch("checkers_py.windows.base_system_checker._get_bios_release")
    @patch("checkers_py.windows.base_system_checker._get_bios_date")
    def test_get_bios_information_positive(self, mocked_get_bios_date, mocked_get_bios_release,
                                           mocked_get_bios_version, mocked_get_bios_vendor):
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

        mocked_get_bios_date.side_effect = lambda node: node.update({
            "Date": {
                "CheckResult": "some data",
                "CheckStatus": "INFO"
            }
        })
        mocked_get_bios_release.side_effect = lambda node: node.update({
            "Release": {
                "CheckResult": "some data",
                "CheckStatus": "INFO"
            }
        })
        mocked_get_bios_version.side_effect = lambda node: node.update({
            "Version": {
                "CheckResult": "some data",
                "CheckStatus": "INFO"
            }
        })
        mocked_get_bios_vendor.side_effect = lambda node: node.update({
            "Vendor": {
                "CheckResult": "some data",
                "CheckStatus": "INFO"
            }
        })

        actual = {}
        base_system_checker.get_bios_information(actual)

        self.assertEqual(expected, actual)


@unittest.skipIf(platform.system(
) == "Linux", "run on Windows only")
class TestGetOsEdition(unittest.TestCase):

    @patch("winreg.QueryValueEx", return_value=["edition"])
    def test_get_os_edition_positive(self, mocked_QueryValueEx):
        expected = {
            "Edition": {'CheckResult': 'edition', 'CheckStatus': 'INFO'}
        }

        actual = {}
        base_system_checker._get_os_edition(actual)

        self.assertEqual(expected, actual)

    @patch("winreg.QueryValueEx", side_effect=Exception("test message"))
    def test_get_os_edition_error(self, mocked_QueryValueEx):
        expected = {
            "Edition": {
                "CheckResult": "Undefined",
                "CheckStatus": "ERROR",
                "Message": "test message",
                "HowToFix": "The Windows registry does not contain information about windows "
                "edition. Ignore this error."  # noqa: E501
            }
        }

        actual = {}
        base_system_checker._get_os_edition(actual)

        self.assertEqual(expected, actual)


@unittest.skipIf(platform.system(
) == "Linux", "run on Windows only")
class TestGetOsMachine(unittest.TestCase):

    @patch("winreg.QueryValueEx", return_value=["machine"])
    def test_get_os_machine_positive(self, mocked_QueryValueEx):
        expected = {
            "Machine": {'CheckResult': 'machine', 'CheckStatus': 'INFO'}
        }

        actual = {}
        base_system_checker._get_os_machine(actual)

        self.assertEqual(expected, actual)

    @patch("winreg.QueryValueEx", side_effect=Exception("test message"))
    def test_get_os_machine_error(self, mocked_QueryValueEx):
        expected = {
            "Machine": {
                "CheckResult": "Undefined",
                "CheckStatus": "ERROR",
                "Message": "test message",
                "HowToFix": "The Windows registry does not contain information about processor "
                "architecture. Ignore this error."  # noqa: E501
            }
        }

        actual = {}
        base_system_checker._get_os_machine(actual)

        self.assertEqual(expected, actual)


@unittest.skipIf(platform.system(
) == "Linux", "run on Windows only")
class TestGetCpuFrequency(unittest.TestCase):

    @patch("winreg.EnumKey", side_effect=Exception("test message"))
    def test_get_cpu_frequency_positive(self, mocked_QueryValueEx):

        expected = {
            "CPU frequency":  {
                'CheckResult': {},
                'CheckStatus': 'INFO',
                'Verbosity': 1
            }
        }

        actual = {}
        base_system_checker.get_cpu_frequency('', actual)

        self.assertEqual(expected, actual)

    @patch("winreg.OpenKey", side_effect=Exception("test message"))
    def test_get_cpu_frequency_error(self, mocked_QueryValueEx):
        expected = {
            "CPU frequency": {
                    "CheckResult": "Undefined",
                    "CheckStatus": "ERROR",
                    "Message": "test message",
                    'Verbosity': 1,
                    "HowToFix": "The Windows registry does not contain information about CPU frequency. "
                    "Ignore this error."  # noqa: E501
                }
        }

        actual = {}
        base_system_checker.get_cpu_frequency('', actual)

        self.assertEqual(expected, actual)


@unittest.skipIf(platform.system(
) == "Linux", "run on Windows only")
class TestGetCpuInfo(unittest.TestCase):

    @patch("winreg.QueryValueEx", return_value=["data"])
    @patch("winreg.EnumKey", side_effect=Exception("test message"))
    @patch("checkers_py.windows.base_system_checker.get_cpu_frequency")
    def test_get_cpu_info_positive(self, mocked_get_cpu_frequency, mocked_EnumKey, mocked_QueryValueEx):

        expected = {
            "CPU information":  {
                'CheckResult': {
                    'Model identifier': {'CheckResult': 'data', "CheckStatus": "INFO"},
                    "Model name": {"CheckResult": 'data', "CheckStatus": "INFO"},
                    "Vendor": {"CheckResult": 'data', "CheckStatus": "INFO", "Verbosity": 1},
                    "CPU count": {"CheckResult": 0, "CheckStatus": "INFO"},
                },
                'CheckStatus': 'INFO'
            }
        }

        actual = {}
        base_system_checker.get_cpu_info(actual)

        self.assertEqual(expected, actual)

    @patch("winreg.QueryValueEx", side_effect=Exception("test message"))
    def test_get_cpu_info_error(self, mocked_QueryValueEx):
        expected = {
            "CPU information": {
                "CheckResult": "Undefined",
                "CheckStatus": "ERROR",
                "Message": "test message",
                "HowToFix": "The Windows registry does not contain information about CPU. "
                "Ignore this error."
            }
        }

        actual = {}
        base_system_checker.get_cpu_info(actual)

        self.assertEqual(expected, actual)


@unittest.skipIf(platform.system(
) == "Linux", "run on windows only")
class TestRunBaseCheck(unittest.TestCase):

    @patch("checkers_py.windows.base_system_checker.get_hostname")
    @patch("checkers_py.windows.base_system_checker.get_cpu_info")
    @patch("checkers_py.windows.base_system_checker.get_bios_information")
    @patch("checkers_py.windows.base_system_checker.get_os_information")
    def test_positive(self, mocked_get_os_information, mocked_get_bios_information,
                      mocked_get_cpu_info, mocked_get_hostname):

        mocked_get_os_information.side_effect = lambda node: node.update(
            {"Operating system information": os_information_json})
        mocked_get_bios_information.side_effect = lambda node: node.update(
            {"BIOS information": bios_information_json})
        mocked_get_cpu_info.side_effect = lambda node: node.update(
            {"CPU information": cpu_info_json})
        mocked_get_hostname.side_effect = lambda node: node.update(
            {"Hostname": hostname_json})

        expected_json = {
            "CheckResult": {},
            "CheckStatus": "INFO"
        }
        expected_json["CheckResult"].update({"Hostname": hostname_json})
        expected_json["CheckResult"].update({"CPU information": cpu_info_json})
        expected_json["CheckResult"].update({"BIOS information": bios_information_json})
        expected_json["CheckResult"].update({"Operating system information": os_information_json})

        expected = CheckSummary(
            result=json.dumps(expected_json, indent=4)
        )

        actual = base_system_checker.run_base_check({})
        self.assertEqual(expected.result, actual.result)


if __name__ == "__main__":
    unittest.main()


os_information_json = {
    "CheckResult": {
        "System": {
            "CheckResult": "Windows",
            "CheckStatus": "INFO"
        },
        "Release": {
            "CheckResult": "10",
            "CheckStatus": "INFO"
        },
        "Version": {
            "CheckResult": "10.0.0",
            "CheckStatus": "INFO"
        },
        "Edition": {
            "CheckResult": "Enterprise",
            "CheckStatus": "INFO"
        },
        "Machine": {
            "CheckResult": "AMD64",
            "CheckStatus": "INFO"
        },
    },
    "CheckStatus": "INFO"
}


bios_information_json = {
    "CheckResult": {
        "BIOS vendor": {
            "CheckResult": "HP",
            "CheckStatus": "INFO"
        },
        "BIOS version": {
            "CheckResult": "1",
            "CheckStatus": "INFO"
        },
        "BIOS release": {
            "CheckResult": {
                "Major": {
                    "CheckResult": "1",
                    "CheckStatus": "INFO"},
                "Minor": {
                    "CheckResult": "0",
                    "CheckStatus": "INFO"}
            },
            "CheckStatus": "INFO"
        },
        "BIOS date": {
            "CheckResult": "01.01.2001",
            "CheckStatus": "INFO"
        }
    },
    "CheckStatus": "INFO"
}


hostname_json = {
    "CheckResult": "$uper_Host1998",
    "CheckStatus": "INFO"
}

cpu_info_json = {
    "CheckResult": {
        "Model identifier": {
            "CheckResult": "Intel Family",
            "CheckStatus": "INFO"
        },
        "Model name": {
            "CheckResult": "5th Gen",
            "CheckStatus": "INFO"
        },
        "Vendor": {
            "CheckResult": "GenuineIntel",
            "CheckStatus": "INFO"
        },
        "CPU count": {
            "CheckResult": "1",
            "CheckStatus": "INFO"
        },
        "CPU frequency": {
            "CheckResult": {
                "Core 0": {
                    "CheckResult": "1 MHz",
                    "CheckStatus": "INFO",
                    "Verbosity": 1
                }},
            "CheckStatus": "INFO"
        },
    },
    "CheckStatus": "INFO"
}
