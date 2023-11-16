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

import os
import re
from modules.check import CheckSummary, CheckMetadataPy
import json
from typing import List
import sqlite3


def get_api_version() -> str:
    return "0.2"


def get_check_list() -> List[CheckMetadataPy]:
    someCheck = CheckMetadataPy(
        name="oneapi_toolkit_check",
        type="Data",
        groups="default,sysinfo,compile,runtime,host,target",
        descr="This check shows information about installed oneAPI toolkits.",
        dataReq="{}",
        merit=20,
        timeout=5,
        version=2,
        run="run_oneapi_toolkit_checker"
    )
    return [someCheck]


def run_oneapi_toolkit_checker(data):
    check_result = {"CheckResult": {}, "CheckStatus": "INFO"}

    check_result["CheckResult"].update(installer_cache_check())

    check_summary = CheckSummary(
        result=json.dumps(check_result, indent=4)
    )
    return check_summary


def installer_cache_check():
    result = {"CheckResult": {}, "CheckStatus": "INFO"}
    try:
        cacheChecker = OneApiCacheChecker()
        result = cacheChecker.get_information_as_json()
    except PermissionError as err:
        result["CheckStatus"] = "ERROR"
        result["Message"] = str(err)
        result["HowToFix"] = "Try run as administrator"
    return {"OneAPI Installed products": result}


class OneApiToolkit:
    def __init__(self, id, name, version) -> None:
        self.id = id
        self.name = name
        self.version = version
        self.components: List[OneApiComponent] = []

    def __eq__(self, other):
        if not isinstance(other, OneApiToolkit):
            return NotImplemented
        return self.id == other.id and \
            self.name == other.name and \
            self.version == other.version


class OneApiComponent:
    def __init__(self, name, version, path, id) -> None:
        self.name = name
        self.version = version
        self.path = path
        self.toolkit_id = id
        self.description = ""

    def __eq__(self, other):
        if not isinstance(other, OneApiComponent):
            return NotImplemented
        return self.name == other.name and \
            self.version == other.version and \
            self.path == other.path and \
            self.toolkit_id == other.toolkit_id and \
            self.description == other.description


class OneApiCacheChecker:
    def __init__(self) -> None:
        self.installer_cache_path = self.__get_installer_cache_path()
        self.db = sqlite3.connect(os.path.join(self.installer_cache_path, "packagemanager.db"))
        self.cursor = self.db.cursor()
        self.__installed_toolkits = self.__get_toolkits_from_db()
        self.__fill_toolkits_with_components()

    def get_information_as_json(self):
        result = {"CheckResult": {}, "CheckStatus": "INFO"}

        for t in self.__installed_toolkits:
            t_result = {"CheckResult": {}, "CheckStatus": "INFO"}

            for c in t.components:
                c_result = {
                    "CheckResult": {
                        "Version": {"CheckResult": c.version, "CheckStatus": "INFO"},
                        "Description":  {"CheckResult": c.description, "CheckStatus": "INFO"},
                        "Path":  {"CheckResult": c.path, "CheckStatus": "INFO"}
                    },
                    "CheckStatus": "INFO"
                }
                t_result["CheckResult"].update({c.name: c_result})

            result["CheckResult"].update({f"oneAPI {t.name} {t.version}": t_result})
        return result

    def __get_installer_cache_path(self):
        program_data_path = os.getenv("ALLUSERSPROFILE")
        if program_data_path is None:
            program_data_path = os.getenv("PROGRAMDATA")
        if program_data_path is None:
            sys_drive_path = os.getenv("SystemDrive")
            if sys_drive_path is None:
                raise Exception("Failed to get path to ProgramData folder")
            program_data_path = os.path.join(sys_drive_path, "ProgramData")

        return os.path.join(program_data_path, "Intel", "InstallerCache")

    def __get_toolkits_from_db(self):
        self.cursor.execute('''
        SELECT record_id,id,version
        FROM package
        ''')
        db_fetch = self.cursor.fetchall()
        installed_toolkits = [
            OneApiToolkit(t[0],
                          re.search("intel\\.oneapi\\.win\\.(\\w*)\\.package", t[1]).group(1),
                          t[2])
            for t in db_fetch]
        return installed_toolkits

    def __fill_toolkits_with_components(self):
        components = self.__get_components_from_db()
        components = self.__update_components_information_from_manifest_json(components)
        for c in components:
            for t in self.__installed_toolkits:
                if (t.id == c.toolkit_id):
                    t.components.append(c)

    def __get_components_from_db(self):
        paths = self.__get_installation_paths_dict_from_db()

        self.cursor.execute('''
        SELECT component.id,component.version,component_owner.install_dir,component_owner.package
        FROM component_owner
        INNER JOIN component ON component_owner.component=component.record_id
        ''')
        db_fetch = self.cursor.fetchall()
        components = [OneApiComponent(c[0], c[1], paths[c[2]], c[3]) for c in db_fetch]
        return components

    def __get_installation_paths_dict_from_db(self):
        self.cursor.execute('''
        SELECT record_id,path
        FROM install_dir
        ''')
        db_fetch = self.cursor.fetchall()
        id_to_path_dict = {inst_dir[0]: inst_dir[1] for inst_dir in db_fetch}
        return id_to_path_dict

    def __update_components_information_from_manifest_json(self, components: List[OneApiComponent]):
        result = []
        for c in components:
            manifest_path = os.path.join(self.installer_cache_path, "PackagesCache",
                                         f"{c.name},v={c.version}", "manifest.json")
            mainfest = open(manifest_path, encoding='utf-8')
            manifest_json = json.load(mainfest)

            if not self.__is_component_visible(manifest_json):
                mainfest.close()
                continue
            c.description = self.__get_description_from_manifest_json(manifest_json)
            c.name = self.__get_name_from_manifest_json(manifest_json)
            result.append(c)
            mainfest.close()
        return result

    def __is_component_visible(self, manifest_json):
        if "visible" in manifest_json and manifest_json["visible"] is True:
            return True
        return False

    def __get_description_from_manifest_json(self, manifest_json):
        for localize in manifest_json["display"]["localized"]:
            if localize["language"] == "en-us":
                return localize["description"]
        return "Undefined"

    def __get_name_from_manifest_json(self, manifest_json):
        for localize in manifest_json["display"]["localized"]:
            if localize["language"] == "en-us":
                return localize["title"]
        return "Undefined"
