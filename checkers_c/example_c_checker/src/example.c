/*******************************************************************************
Copyright Intel Corporation.
This software and the related documents are Intel copyrighted materials, and your use of them
is governed by the express license under which they were provided to you (License).
Unless the License provides otherwise, you may not use, modify, copy, publish, distribute, disclose
or transmit this software or the related documents without Intel's prior written permission.
This software and the related documents are provided as is, with no express or implied warranties,
other than those that are expressly stated in the License.

*******************************************************************************/

#include "checker_list_interface.h"
#include "checker_interface.h"

#include <stdio.h>
#include <sys/sysinfo.h>
#include <string.h>

#define API_VERSION "0.1"

#define SOME_JSON \
    "{\"Value\": {\"GPU (OpenCL™ Vendors)\": {\"Value\": {\"Intel\": {\"Value\": {\"OpenCL2.0\": {\"Value\": \"test\", \"Verbosity\": 2, \"Message\": \"\", \"RetVal\": \"PASS\" }, \"OpenCL1.2\": {\"Value\": \"test\", \"Verbosity\": 2, \"Message\": \"Please do something\", \"RetVal\": \"ERROR\" }}, \"Verbosity\": 1, \"Message\": \"\", \"RetVal\": \"PASS\" }, \"AMD\": {\"Value\": {\"OpenCL1.0\": {\"Value\": \"test\", \"Verbosity\": 1, \"Message\": \"\", \"RetVal\": \"PASS\" }}, \"Verbosity\": 1, \"Message\": \"\", \"RetVal\": \"PASS\" }}, \"RetVal\": \"PASS\", \"Verbosity\": 0, \"Message\": \"\" }, \"Test1\": {\"Value\": \"test\", \"Message\": \"\", \"RetVal\": \"PASS\" }}}"

char some_result[1024 * 100];
char api_version[MAX_STRING_LEN];

struct CheckResult example(char *data)
{
    sprintf(some_result, "%s", SOME_JSON);

    struct CheckResult ret = {.result = some_result};

    return ret;
}

int main()
{
    printf("%s", SOME_JSON);
    return 0;
}

REGISTER_CHECKER(g_example,
                 "example_c_check",
                 "GetData",
                 "example,c",
                 "This is an example of cpp module.",
                 "{}",
                 "user",
                 10,
                 "1.0",
                 example)

static struct Check *checkers[] =
    {&g_example, NULL};

char *get_api_version(void)
{
    sprintf(api_version, "%s", API_VERSION);
    return api_version;
}

__attribute__((const)) struct Check **get_check_list(void)
{
    return checkers;
}
