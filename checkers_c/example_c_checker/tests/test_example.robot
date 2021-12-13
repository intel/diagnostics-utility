#!/usr/bin/env robot

*** Variables ***
${RESOURCES}         ${CURDIR}
${CHECKER}           example_c_check_exe

*** Settings ***
Resource    ${RESOURCES}/../robot/util/extensions.robot

*** Test Cases ***
Basic Run
    ${COMMAND}=    Set Variable    ${CHECKER}
    Run Command And Compare Status    ${COMMAND}    0
