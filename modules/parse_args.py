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

import argparse

from pathlib import Path


def create_parser(version: str):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="The Diagnostics Utility for oneAPI is a tool "
                    "designed to diagnose the system status for using Intel® software.",
        epilog=f"Important notes:\n"
               f"\n"
               f"1. The most popular use cases for Utility:\n"
               f" - For GPU diagnostics run 'python3 diagnostics.py --select gpu'\n"
               f" - To get all information run 'python3 diagnostics.py --select all'\n"
               f"\n"
               f"2. Explanation of result status:\n"
               f"PASS - the check passed, no further information will be given.\n"
               f"FAILED - the check ran successfully but the check found a\n"
               f"problem with the expected result. For example, if a GPU check\n"
               f"is run on a system that does not have a GPU, the check will\n"
               f"fail. A brief description will indicate why the check failed.\n"
               f"ERROR - check was not able to run. Possible causes:\n"
               f"- current user does not have permissions to access information\n"
               f"that the check is looking for. (Example: check is looking\n"
               f"for the driver version, but the driver is not accessible to\n"
               f"the current user).\n"
               f"- software or hardware is not initialized.\n"
               f"WARNING - check ran successfully and but found incompatible or incorrect information.\n"
               f"   A brief description will indicate why.\n"
               f"\n"
               f"3. Basic rules for how to interpret results:\n"
               f"   - Each category of checks contains multiple checks with different level of details.\n"
               f"   Please go through all checks and analyze all failures before deciding on what is causing "
               f"the problem.\n"
               f"   Some checks only report that information is not available, while other checks provide\n"
               f"   diagnostics to indicate what might the problem might be. \n"
               f"   Please read all failures\\infos to evaluate the results of the checks.\n"
               f"   - Using verbose mode (-v) with or without other parameters will display\n"
               f"   output in different formats which may help you determine the root cause of the problems."
               f"\n"
               f"\n"
               f"4. For more details see online documentation:\n"
               f"   https://www.intel.com/content/www/us/en/develop/documentation/diagnostic-utility-user-guide/top.html \n"  # noqa: E501
               f"\n"
               f"Diagnostics Utility for oneAPI {version}\n"
               f"Copyright (C) Intel Corporation. All rights reserved.",
        add_help=False
    )
    group_check_run = parser.add_mutually_exclusive_group()
    group_output_format = parser.add_mutually_exclusive_group()
    group_update_format = parser.add_mutually_exclusive_group()
    group_check_run.add_argument(
        "--select",
        nargs="+",
        type=str,
        default=["not_initialized"],
        help="Select checks to run by group name or check name.\n"
             "Each check can belong to one or more groups.\n"
             "To view all available checks with their names and marked groups,\n"
             "run the Diagnostics Utility for oneAPI\n"
             "with the \"--list\" option."
    )
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="Show list of available checks."
    )
    group_check_run.add_argument(
        "-c", "--config",
        type=Path,
        metavar="PATH_TO_CONFIG",
        help="Path to the JSON config file to run a group of checks or a specific check."
    )
    group_output_format.add_argument(
        "-o", "--output",
        type=Path,
        metavar="PATH_TO_OUTPUT",
        default=f"{Path.home()}/intel/diagnostics/logs",
        help="Path to the folder for saving the console output file and\n"
             "the JSON file with the results of the performed checks.\n"
    )
    group_output_format.add_argument(
        "-t", "--terminal_output",
        action="store_true",
        help="Output to the terminal window without saving additional output files."
    )
    group_update_format.add_argument(
        "-u", "--update",
        action="store_true",
        help="Download new databases if they are available."
    )
    parser.add_argument(
        "-p", "--path",
        nargs="+",
        type=str,
        help="Add paths to folders with checker files or to specific checker files\n"
             "using the environment variable DIAGUTIL_PATH. Paths from this environment are an additional\n"
             "way to load checks."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force the program to run on any operating system.")
    parser.add_argument(
        "-v", "--verbosity",
        action="count",
        help="Increase output verbosity. By default, this utility prints\n"
             "FAILUREs and ERRORs only. Use -v for get more details.\n"
             "Add additional 'v' (like -vvvv) to increase the amount of details",
        default=-1
    )
    parser.add_argument(
        "-V", "--version",
        action="version",
        version=f"Diagnostics Utility for oneAPI\n"
                f"Version: {version}\n"
                f"Date of creation: @DATE_OF_CREATION@\n"
                f"Git commit: @GIT_COMMIT@\n"
                f"Copyright (C) Intel Corporation. All rights reserved.",
        help="Show version and exit."
    )
    parser.add_argument(
        "-h", "--help",
        action="help",
        help="Show this help message and exit.",
        default=argparse.SUPPRESS)
    parser.add_argument(
        "-j", "--json",
        action="store_true",
        help="Print json onto STDOUT.")
    return parser
