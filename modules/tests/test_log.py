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

import tempfile  # noqa: E402
import unittest  # noqa: E402
from unittest.mock import patch  # noqa: E402

import modules.log as log  # noqa: E402


class TestVerbosity2LogLevel(unittest.TestCase):

    def test_set_correct_verbosity_level(self):
        verbosity_level = -1
        expected = 30

        actual = log._verbosity2loglevel(verbosity_level)

        self.assertEqual(expected, actual)

    def test_set_large_verbosity_level_is_correct(self):
        verbosity_level = 10
        expected = 10

        actual = log._verbosity2loglevel(verbosity_level)

        self.assertEqual(expected, actual)

    def test_set_incorrect_verbosity_level(self):
        self.assertRaises(ValueError, log._verbosity2loglevel, -2)


class TestConfigureLogger(unittest.TestCase):

    def test_configure_logger_no_raise_error(self):
        log.configure_logger(0)

    def test_configure_logger_second_time_no_raise_error(self):
        log.configure_logger(0)
        log.configure_logger(0)

    @unittest.skipIf(platform.system(
    ) == "Windows", "does not work on Windows")
    def test_configure_logger_second_time_when_file_handler_exists_no_raise_error(self):
        with tempfile.NamedTemporaryFile() as temp:
            log.configure_logger(0)
            log.configure_file_logging(0, temp.name)
            log.configure_logger(0)

    @unittest.skipIf(platform.system(
    ) == "Linux", "Exception on Windows")
    def test_configure_file_logging(self):
        self.assertRaises(Exception, log.configure_file_logging, 0, '')

    @unittest.skipIf(platform.system(
    ) == "Linux", "Exception on Windows")
    @patch("logging.FileHandler", return_value=["data"])
    def test_configure_file_logging_err(self, mocked_FileHandler):
        self.assertRaises(Exception, log.configure_file_logging, 0, '')


if __name__ == '__main__':
    unittest.main()
