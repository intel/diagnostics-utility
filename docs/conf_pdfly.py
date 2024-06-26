# -*- coding: utf-8 -*-
#
# Customized Sphinx build configuration file for pdfly.
# maintainer: michael.vincerra@intel.com
# This file requires the pdfly app for successful builds.

# This configuration file requires several packages to be installed.
# Validated on Ubuntu 18.04 Desktop, Windows Subsystem for Linux v1.
# File assumes the installation of several macros from LaTeX.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import datetime
import os
import sys

# Added for hybrid
import docutils

sys.path.append(os.path.abspath("./_ext"))

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# sys.path.insert(0, os.path.abspath('.'))

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx_sitemap',
    # 'sphinxcontrib.spelling', #unused for pdf generation
    # 'sphinx2dita', #unused for pdf generation
]

# Following option unused for pdf generation.
# if 'SPHINX2DITA' in os.environ:
#         extensions.append("sphinx2dita")]

spelling_lang = 'en_US'

tokenizer_lang = 'en_US'


latex_engine = 'xelatex'

f = open('_latex_temp/preamble.tex', 'r+')
PREAMBLE = f.read()

latex_elements = {
    # Solves babel failure error
    'babel': '\\usepackage[english]{babel}',
    # Removes empty pages inserted
    'classoptions': '',
    # Alternative: 'classoptions': 'openany, oneside',
    # Previously set to: ',oneside',
    # 'extraclassoptions': 'openany',
    'papersize': 'letterpaper',
    'fncychap': '',
    'figure_align': 'H',
    # The font size should be one of these ('10pt', '11pt' or '12pt').
    'pointsize': '11pt',
    'fontpkg': r'''
\usepackage{fontspec}
\usepackage{xunicode}
\usepackage{xcolor}

% Classic Blue | Intel new logo: classic-blue-fullcolor
\definecolor{IntelClassicBlue}{HTML}{0068B5}

% Classic Blue Tint 1
\definecolor{IntelClassicBlue-T1}{HTML}{00A3F6}

% Classic Blue Tint 2
\definecolor{IntelClassicBlue-T2}{HTML}{76CEFF}

% Classic Blue Shade 1
\definecolor{IntelClassicBlue-S1}{HTML}{004A86}

% Classic Blue Shade 2
\definecolor{IntelClassicBlue-S2}{HTML}{00285A}

\definecolor{darkcyan}{HTML}{0071C5}
            \usepackage{anyfontsize}

%% intelone-display-light -- additional option unused

\setmainfont{intelone-display-regular.ttf}[
    BoldFont       = intelone-display-bold.ttf,
    ItalicFont      = intelone-display-medium.ttf,
    BoldItalicFont  = intelone-display-medium.ttf
   ]

\setmonofont[Scale=MatchLowercase,Path=/usr/share/fonts/truetype/dejavu/]{DejaVuSansMono.ttf}

%\setsansfont{Courier}
''',
    'preamble': PREAMBLE,
    'maketitle': r'''

\pagestyle{empty}

\begin{titlepage}
\textcolor{IntelClassicBlue-S1}{\rule{\textwidth}{.8pt}}

 %\sphinxlogo
 \begin{flushright}
 \sphinxlogo

  \vspace*{50mm}

  \begingroup

  {\color{IntelClassicBlue}{\fontsize{48}{50}\selectfont\bfseries\itshape\thetitle}}

  {\color{IntelClassicBlue-S1}{\fontsize{24}{28}\selectfont\mdseries\upshape\theauthor}}

  \vspace*{50mm}
  {\color{IntelClassicBlue-S1}{\fontsize{14}{16}\selectfont\mdseries\upshape\thedate}}

    \makeatletter
    \ThisCenterWallPaper{1.0}{azzurri-rect3.png}
    \makeatother

    % alternate
    %\begin{center}
      %\includegraphics[width=\textwidth]{azzurri-rect3.png}
    %\end{center}


  \vspace*{3mm}

  \makeatletter
  {\color{IntelClassicBlue-S1}{\fontsize{14}{16}\selectfont\mdseries\upshape\py@release\releaseinfo}}
  \makeatother

  \endgroup

\end{flushright}

\end{titlepage}


\cleardoublepage
\cleardoublepage

''',
    'inputenc': '',
    'fontenc': '',
    'sphinxsetup': 'hmargin={0.7in,0.7in}, vmargin={1in,1in},\
verbatimwithframe=true,\
verbatimwrapslines=true,\
TitleColor={HTML}{003C71},\
HeaderFamily=\\rmfamily\\bfseries, \
InnerLinkColor={rgb}{0.208,0.374,0.486},\
OuterLinkColor={rgb}{0.216,0.439,0.388},\
VerbatimColor={HTML}{F0F0F0},\
VerbatimHighlightColor={HTML}{76CEFF},\
VerbatimBorderColor={HTML}{00285A}',
}

