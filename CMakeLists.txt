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

project(diagnostics)

set(CMAKE_C_STANDARD 99)
set(CMAKE_CXX_STANDARD 11)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE "Release" CACHE STRING "..." FORCE)
endif()

set(CMAKE_BUILD_DIR "${CMAKE_CURRENT_BINARY_DIR}")
if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
  set(CMAKE_INSTALL_PREFIX "${CMAKE_BUILD_DIR}" CACHE PATH "..." FORCE)
endif()

set(SOURCES_INSTALL_PREFIX install/ CACHE PATH "..." FORCE)

option(BUILD_TESTS "Build test programs" OFF)
option(COVERAGE "Add coverage flags" OFF)
option(BUILD_DOCS "Build html documents" OFF)
# option(DEV_PACKAGE "Build dev package" OFF)

if(NOT DEFINED OS)
  set(OS "linux")
elseif(${OS} STREQUAL "LIN" OR ${OS} STREQUAL "LINUX")
  set(OS "linux")
elseif(${OS} STREQUAL "WIN" OR ${OS} STREQUAL "WINDOWS")
  set(OS "windows")
else()
  message(SEND_ERROR "Operation systems name '${OS}' is incorrect. Please use LIN or WIN")
endif()

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
    USE_SOURCE_PERMISSIONS
    PATTERN "linux" EXCLUDE
    PATTERN "windows" EXCLUDE
  )

  install(DIRECTORY configs/${OS}/
      DESTINATION ${SOURCES_INSTALL_PREFIX}/configs
      USE_SOURCE_PERMISSIONS
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
    PATTERN "parse_args.py" EXCLUDE
  )

execute_process(COMMAND git rev-parse HEAD 
    OUTPUT_VARIABLE GIT_COMMIT
    OUTPUT_STRIP_TRAILING_WHITESPACE
  )

execute_process(COMMAND git log -1 --date=format:"%d/%m/%Y %T" --format="%ad"
    OUTPUT_VARIABLE DATE_OF_CREATION
    OUTPUT_STRIP_TRAILING_WHITESPACE
  )

configure_file(modules/parse_args.py ${SOURCES_INSTALL_PREFIX}/modules/parse_args.py
    @ONLY
  )

install(DIRECTORY checkers_py
    DESTINATION ${SOURCES_INSTALL_PREFIX}
    USE_SOURCE_PERMISSIONS
    PATTERN "mock" EXCLUDE
    PATTERN "*test*" EXCLUDE
    PATTERN "CMakeLists.*" EXCLUDE
    PATTERN "*__pycache__*" EXCLUDE
    PATTERN "merge_json.py" EXCLUDE
    PATTERN "*.json" EXCLUDE
    PATTERN "linux" EXCLUDE
    PATTERN "windows" EXCLUDE
  )

install(DIRECTORY checkers_py/${OS}/
      DESTINATION ${SOURCES_INSTALL_PREFIX}/checkers_py
      USE_SOURCE_PERMISSIONS
      PATTERN ".gitkeep" EXCLUDE
      PATTERN "mock" EXCLUDE
      PATTERN "*test*" EXCLUDE
      PATTERN "CMakeLists.*" EXCLUDE
      PATTERN "*__pycache__*" EXCLUDE
      PATTERN "merge_json.py" EXCLUDE
      PATTERN "*.json" EXCLUDE
  )

if(${OS} STREQUAL "linux")
  install(FILES ${CMAKE_SOURCE_DIR}/checkers_py/${OS}/data/oneapi_names_map.json
      DESTINATION ${SOURCES_INSTALL_PREFIX}/checkers_py/data/)
endif()

install(DIRECTORY checkers_exe
    DESTINATION ${SOURCES_INSTALL_PREFIX}
    USE_SOURCE_PERMISSIONS
    PATTERN "mock" EXCLUDE
    PATTERN "*test*" EXCLUDE
    PATTERN "CMakeLists.*" EXCLUDE
    PATTERN "*__pycache__*" EXCLUDE
    PATTERN "linux" EXCLUDE
    PATTERN "windows" EXCLUDE
  )

install(DIRECTORY checkers_exe/${OS}/
    DESTINATION ${SOURCES_INSTALL_PREFIX}/checkers_exe
    USE_SOURCE_PERMISSIONS
    PATTERN ".gitkeep" EXCLUDE
    PATTERN "mock" EXCLUDE
    PATTERN "*test*" EXCLUDE
    PATTERN "CMakeLists.*" EXCLUDE
    PATTERN "*__pycache__*" EXCLUDE
  )

