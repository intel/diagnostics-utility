#!/usr/bin/env bash
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

# Using global variables to pass information
# from one function to the next
OUTPUT=''   # Output of running the check commands
STATUS=''   # Result of the check (ERROR/WARING/INFO)
HOWTOFIX='' # Information on how to fix problems
MESSAGE=''  # Information to display in verbose mode
VALUE=''    # Information extracted from check output
RESULT=''   # Final summary

parse_args() {
	case "$1" in
	--get_metadata)
		get_metadata
		;;
	--get_summary)
		get_summary
		;;
	--get_api_version)
		get_api_version
		;;
	*) exit ;;
	esac
}

run_check() {
	# Run the check
	# * Capture stdout and stdin in OUTPUT
	# * Return exit code next step
	if OUTPUT=$(ulimit -a 2>&1); then
		# Enable the next step
		return 0
	else
		# Flag problematic run as an ERROR
		STATUS=ERROR
		MESSAGE="${OUTPUT//$'\n'/\\\\n}"
		HOWTOFIX="Make sure that 'ulimit' is found with the 'PATH' environment variable"
		VALUE='{}'
		return 1
	fi
}

parse_output() {

	# Variable to construct information extracted from OUTPUT
	INFORMATION=''

	# Validate OUTPUT line by line, and extract information
	while IFS= read -r line; do
		# Parse each line
		# https://regex101.com/r/7vNIja/3
		resource='[-\w\s]+\b'
		option='[(][^)]+[)]'
		limit='unlimited|\d+'
		pattern="^($resource)\s+($option)\s+($limit)\$"
		if ! echo "$line" | grep -qP "$pattern"; then
			# The current line does not match the expected pattern
			# Issue the warning information, and break
			STATUS=WARNING
			MESSAGE="Can not parse check output line:[$line]"
			HOWTOFIX="Make sure that the 'ulimit' application supports the '-a' option'"
			VALUE='{}'
			return 1
		fi

		# The current line does match the expected pattern
		# We could create a PASS/FAIL check by checking the limits for minimum
		# requirements
		# For demonstration purposes, this example simply reformats OUTPUT
		# results as INFO.
		r=$(echo "$line" | grep -oP "^$resource")
		l=$(echo "$line" | grep -oP "$limit\$")
		INFORMATION+=$(
			cat <<-LINE
				"$r": {
				  "Value": "$l",
				  "RetVal": "INFO"
				},
			LINE
		)

	done <<<"$OUTPUT"

	# All lines match the expected pattern
	# Make the formatted INFORMATION available as INFO
	STATUS=INFO
	MESSAGE="Output presented with expected semantics"
	HOWTOFIX='-'
	VALUE="{ ${INFORMATION%,} }"

	return 0
}

create_report() {

	read -r -d '' RESULT <<-JSON
		{ 
			"Value": {
		  "User resources limits": {
		    "Command": "ulimit -a",
		    "RetVal": "${STATUS}",
				"Message": "${MESSAGE}",
				"HowToFix": "${HOWTOFIX}",
		    "Value": ${VALUE}
		    }
		  }
		}
	JSON

	# Flatten the JSON result into the expected string
	# * Remove new-line
	# * Escape double-quotes
	RESULT="${RESULT//$'\n'/}"
	RESULT="${RESULT//\"/\\\"}"
}

get_metadata() {
	# Retrieve the metadata for this test, and provide the results in the prescribed JSON format

	cat <<-META
		{
		  "name": "user_resources_limits_check",
		  "type": "Data",
		  "tags": "sysinfo,compile,runtime,host,target",
		  "descr": "List the user limits of each resource.",
		  "dataReq": "{}",
		  "merit": 0,
		  "timeout": 5,
		  "version": 1,
		  "run": ""
		}
	META
}

get_summary() {
	# Run the test, and provide the results in the prescribed JSON format
	run_check && parse_output
	create_report
	cat <<-SUMMARY
		{
			"result": "$RESULT" 
		}
	SUMMARY
	return 0
}

get_api_version() {
	# Print the version of this checker API
	printf "0.1\n"
	return 0
}

# `main` entry to script
parse_args "$@"
