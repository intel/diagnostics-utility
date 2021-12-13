/*******************************************************************************
Copyright Intel Corporation.
This software and the related documents are Intel copyrighted materials, and your use of them 
is governed by the express license under which they were provided to you (License).
Unless the License provides otherwise, you may not use, modify, copy, publish, distribute, disclose 
or transmit this software or the related documents without Intel's prior written permission.
This software and the related documents are provided as is, with no express or implied warranties, 
other than those that are expressly stated in the License.

*******************************************************************************/

#ifndef __CHECKER_LIST_INTERFACE_H__
#define __CHECKER_LIST_INTERFACE_H__

#ifdef __cplusplus
extern "C" {  
#endif  

/**
 * @brief Get api version that checkers use
 * @return String with api version
 */
char* get_api_version(void);

/**
 * @brief Get list of the Checks in the library
 * @return Array of the pointers to checkers
 */
__attribute__((const)) struct Check** get_check_list(void);

#ifdef __cplusplus  
} // extern "C"  
#endif

#endif /* __CHECKER_LIST_INTERFACE_H__ */