latex_toplevel_sectioning = 'chapter'

# latex_additional_files = ["mystyle.sty"]

html_logo = 'images/logo-classicblue-400px.png'

# latex_elements = { 'letterpaper' }

latex_paper_size = 'letterpaper'

# alt: 'a4paper'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# Set depth of Figures; Set to 0 to use simple numbers, without decimals
numfig_secnum_depth = 0


# General information about the project.

# Added for hybrid

project = "Diagnostics Utility for oneAPI User Guide"
copyright = "2021, Intel"
author = "Intel"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
# version = '0.1'
# The full version, including alpha/beta/rc tags.
# release = '0.1'

# Removed release per discussion with rscohn1 on 01-22-2021
# release = u'Beta'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
# today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = [
    "_build",
    "_themes",
    "root/*.rst",
    "*.inc.rst",
    "**/*.inc.rst",
]

# The reST default role (used for this markup: `text`) to use for all
# documents.
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
# add_module_names = True

text_sectionchars = '*=-^'

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False


# If true, `todo` and `todoList` produce output, else they produce nothing.

# Add for hybrid
todo_include_todos = True

# Add for hybrid

rst_prolog = r"""
.. |intel_r| replace:: Intel\ :superscript:`®`
.. |vtune_tm| replace:: VTune\ :supsub:`tm`
.. |tm| unicode:: U+2122 .. trademark
.. |opencl| replace:: OpenCL\ :supsub:`tm`
.. |onemkl| replace:: oneAPI Math Kernel Library (oneMKL)
.. |onednn| replace:: oneAPI Deep Neural Network Library (oneDNN)
""" + (
    r'.. |irisxe| replace:: Intel\ :superscript:`®`'
    r' Iris\ :superscript:`®` X\ :superscript:`e`'
)

primary_domain = "cpp"

# -- Options for spelling extension-------------------------------------------
spelling_warning = True

# rst_epilog = """
# .. include:: /substitutions.txt
# """

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
# html_theme = 'sphinx_rtd_theme'

# ALT: 'alabaster'

# Added for hybrid

html_theme = 'sphinx_book_theme'

# otc_tcs_sphinx_theme
version = current_version = "latest"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.

# Replace value of 'canonical_url' below with actual location of doc website.
# TODO: Write user-setup section to customize dictionary output below.

html_theme_options = {
    'canonical_url': '',
    'style_nav_header_background': '#007ab2',
    'navigation_depth': 3,
    'display_version': False,
    'collapse_navigation': False,
    'prev_next_buttons_location': 'None',
    'sticky_navigation': True,
}

# TODO: Add option for html_context in user-setup
html_context = {
    'author': 'Intel Business Unit',
    'date': datetime.date.today().strftime('%d/%m/%y'),
    # Replace  key/values below with custom info.
    # "display_github": True, # Integrate GitHub
    # "github_user": "", # Username
    # "github_repo": "", # Repo name
    # "github_version": "master", # Version
    # "conf_py_path": "/source/", # Path in the checkout to the docs root
    # "current_version": current_version,
}

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = ['_themes']

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".

html_title = "Diagnostics Utility for oneAPI User Guide"
html_favicon = "_static/favicon.png"
html_logo = '_static/oneAPI-rgb-rev-100.png'

# html_logo. images/logo-energyblue-white-72px-MED.png.
# Used for multi-target testing and validation for pdfly only.

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".

# Added for hybrid
html_static_path = ['_static']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
# html_extra_path = ['_html_extra']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants =

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
html_domain_indices = False

# If false, no index is generated.
html_use_index = True

# If true, the index is split into individual pages for each letter.
html_split_index = True

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink =

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
# html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
#   'da', 'de', 'en', 'es', 'fi', 'fr', 'hu', 'it', 'ja'
#   'nl', 'no', 'pt', 'ro', 'ru', 'sv', 'tr'
# html_search_language = 'en'

# A dictionary with options for the search language support, empty by default.
# Now only 'ja' uses this config value
# html_search_options = {'type': 'default'}

# The name of a javascript file (relative to the configuration directory) that
# implements a search results scorer. If empty, the default will be used.
# html_search_scorer = 'scorer.js'

