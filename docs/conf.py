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
release = '2023.2'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
# extensions = [
#   'sphinx_tabs.tabs'
# ]


nbsphinx_allow_errors = True

# for svg files handling for latex
nbsphinx_execute_arguments = [
    "--InlineBackend.figure_formats={'svg', 'pdf'}",
    "--InlineBackend.rc={'figure.dpi': 150}",
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

# html_theme = "sphinx_book_theme"
# html_theme_path = [
#    "_themes"
# ]

rst_prolog = r"""
.. |intel_r| replace:: Intel\ :superscript:`®`
.. |vtune_tm| replace:: VTune\ :superscript:`tm`
.. |tm| unicode:: U+2122 .. trademark
.. |opencl| replace:: OpenCL\ :superscript:`tm`
.. |onemkl| replace:: oneAPI Math Kernel Library (oneMKL)
.. |onednn| replace:: oneAPI Deep Neural Network Library (oneDNN)
.. |trade| replace:: :superscript:`TM`
""" + (
    r'.. |irisxe| replace:: Intel\ :superscript:`®`'
    r' Iris\ :superscript:`®` X\ :superscript:`e`'
)


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

ditaxml_make_flat = True
ditaxml_flat_map_to_title = False
ditaxml_shorten_alias = True

ditaxml_topic_meta = {}
ditaxml_topic_meta["audience"] = \
    "etm-aa2a8ffb0e5b41fe85bf2f5d50a71cf2"
ditaxml_topic_meta["description"] = "Identify problems with your toolkit installation."
ditaxml_topic_meta["document_title"] = "Diagnostics Utility for Intel® oneAPI Toolkits User Guide"
ditaxml_topic_meta["keywords"] = "None"
ditaxml_topic_meta["locale"] = "en-us"
ditaxml_topic_meta["menu"] = \
    "/content/data/globalelements/US/en/sub-navigation/idz/developer-sub-navigation-breadcrumb"
ditaxml_topic_meta["menu_parent"] = "/content/www/us/en/developer/tools/oneapi/toolkits"
ditaxml_topic_meta["primary_tags"] = (
    "etm-086ec8c4b4074875b84ba0e35d214cf5,"
    "etm-cf0ee1fba3374ceea048ddac3e923cab,"
    "etm-e9827d867eda46abb846aa3d8062b7f0,"
    "etm-e759606e77ad42549ba71c380d6d61e2,"
    "etm-bd7e6ab0b34d4e95901e82eaa67c07a8,"
    "etm-e9ad772b023840f09a3bb94d6251ea2c,"
    "etm-dba967177bfa477ca933d10533b04c38,"
    "etm-4c7a4593bba04ee2940ff6a1bc1bc95a,"
    "etm-c326ac0dddbc45cbb916bec3c0e56d03,"
    "etm-6b088d69d83243a0aa3b986645a7e74b"
)
ditaxml_topic_meta["content_type"] = "etm-6d0f0d9ff2b54ee4a65b84789754d34e"  # Install Guide
ditaxml_topic_meta["primary_owner"] = "Moore, Benjamin D (benjamin.d.moore@intel.com)"
ditaxml_topic_meta["primary_business_owner"] = "Feldhousen, Jeanette S (jeanette.s.feldhousen@intel.com)"
ditaxml_topic_meta["notification_dl"] = "benjamin.d.moore@intel.com,taryn.e.apel@intel.com,infodev.book.publishing.notices@intel.com"  # noqa: E501
ditaxml_topic_meta["program_identifier"] = "idz"
ditaxml_topic_meta["publish_date"] = "2023-07-10"
ditaxml_topic_meta["revision_date"] = "2023-07-13"
ditaxml_topic_meta["classification_type"] = "Public"
ditaxml_topic_meta["content_classification"] = "Public"
ditaxml_topic_meta["metadata_classification"] = "Public"
ditaxml_topic_meta["noindexfollowarchive"] = "false"
ditaxml_topic_meta["latest_version"] = "true"
ditaxml_topic_meta["group_content_id"] = "771725"  # 771725_771726 for 2023.0
ditaxml_topic_meta["publication_content_id"] = "781960"  # 771726 = 2023.0 773660 = 2023.1
ditaxml_topic_meta["publication_root_node"] = "oneapi"
ditaxml_topic_meta["publication_name"] = "user-guide-diagnostic-utility"
ditaxml_prod_info = {}
ditaxml_prod_info["prodname"] = ""
ditaxml_prod_info["version"] = "2023.2"

imgmath_image_format = "svg"

ditaxml_nocp_parameters = {
    "operation": "publish",
    "environment": "production",
    "ipix-path": "IPIX_Importtointelsite\\oneapi\\programming-guide",
    "dita-map": "C:\\git\\programming-guide\\_build\\ditaxml\\toc.ditamap",
    "publication-name": "Intel® oneAPI Programming Guide",
    "output-format": "NOCP staging",  # change to NOCP production to go live
    "conversion-out": "C:\\nocp-publish\\conversion-out\\programming-guide"
}

ditaxml_publish_to_nocp = True
ditaxml_blockquote_warning = True
