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

cmake_minimum_required(VERSION 3.7)

set(TOOL_NAME Diagnostics)
set(PROJ_VERSION 1)
set(MAJOR_VERSION 0)

project(${TOOL_NAME})

set(CMAKE_BUILD_DIR "${CMAKE_CURRENT_BINARY_DIR}")

set(CMAKE_C_STANDARD 99)
set(CMAKE_CXX_STANDARD 11)

if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
  set(CMAKE_INSTALL_PREFIX "${CMAKE_BUILD_DIR}" CACHE PATH "..." FORCE)
endif()

set(SOURCES_INSTALL_PREFIX install/ CACHE PATH "..." FORCE)

option(DEV_PACKAGE "Build dev package" OFF)
option(BUILD_TESTS "Build test programs" OFF)
option(COVERAGE "Add coverage flags" OFF)
option(BUILD_DOCS "Build html documents" OFF)

install(PROGRAMS diagnostics.py
    DESTINATION ${SOURCES_INSTALL_PREFIX}
    PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_WRITE GROUP_EXECUTE WORLD_READ WORLD_EXECUTE
  )

install(DIRECTORY databases
    DESTINATION ${SOURCES_INSTALL_PREFIX}
    PATTERN "src" EXCLUDE
  )

install(FILES README.md DESTINATION ${SOURCES_INSTALL_PREFIX})

install(DIRECTORY configs
    DESTINATION ${SOURCES_INSTALL_PREFIX}
  )

install(DIRECTORY licensing
    DESTINATION ${SOURCES_INSTALL_PREFIX}
  )

install(DIRECTORY modules
    DESTINATION ${SOURCES_INSTALL_PREFIX}
    PATTERN "mock" EXCLUDE
    PATTERN "*test*" EXCLUDE
    PATTERN "CMakeLists.*" EXCLUDE
    PATTERN "*__pycache__*" EXCLUDE
  )

if(NOT DEV_PACKAGE)
  install(DIRECTORY checkers_py
      DESTINATION ${SOURCES_INSTALL_PREFIX}
      USE_SOURCE_PERMISSIONS
      PATTERN "mock" EXCLUDE
      PATTERN "*test*" EXCLUDE
      PATTERN "CMakeLists.*" EXCLUDE
      PATTERN "*__pycache__*" EXCLUDE
      PATTERN "example_*" EXCLUDE
      PATTERN "merge_json.py" EXCLUDE
      PATTERN "*.json" EXCLUDE
    )

  install(FILES ${CMAKE_SOURCE_DIR}/checkers_py/data/oneapi_names_map_public.json
      DESTINATION ${SOURCES_INSTALL_PREFIX}/checkers_py/data
      RENAME oneapi_names_map.json
    )

  install(DIRECTORY checkers_exe
      DESTINATION ${SOURCES_INSTALL_PREFIX}
      USE_SOURCE_PERMISSIONS
      PATTERN "mock" EXCLUDE
      PATTERN "*test*" EXCLUDE
      PATTERN "CMakeLists.*" EXCLUDE
      PATTERN "*__pycache__*" EXCLUDE
      PATTERN "example_*" EXCLUDE
    )
else()
  install(DIRECTORY checkers_py
      DESTINATION ${SOURCES_INSTALL_PREFIX}
      USE_SOURCE_PERMISSIONS
      PATTERN "mock" EXCLUDE
      PATTERN "*test*" EXCLUDE
      PATTERN "CMakeLists.*" EXCLUDE
      PATTERN "*__pycache__*" EXCLUDE
      PATTERN "merge_json.py" EXCLUDE
      PATTERN "*.json" EXCLUDE
    )

  install(FILES ${CMAKE_SOURCE_DIR}/checkers_py/data/oneapi_names_map_public.json
      DESTINATION ${SOURCES_INSTALL_PREFIX}/checkers_py/data
      RENAME oneapi_names_map.json
    )

  install(DIRECTORY checkers_exe
      DESTINATION ${SOURCES_INSTALL_PREFIX}
      USE_SOURCE_PERMISSIONS
      PATTERN "mock" EXCLUDE
      PATTERN "*test*" EXCLUDE
      PATTERN "CMakeLists.*" EXCLUDE
      PATTERN "*__pycache__*" EXCLUDE
    )
endif()