# Output file base name for HTML help builder.

# TODO: Add option for html_context in user-setup
# htmlhelp_basename = ''

# -- Options for LaTeX output ---------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
# Replace Document Revision, below, to match release date; hard coded value.


# Removed below: u'Deep learning optimized for Intel® architecture'.
# Third item is generally the document subtitle; optional.


latex_documents = [
    (
        master_doc,
        'get_started.tex',
        u'Diagnostics Utility for oneAPI User Guide',
        u'',
        'manual',
    ),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
latex_logo = 'images/logo-classicblue-400px.png'

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# If true, show page references after internal links.
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
# latex_show_urls = False

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, '', [author], 1)]

# If true, show URL addresses after external links.
# man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        'index',
        u'Diagnostics Utility for oneAPI User Guide',
        author,
        'Intel® Software',
        'Diagnostics Utility for oneAPI User Guide.',
        'Miscellaneous',
    ),
]

# Documents to append as an appendix to all manuals.
# texinfo_appendices = []

# If false, no module index is generated.
# texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
# texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
# texinfo_no_detailmenu = False

# If true, generates permalinks on the HTML output.
# html_add_permalinks = ""

# suppresses warnings for options that aren't referenced
# suppress_warnings = ["ref.option"]

numfig = True

# -- Options for Localization using sphinx-intl ---------------------------

gettext_compact = False  # optional.


# -- Add some directives for structure------------------------------------


def supsub_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    node = docutils.nodes.superscript()
    node2 = docutils.nodes.substitution_reference(refname=text)
    node += [node2]
    return [node], []


def setup(app):
    app.add_role('supsub', supsub_role)
    add_custom_css = getattr(
        app, "add_css_file", getattr(app, "add_stylesheet")
    )
    add_custom_css("custom.css")
    return {"version": "0.1"}


ditaxml_make_flat = True
ditaxml_flat_map_to_title = True
ditaxml_default_codeblock_type = 'c'

ditaxml_topic_meta = {}
ditaxml_topic_meta["audience"] = (
    "emtaudience:business/btssbusinesstechnologysolutionspecialist/"
    "softwaredeveloper"
)
ditaxml_topic_meta["content type"] = "Developer Guide"
ditaxml_topic_meta[
    "description"
] = "Diagnose installation errors."
ditaxml_topic_meta["document title"] = "Diagnostics Utility for oneAPI User Guide"
ditaxml_topic_meta["IDZ custom tags"] = "idzcustomtags:productdocumentation"
ditaxml_topic_meta["keywords"] = "None"
ditaxml_topic_meta["language"] = "en"
ditaxml_topic_meta["location"] = "us"
ditaxml_topic_meta["menu"] = "/us/en/develop/documentation"
ditaxml_topic_meta[
    "operating system"
] = "emtoperatingsystem:linux&#x0002C;emtoperatingsystem:macos"
ditaxml_topic_meta[
    "programming language"
] = "emtprogramminglanguage:cc/dataparallelcdpc"
ditaxml_topic_meta["software"] = (
    "rsoftware:componentsproducts/intelccompiler&#x0002C;"
    "rsoftware:inteloneapitoolkits/inteloneapibasetoolkit"
)
ditaxml_topic_meta[
    "primaryOwner"
] = "Moore, Benjamin D (benjamin.d.moore@intel.com))"
ditaxml_topic_meta["programidentifier"] = "idz"
ditaxml_topic_meta["published date"] = "08/26/2021"
ditaxml_topic_meta["resourcetypeTag"] = "emtcontenttype:document"
ditaxml_topic_meta[
    "secondary contenttype"
] = "emtcontenttype:document/guide/developerguide"
ditaxml_topic_meta["security classification"] = "Public Content"
ditaxml_topic_meta[
    "shortDescription"
] = "Maximize your hardware’s ability to execute the code."
ditaxml_topic_meta["shortTitle"] = "Diagnostics Utility for oneAPI User Guide"
ditaxml_topic_meta["entitlement"] = "intel_usr"
ditaxml_topic_meta["entitlementtype"] = "any"
ditaxml_topic_meta["noindexfollowarchive"] = "true"
ditaxml_prod_info = {}
ditaxml_prod_info["prodname"] = ""
ditaxml_prod_info["version"] = "2021.1"
ditaxml_data_about = {}
ditaxml_data_about["intelswd_aliasprefix"] = {
    "datatype": "webAttr",
    "value": "diagnostics-utility-user-guide",
}

imgmath_image_format = "svg"
