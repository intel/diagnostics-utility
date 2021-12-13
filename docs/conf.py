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

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'Diagnostics Utility for Intel® oneAPI Toolkits User Guide'
copyright = 'Intel Corporation'

# The full version, including alpha/beta/rc tags
release = '2022.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx_tabs.tabs'
]

# Add any paths that contain templates here, relative to this directory.
# templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

html_theme = "sphinx_book_theme"
# html_theme_path = [
#    "_themes"
# ]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

ditaxml_make_flat = True
ditaxml_flat_map_to_title = False
ditaxml_shorten_alias = True

ditaxml_topic_meta = {}
ditaxml_topic_meta["audience"] = \
    "guid:etm-aa2a8ffb0e5b41fe85bf2f5d50a71cf2"
ditaxml_topic_meta["content type"] = "User Guide"
ditaxml_topic_meta["description"] = "Identify problems with your toolkit installation."
ditaxml_topic_meta["document title"] = "Diagnostics Utility for Intel® oneAPI Toolkits User Guide"
ditaxml_topic_meta["download url"] = ""
ditaxml_topic_meta["IDZ custom tags"] = "guid:etm-086ec8c4b4074875b84ba0e35d214cf5"
ditaxml_topic_meta["keywords"] = "None"
ditaxml_topic_meta["language"] = "en"
ditaxml_topic_meta["location"] = "us"
ditaxml_topic_meta["menu"] = \
    "/content/data/globalelements/US/en/sub-navigation/idz/developer-sub-navigation-breadcrumb"
ditaxml_topic_meta["menu parent page"] = "/content/www/us/en/developer/tools/oneapi/toolkits"
ditaxml_topic_meta["operating system"] = \
    "guid:etm-cf0ee1fba3374ceea048ddac3e923cab,guid:etm-e9827d867eda46abb846aa3d8062b7f0"
ditaxml_topic_meta["programming language"] = "guid:etm-e759606e77ad42549ba71c380d6d61e2"
ditaxml_topic_meta["software"] = \
    "guid:etm-dba967177bfa477ca933d10533b04c38,guid:etm-4c7a4593bba04ee2940ff6a1bc1bc95a"
ditaxml_topic_meta["primaryOwner"] = "Moore, Benjamin D (benjamin.d.moore@intel.com)"
ditaxml_topic_meta["programidentifier"] = "idz"
ditaxml_topic_meta["published date"] = "12/07/2021"
ditaxml_topic_meta["resourcetypeTag"] = "guid:etm-6d0f0d9ff2b54ee4a65b84789754d34e"
ditaxml_topic_meta["secondary contenttype"] = \
    "emtcontenttype:document/guide/developerguide/developergettingstartedguide"
ditaxml_topic_meta["security classification"] = "Public Content"
ditaxml_topic_meta["shortDescription"] = "Identify problems with your toolkit installation."
ditaxml_topic_meta["shortTitle"] = "Diagnostics Utility for Intel® oneAPI Toolkits User Guide"
ditaxml_topic_meta["entitlement"] = "intel_usr,iot_tcc"
ditaxml_topic_meta["entitlementtype"] = "any"
ditaxml_topic_meta["noindexfollowarchive"] = "false"
ditaxml_topic_meta["technology"] = "guid:etm-6b088d69d83243a0aa3b986645a7e74b"
ditaxml_prod_info = {}
ditaxml_prod_info["prodname"] = ""
ditaxml_prod_info["version"] = "2022.0"
ditaxml_data_about = {}
ditaxml_data_about["intelswd_aliasprefix"] = {
    "datatype": "webAttr", "value": "get-started-with-intel-time-coordinated-computing-tools-0-11"}
