# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys


sys.path.insert(0, os.path.abspath('..'))

project = 'minecraft.py'
copyright = '2023-present plun1331'
author = 'plun1331'
release = '0.0.0a1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for extensions ---------------------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None), 
    'crypto': ('https://cryptography.io/en/latest/', None),
    'msal': ('https://msal-python.readthedocs.io/en/latest', None),
}



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
