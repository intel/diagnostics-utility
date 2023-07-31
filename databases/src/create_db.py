#!/usr/bin/env python3
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

import argparse
import sqlite3
import pandas
import json

from hashlib import sha384
from pathlib import Path
from datetime import date
from typing import Dict


DB_NAME = "compatibility_map.db"


def create_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False
    )
    parser.add_argument(
        "-s", "--spreadsheet",
        type=Path,
        metavar="PATH_TO_SPREADSHEET",
        default=Path("./oneAPI_compatibility_map.xlsx"),
        help="Path to the spreadsheet for creation compatibility database."
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        metavar="PATH_TO_OUTPUT",
        default=Path("./"),
        help="Path to the folder for saving the database file."
    )
    parser.add_argument(
        "-m", "--metadata",
        type=Path,
        metavar="PATH_TO_EXISTING_METADATA",
        default=Path("../metadata.json"),
        help="Metadata to update."
    )
    parser.add_argument(
        "-v", "--version",
        type=str,
        metavar="DB_PACKAGE_VERSION",
        required=True,
        help="Diagnostics package version."
    )
    return parser


def read_excel(spreadsheet: Path):
    data = None
    try:
        data = pandas.read_excel(
            str(spreadsheet), sheet_name=None, header=0)
    except ValueError as e:
        print(e)
    return data


def create_db_conn(database_file: Path):
    conn = None
    try:
        if not database_file.exists():
            conn = sqlite3.connect(database_file)
        else:
            raise Exception(f"The database {database_file} already exists")
    except Exception as e:
        print(e)
    return conn


def create_tables(cursor) -> None:
    cursor.execute(
        """
        CREATE TABLE [Component](
            [Id] INTEGER NOT NULL PRIMARY KEY,
            [Name] [nvarchar](400) NOT NULL UNIQUE,
            [Description] [nvarchar](2000) NULL
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE [OS](
            [Id] INTEGER NOT NULL PRIMARY KEY,
            [Name] [nchar](10) NOT NULL UNIQUE
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE [Version](
            [Id] INTEGER NOT NULL PRIMARY KEY,
            [ComponentId] INTEGER NOT NULL,
            [OSId] INTEGER NOT NULL,
            [Version] [nvarchar](100) NOT NULL,
            UNIQUE([ComponentId], [OSId], [Version]),
            FOREIGN KEY ([ComponentId]) REFERENCES Component([Id]),
            FOREIGN KEY ([OSId]) REFERENCES OS([Id])
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE [Regression](
            [Id] INTEGER NOT NULL PRIMARY KEY,
            [ComponentId] INTEGER NOT NULL,
            [OSId] INTEGER NOT NULL,
            [Version] [nvarchar](100) NOT NULL,
            UNIQUE([ComponentId], [OSId], [Version]),
            FOREIGN KEY ([ComponentId]) REFERENCES Component([Id]),
            FOREIGN KEY ([OSId]) REFERENCES OS([Id])
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE [LatestVersion](
            [Id] INTEGER NOT NULL PRIMARY KEY,
            [ComponentId] INTEGER NOT NULL,
            [OSId] INTEGER NOT NULL,
            [Version] [nvarchar](100) NOT NULL,
            UNIQUE([ComponentId], [OSId], [Version]),
            FOREIGN KEY ([ComponentId]) REFERENCES Component([Id]),
            FOREIGN KEY ([OSId]) REFERENCES OS([Id])
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE [Compatibility](
            [ServiceId] INTEGER NOT NULL,
            [ConsumerId] INTEGER NOT NULL,
            UNIQUE([ServiceId], [ConsumerId]),
            CHECK ([ServiceId] < [ConsumerId])
        );
        """
    )


def fill_OSes(cursor) -> int:
    OSes = ['Windows', 'Linux', 'macOS']
    for os in OSes:
        cursor.execute("INSERT INTO  [OS] ([Name]) VALUES ('%s');" % os)
    return 0


def _component_version_bundle(bundle_name: str, compatibility_data: Dict) -> Dict:
    components = {}
    for _, row in compatibility_data[bundle_name].iterrows():
        if pandas.isnull(row["Version"]):
            components.update(_component_version_bundle(row["Name"], compatibility_data))
        else:
            components[row["Name"]] = row["Version"]
    return components