include(FetchContent)
set(JSON_C_BASE_DIR "${CMAKE_BUILD_DIR}/json-c")
FetchContent_Declare(
    json_c
    GIT_REPOSITORY https://github.com/json-c/json-c.git
    GIT_TAG        json-c-0.15-20200726
    GIT_SHALLOW TRUE
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
  add_subdirectory(
      ${json_c_SOURCE_DIR}
      ${json_c_BINARY_DIR}
      EXCLUDE_FROM_ALL
    )
endif()
include_directories(${JSON_C_BASE_DIR} "${JSON_C_BASE_DIR}/json-c-build")

if(BUILD_TESTS)
  set(GTEST_BASE_DIR "${CMAKE_BUILD_DIR}/gtest")
  FetchContent_Declare(
      googletest
      GIT_REPOSITORY https://github.com/google/googletest.git
      GIT_TAG        release-1.11.0
      GIT_SHALLOW TRUE
      SOURCE_DIR "${GTEST_BASE_DIR}/googletest"
      BINARY_DIR "${GTEST_BASE_DIR}/googletest-build"
      SUBBUILD_DIR "${GTEST_BASE_DIR}/googletest-subbuild"
      CMAKE_ARGS -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
                  -DCMAKE_SYSTEM_NAME=${CMAKE_SYSTEM_NAME}
                  -DCMAKE_CXX_FLAGS=${GTEST_CXX_FLAGS}
                  -DCMAKE_C_FLAGS=${GTEST_C_FLAGS}
                  -DBUILD_GMOCK=ON
                  -DBUILD_GTEST=ON
                  -DBUILD_SHARED_LIBS=OFF
                  -DBUILD_STATIC_LIBS=ON
    )
  FetchContent_GetProperties(googletest)
  if(NOT googletest_POPULATED)
    FetchContent_Populate(googletest)
    set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
    set(BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)
    set(BUILD_STATIC_LIBS ON CACHE BOOL "" FORCE)
    add_subdirectory(
        ${googletest_SOURCE_DIR}
        ${googletest_BINARY_DIR}
        EXCLUDE_FROM_ALL
      )
  endif()
  enable_testing()
  include(GoogleTest)
endif()

if(CMAKE_COMPILER_IS_GNUCC)
  set(SECURITY_COMPILATION_FLAGS " \
      -Wall \
      -fno-strict-overflow \
      -fno-delete-null-pointer-checks \
      -fwrapv \
      -Wformat=2 \
      -D_FORTIFY_SOURCE=2 \
      -Wformat-security \
      -Werror=format-security \
      -fstack-protector-strong \
      -fPIE \
      -fPIC \
      -pie \
      -fstack-clash-protection \
      -mindirect-branch-register"
    )

  set(INTEGER_OVERFLOW_AND_COMPARISON_FLAGS " \
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
      ${SECURITY_COMPILATION_FLAGS} \
      ${INTEGER_OVERFLOW_AND_COMPARISON_FLAGS}"
    )

  set(CMAKE_CXX_FLAGS " \
      ${CMAKE_CXX_FLAGS} \
      ${SECURITY_COMPILATION_FLAGS} \
      ${INTEGER_OVERFLOW_AND_COMPARISON_FLAGS}"
    )

  if(COVERAGE)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} --coverage")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} --coverage")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} --coverage")
  endif()
endif()

if(MSVC)
  set(SECURITY_COMPILATION_FLAGS " \
      /Wall \
      /Qspectre"
    )

  set(INTEGER_OVERFLOW_AND_COMPARISON_FLAGS " \
      /GS"
    )

  set(SECURITY_LINK_FLAGS " \
      /DYNAMICBASE \
      /HIGHENTROPYVA \
      /LARGEADDRESSAWARE \
      /NXCOMPAT \
      /GUARD:CF"
    )

  # if(NOT DEV_PACKAGE AND NOT BUILD_TESTS)
  #   set(SECURITY_LINK_FLAGS " \
  #       ${SECURITY_LINK_FLAGS} \
  #       /INTEGRITYCHECK"
  #     )
  # endif()

  set(SECURITY_EXE_LINK_FLAGS " \
      /ALLOWISOLATION"
    )

  set(CMAKE_EXE_LINKER_FLAGS " \
      ${CMAKE_EXE_LINKER_FLAGS} \
      ${SECURITY_EXE_LINK_FLAGS} \
      ${SECURITY_LINK_FLAGS}"
    )

  set(CMAKE_SHARED_LINKER_FLAGS " \
      ${CMAKE_SHARED_LINKER_FLAGS} \
      ${SECURITY_LINK_FLAGS}"
    )

  set(CMAKE_C_FLAGS " \
      ${CMAKE_C_FLAGS} \
      ${SECURITY_COMPILATION_FLAGS} \
      ${INTEGER_OVERFLOW_AND_COMPARISON_FLAGS}"
    )

  set(CMAKE_CXX_FLAGS " \
      ${CMAKE_CXX_FLAGS} \
      ${SECURITY_COMPILATION_FLAGS} \
      ${INTEGER_OVERFLOW_AND_COMPARISON_FLAGS}"
    )
endif()

if(BUILD_DOCS)
  execute_process(COMMAND sphinx-build -b html ${CMAKE_SOURCE_DIR}/docs/ ${CMAKE_BUILD_DIR}/docs)
  install(DIRECTORY ${CMAKE_BUILD_DIR}/docs
      DESTINATION ${SOURCES_INSTALL_PREFIX}
    )
endif()

add_subdirectory(checkers_samples)
add_subdirectory(checkers_c)

install(SCRIPT "replace.cmake")

