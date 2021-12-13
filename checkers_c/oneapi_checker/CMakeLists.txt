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

set(CHECKERS_LIB_NAME oneapi_checker)

AUX_SOURCE_DIRECTORY(src CHECKERS_SRC)

add_library(${CHECKERS_LIB_NAME} SHARED ${CHECKERS_SRC})
target_include_directories(${CHECKERS_LIB_NAME} PRIVATE include)
target_include_directories(${CHECKERS_LIB_NAME} PRIVATE ../../include)
target_link_libraries(${CHECKERS_LIB_NAME} json-c-static sqlite3)

install(TARGETS ${CHECKERS_LIB_NAME} DESTINATION ${SOURCES_INSTALL_PREFIX}/checkers_c)

if(DEV_PACKAGE)
    set(CHECKERS_EXE_NAME oneapi_checker_exe)

    add_executable (${CHECKERS_EXE_NAME} ${CHECKERS_SRC})
    target_include_directories(${CHECKERS_EXE_NAME} PRIVATE include)
    target_include_directories(${CHECKERS_EXE_NAME} PRIVATE ../../include)
    target_link_libraries(${CHECKERS_EXE_NAME} json-c-static sqlite3)

    install(TARGETS ${CHECKERS_EXE_NAME} DESTINATION ${SOURCES_INSTALL_PREFIX}/checkers_c)
endif()