def fill_components_versions_compatibility(cursor, compatibility_data: Dict) -> int:
    if not compatibility_data:
        return 1

    for compatibility in compatibility_data.keys():
        os = compatibility.split(' ')[0]
        components = _component_version_bundle(compatibility, compatibility_data)
        for component_name, component_version in components.items():
            cursor.execute(
                """
                INSERT OR IGNORE INTO [Component] ([Name], [Description])
                VALUES ('%s', NULL);
                """ % component_name
            )
            cursor.execute(
                """
                INSERT OR IGNORE INTO [Version] ([Version], [ComponentID], [OSId])
                VALUES ('%s', (SELECT ID FROM Component where Name = '%s'),
                (SELECT ID FROM OS where Name = '%s'));
                """ % (component_version, component_name, os)
            )
        for component_name_1, component_version_1 in components.items():
            for component_name_2, component_version_2 in components.items():
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO [Compatibility] ([ServiceId], [ConsumerId])
                    VALUES
                    ((SELECT Version.Id FROM
                        Version inner join Component on Version.ComponentId = Component.ID
                        where Component.Name='%s' and Version.Version='%s'),
                    (SELECT Version.Id FROM
                        Version inner join Component on Version.ComponentId = Component.ID
                        where Component.Name='%s' and Version.Version='%s'));
                    """ % (component_name_1, component_version_1, component_name_2, component_version_2)
                )
    return 0


def fill_regression(cursor, regressions_data: Dict) -> int:
    if not regressions_data:
        return 1
    for regression, data in regressions_data.items():
        os = regression.split(' ')[0]
        for _, row in data.iterrows():
            cursor.execute(
                """
                INSERT OR IGNORE INTO [Regression] ([ComponentID], [OSId], [Version])
                VALUES ((SELECT ID FROM Component where Name = '%s'),
                (SELECT ID FROM OS where Name = '%s'), '%s');
                """ % (row["Name"], os, row["Version"])
            )
    return 0


def fill_latest_versions(cursor, latest_versions_data: Dict) -> int:
    if not latest_versions_data:
        return 1
    for latest_versions, data in latest_versions_data.items():
        os = latest_versions.split(' ')[0]
        for _, row in data.iterrows():
            cursor.execute(
                """
                INSERT OR IGNORE INTO [LatestVersion] ([ComponentID], [OSId], [Version])
                VALUES ((SELECT ID FROM Component where Name = '%s'),
                (SELECT ID FROM OS where Name = '%s'), '%s');
                """ % (row['Name'], os, row['Version'])
            )
    return 0


def fill_tables(cursor, spreadsheet: Path) -> None:
    excxel_data = read_excel(spreadsheet)
    if excxel_data is None:
        return
    result = 0
    result += fill_OSes(cursor)
    result += fill_components_versions_compatibility(
        cursor,
        {
            sheet_name: dataframe
            for sheet_name, dataframe in excxel_data.items()
            if "Bundle" in sheet_name
        }
    )
    result += fill_regression(
        cursor,
        {
            sheet_name: dataframe
            for sheet_name, dataframe in excxel_data.items()
            if "Regressions" in sheet_name
        }
    )
    result += fill_latest_versions(
        cursor,
        {
            sheet_name: dataframe
            for sheet_name, dataframe in excxel_data.items()
            if "Latest Versions" in sheet_name
        }
    )
    if result > 0:
        print("Some tables was not filled.")


def update_metadata(
        existing_metadata: Path,
        db_file: Path,
        db_name: str,
        version: str) -> None:

    with open(db_file, "rb") as database:
        db_hash = sha384(database.read()).hexdigest()

    curr_date = date.today().strftime("%Y%m%d")

    metadata_content = {}
    with open(existing_metadata, "r") as metadata:
        metadata_content = json.load(metadata)
    name, postfix = db_name.split(".", -1)
    metadata_content["databases"]["compatibility"][0]["name"] = f"{name}_{curr_date}.{postfix}"
    metadata_content["databases"]["compatibility"][0]["installation_name"] = db_name
    metadata_content["databases"]["compatibility"][0]["version"] = version
    metadata_content["databases"]["compatibility"][0]["date_of_creation"] = curr_date
    metadata_content["databases"]["compatibility"][0]["hash"] = db_hash

    with open(existing_metadata, "w") as metadata:
        json.dump(metadata_content, metadata, indent=4)


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    if not Path(args.spreadsheet).exists():
        print(f"{args.spreadsheet} doesn't exist.")
        exit(1)

    db_file = args.output / DB_NAME
    connection = create_db_conn(db_file)
    if connection is None:
        exit(1)

    cursor = connection.cursor()
    create_tables(cursor)
    fill_tables(cursor, args.spreadsheet)
    connection.commit()
    connection.close()
    update_metadata(args.metadata, db_file, DB_NAME, args.version)