include(FetchContent)
set(JSON_C_BASE_DIR "${CMAKE_BUILD_DIR}/json-c")
FetchContent_Declare(
    json_c
    GIT_REPOSITORY https://github.com/json-c/json-c.git
    GIT_TAG        json-c-0.15-20200726
    SOURCE_DIR "${JSON_C_BASE_DIR}/json-c"
    BINARY_DIR "${JSON_C_BASE_DIR}/json-c-build"
    SUBBUILD_DIR "${JSON_C_BASE_DIR}/json-c-subbuild"
    CMAKE_ARGS -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
                -DCMAKE_SYSTEM_NAME=${CMAKE_SYSTEM_NAME}
                -DBUILD_SHARED_LIBS=OFF
                -DBUILD_STATIC_LIBS=ON
                -DDISABLE_STATIC_FPIC=ON
  )
FetchContent_GetProperties(json_c)
if(NOT json_c_POPULATED)
  FetchContent_Populate(json_c)
  add_subdirectory(${json_c_SOURCE_DIR} ${json_c_BINARY_DIR} EXCLUDE_FROM_ALL)
endif()
include_directories(${JSON_C_BASE_DIR} "${JSON_C_BASE_DIR}/json-c-build")

if(BUILD_TESTS)
  set(GTEST_BASE_DIR "${CMAKE_BUILD_DIR}/gtest")
  FetchContent_Declare(
      googletest
      GIT_REPOSITORY https://github.com/google/googletest.git
      GIT_TAG        release-1.11.0
      SOURCE_DIR "${GTEST_BASE_DIR}/googletest"
      BINARY_DIR "${GTEST_BASE_DIR}/googletest-build"
      SUBBUILD_DIR "${GTEST_BASE_DIR}/googletest-subbuild"
      CMAKE_ARGS -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
                  -DCMAKE_SYSTEM_NAME=${CMAKE_SYSTEM_NAME}
                  -DCMAKE_CXX_FLAGS=${GTEST_CXX_FLAGS}
                  -DCMAKE_C_FLAGS=${GTEST_C_FLAGS}
                  -DBUILD_GMOCK=ON
                  -DBUILD_GTEST=ON
    )
  FetchContent_GetProperties(googletest)
  if(NOT googletest_POPULATED)
    FetchContent_Populate(googletest)
    add_subdirectory(${googletest_SOURCE_DIR} ${googletest_BINARY_DIR} EXCLUDE_FROM_ALL)
  endif()
  enable_testing()
endif()

if(CMAKE_COMPILER_IS_GNUCC)
  set(SECURITY_COMPILATION_FLAGS " \
      -fPIE \
      -fPIC \
      -pie"
    )

  set(C_SECURITY_COMPILATION_FLAGS " \
      -Wall \
      -fno-strict-overflow \
      -fno-delete-null-pointer-checks \
      -fwrapv \
      -Wformat=2 \
      -D_FORTIFY_SOURCE=2 \
      -Wformat-security \
      -Werror=format-security \
      -fstack-protector-strong \
      ${SECURITY_COMPILATION_FLAGS} \
      -fstack-clash-protection \
      -mindirect-branch-register"
    )

  set(C_INTEGER_OVERFLOW_AND_COMPARISON_FLAGS " \
      -Wtype-limits \
      -Wstrict-overflow=5 \
      -fstrict-overflow \
      -Wsign-compare"
    )

  set(SECURITY_LINK_FLAGS " \
      -Wl,-z,relro \
      -Wl,-z,now \
      -z noexecstack"
    )

  set(SECURITY_EXE_LINK_FLAGS " \
      -Wl,-pie"
    )

  set(CMAKE_EXE_LINKER_FLAGS " \
      ${CMAKE_EXE_LINKER_FLAGS} \
      ${SECURITY_LINK_FLAGS} \
      ${SECURITY_EXE_LINK_FLAGS}"
    )

  set(CMAKE_SHARED_LINKER_FLAGS " \
      ${CMAKE_SHARED_LINKER_FLAGS} \
      ${SECURITY_LINK_FLAGS}"
    )

  set(CMAKE_C_FLAGS " \
      ${CMAKE_C_FLAGS} \
      ${C_SECURITY_COMPILATION_FLAGS} \
      ${C_INTEGER_OVERFLOW_AND_COMPARISON_FLAGS}"
    )

  set(CMAKE_CXX_FLAGS " \
      ${CMAKE_CXX_FLAGS} \
      ${SECURITY_COMPILATION_FLAGS}"
    )
endif()

if(COVERAGE)
  set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} --coverage")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} --coverage")
  set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} --coverage")
endif()

if(BUILD_DOCS)
  execute_process(COMMAND sphinx-build -b html ${CMAKE_SOURCE_DIR}/docs/ ${CMAKE_BUILD_DIR}/docs)
  install(DIRECTORY ${CMAKE_BUILD_DIR}/docs
      DESTINATION ${SOURCES_INSTALL_PREFIX}
    )
endif()

add_subdirectory(checkers_c)
