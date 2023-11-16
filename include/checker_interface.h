/*******************************************************************************
Copyright Intel Corporation.
This software and the related documents are Intel copyrighted materials, and
your use of them is governed by the express license under which they were
provided to you (License). Unless the License provides otherwise, you may not
use, modify, copy, publish, distribute, disclose or transmit this software or
the related documents without Intel's prior written permission. This software
and the related documents are provided as is, with no express or implied
warranties, other than those that are expressly stated in the License.

*******************************************************************************/

#ifndef __CHECKER_INTERFACE_H__
#define __CHECKER_INTERFACE_H__

#ifdef __cplusplus
extern "C" {
#endif

#include <stddef.h>

#define MAX_STRING_LEN 500

struct CheckMetadata {
  char name[MAX_STRING_LEN];
  char type[MAX_STRING_LEN];
  char groups[MAX_STRING_LEN];
  char descr[MAX_STRING_LEN];
  char dataReq[MAX_STRING_LEN];
  int merit;
  int timeout;
  int version;
};

struct CheckResult {
  char *result;
};

struct Check {
  struct CheckMetadata metadata;
  struct CheckResult (*run)(char *);
};

#define REGISTER_CHECKER(VAR, NAME, TYPE, GROUPS, DESCR, DATAREQ, MERIT,      \
                         TIMEOUT, VER, RUN)                                   \
  struct Check VAR = {{(NAME), (TYPE), (GROUPS), (DESCR), (DATAREQ), (MERIT), \
                       (TIMEOUT), (VER)},                                     \
                      (RUN)};

#ifdef __cplusplus
}  // extern "C"
#endif

#endif /* __CHECKER_INTERFACE_H__ */
