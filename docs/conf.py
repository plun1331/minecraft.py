# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

# copy ../CHANGELOG.md to ./changelog.md
with open("../CHANGELOG.md", "r", encoding="utf-8") as file:
    with open("./changelog.md", "w", encoding="utf-8") as dest:
        dest.write(file.read())

sys.path.insert(0, os.path.abspath(".."))

project = "minecraft.py"
copyright = "2023-present plun1331"
author = "plun1331"
release = "0.0.0-alpha"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}


# -- Options for extensions ---------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "crypto": ("https://cryptography.io/en/latest/", None),
    "msal": ("https://msal-python.readthedocs.io/en/latest", None),
}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
