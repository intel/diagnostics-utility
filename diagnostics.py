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

import sys

from pathlib import Path
from typing import List, Optional

from modules.check import BaseCheck, load_checks_from_config, load_default_checks, load_single_checker, \
                          run_checks

from modules.db_downloader import are_database_updates_available, update_databases, print_available_updates
from modules.files_helper import configure_output_files, save_json_output_file
from modules.filter import process_filter, get_filtered_checks
from modules.os_helper import check_that_os_is_supported
from modules.parse_args import create_parser
from modules.log import configure_logger

from modules.printing import print_metadata, print_summary, print_epilog

VERSION = "2022.0.0"


def main():
    # Parse command line arguments
    parser = create_parser(VERSION)
    args = parser.parse_args()

    # Check that OS is supported
    if not args.force:
        check_that_os_is_supported()

    # Configure output files
    txt_output_file: Optional[Path] = None
    json_output_file: Optional[Path] = None
    if not args.terminal_output:
        txt_output_file, json_output_file = configure_output_files(args)

    # Configure logger
    configure_logger(args.verbosity, txt_output_file)

    checks: List[BaseCheck] = []
    if args.single_checker:  # Load single module by path
        checks.extend(load_single_checker(args.single_checker))
    elif args.config:  # Load checks from config
        checks.extend(load_checks_from_config(args.config))
    else:  # Load default checks
        checks.extend(load_default_checks())

    # If checks we not specified, tool should say that it runs with limited set pf checks
    is_filter_not_initialized = len(args.filter) == 1 and args.filter[0] == "not_initialized"
    if not args.list and is_filter_not_initialized and \
       not args.single_checker and not args.config and not args.update:
        print("Default checks will be run. To run another checks see 'python3 diagnostics.py --help'")

    # Print checks metadata
    if args.list:
        if not is_filter_not_initialized:
            checks[:] = get_filtered_checks(checks, args.filter)
        print_metadata(checks, txt_output_file)
        print_epilog(txt_output_file, None, VERSION)
        exit(0)
    elif not args.config and not args.single_checker:
        filter = process_filter(args.filter)
        checks[:] = get_filtered_checks(checks, filter)

    # Check DB updates
    print("Checking for available updates of compatibility database...")
    resource, metadata, databases = are_database_updates_available(load_default_checks())
    print("Checking for available updates completed successfully.")
    if args.update:
        exit(update_databases(resource, metadata, databases))
    else:
        print_available_updates(databases)

    # Run selected checks
    run_checks(checks)

    # Print results to user
    print_summary(checks, args.verbosity, txt_output_file)

    if json_output_file and txt_output_file:
        save_json_output_file(checks, json_output_file)

    print_epilog(txt_output_file, json_output_file, VERSION)


if __name__ == "__main__":
    sys.exit(main())
