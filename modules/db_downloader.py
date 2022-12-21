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

import json
import logging

from hashlib import sha384
from urllib import request
from urllib.error import URLError
from pathlib import Path
from itertools import filterfalse
from typing import List, Dict, Optional, Tuple

from modules.check import BaseCheck
from modules.files_helper import get_json_content_from_file
from modules.printing.printer import print_ex

DEFAULT_DATABASES_FOLDER = Path(__file__).parent.parent.resolve() / "databases"
DOWNLOADED_DATABASES_FOLDER = Path.home() / "intel" / "diagnostics" / "databases"


def _get_available_resource(resources: List[str]) -> Optional[str]:
    available_resource = None
    for resource in resources:
        if "intel.com" not in resource:
            logging.warning("Downloading from domains other than Intel is prohibited. Link will be skipped.")
            continue
        try:
            request.urlopen(f"{resource}/metadata.json", timeout=5)
        except URLError as error:
            logging.warning(f"Resource ({resource}) not available with message: {error}")
            continue
        available_resource = resource
        break
    return available_resource


def _download_metadata(available_resource: str) -> Optional[Dict]:
    content = None
    metadata_url = f"{available_resource}/metadata.json"
    try:
        responce = request.urlopen(metadata_url, timeout=15)
        content = json.loads(responce.read().decode("utf-8"))
    except URLError as error:
        logging.warning(
            f"Cannot download metadata from ({metadata_url}) due to: {error}"
        )
    return content


def _is_db_compatible_with_checks(db_info: Dict, checks: List[BaseCheck]) -> bool:
    is_db_compatible_with_checks = True
    check_compatibility = list(filterfalse(
        lambda x: not list(set(db_info["compatibility"].keys() & set([x.get_metadata().name]))),
        checks
    ))

    for check in check_compatibility:
        check_name, check_version = check.get_metadata().name, check.get_metadata().version
        if check_version not in db_info["compatibility"][check_name]:
            is_db_compatible_with_checks = False
            break

    return is_db_compatible_with_checks


def _check_updates(
        default_metadata: Dict, downloaded_metadata: Dict, all_checks: List[BaseCheck]) -> Dict:
    result: Dict = {}
    for db_type, db_list in default_metadata["databases"].items():
        if db_type not in downloaded_metadata["databases"]:
            continue
        default_db = db_list[0]
        newer_database = None
        for db in downloaded_metadata["databases"][db_type]:
            if db["installation_name"] == default_db["installation_name"] and \
               db["date_of_creation"] > default_db["date_of_creation"]:
                if _is_db_compatible_with_checks(db, all_checks):
                    newer_database = db
        if newer_database is not None:
            result.update({db_type: [newer_database]})
    return result


def _get_metadata_of_all_installed_databases() -> Dict:
    result = get_json_content_from_file(DEFAULT_DATABASES_FOLDER / "metadata.json")
    if (DOWNLOADED_DATABASES_FOLDER / "metadata.json").exists():
        installed_metadata = get_json_content_from_file(DOWNLOADED_DATABASES_FOLDER / "metadata.json")
        result["resources"] = list(set([*result["resources"], *installed_metadata["resources"]]))
        for db_type, db_type_subtree in installed_metadata["databases"].items():
            result["databases"].update({db_type: db_type_subtree})
    return result


def are_database_updates_available(all_checks: List[BaseCheck]) -> Tuple[Optional[str], Dict, Dict]:
    DOWNLOADED_DATABASES_FOLDER.mkdir(parents=True, exist_ok=True)

    default_metadata_content = _get_metadata_of_all_installed_databases()
    available_resource = _get_available_resource(default_metadata_content["resources"])
    if available_resource is None:
        logging.warning(
            "All servers are unavailable or there is no internet connection. "
            "Unable to check for the existence of database updates."
        )
        return None, default_metadata_content, {}
    downloaded_metadata_content = _download_metadata(available_resource)
    if not downloaded_metadata_content:
        logging.warning(
            "Unable to determine if database updates are available."
        )
        return available_resource, default_metadata_content, {}

    newer_databases = _check_updates(default_metadata_content, downloaded_metadata_content, all_checks)
    if len(newer_databases):
        downloaded_metadata_content["databases"] = newer_databases
    return available_resource, downloaded_metadata_content, newer_databases


def update_databases(
        resource: Optional[str], metadata: Dict, databases: Dict) -> int:
    return_code = 0
    if resource is None:
        print_ex("Cannot connect to update server to check for updates.")
        return 1
    if not len(databases):
        print_ex("No available updates for existing databases.")
        return return_code
    for db_type, db_list in databases.items():
        database = db_list[0]
        try:
            database_url = f"""{resource}/{database["name"]}"""
            responce = request.urlopen(database_url, timeout=15)
            binary = responce.read()
            hash = sha384(binary).hexdigest()
            if hash != database["hash"]:
                raise ValueError(
                    f"""The database hash is not valid. """
                    f"""Database ({database["installation_name"]}) not updated."""
                )
            with open(f"""{DOWNLOADED_DATABASES_FOLDER}/{database["installation_name"]}""", "wb") as outfile:
                outfile.write(binary)
        except URLError as error:
            logging.warning(
                f"Cannot download database from ({database_url}) due to: {error}"
            )
            metadata["databases"].pop(db_type)
            return_code += 1
        except ValueError as error:
            logging.error(str(error))
            metadata["databases"].pop(db_type)
            return_code += 1
    with open(f"{DOWNLOADED_DATABASES_FOLDER}/metadata.json", "w") as outfile:
        json.dump(metadata, outfile, indent=4)
    print_ex(f"Compatibility database is updated successfully in {DOWNLOADED_DATABASES_FOLDER}.")
    return return_code


def print_available_updates(databases: Dict) -> None:
    if not len(databases):
        print_ex("No available updates for existing databases.")
        return
    checks_with_new_db = set()
    for db_list in databases.values():
        database = db_list[0]
        checks_with_new_db = checks_with_new_db | set(database["compatibility"].keys())
    print_ex("")
    print_ex(f"""New databases are available for checks: {", ".join(checks_with_new_db)}""")
    print_ex("Run ./diagnostics.py --update to update databases.")
    print_ex("")
