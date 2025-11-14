# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'modusa'
copyright = '2025, Ankit Anand'
author = 'Ankit Anand'

from modusa import __version__
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
	"nbsphinx",
	"sphinx.ext.mathjax",
	'sphinx.ext.autodoc',
	'sphinx.ext.napoleon',
	'sphinx.ext.viewcode',
	'sphinx_copybutton',
	'sphinx.ext.inheritance_diagram'
]

nbsphinx_execute = 'never' # Do not execute the notebooks

autodoc_default_options = {
	"members": True,
	"undoc-members": False,
	"private-members": False,
	"show-inheritance": True
}

autodoc_member_order = 'bysource'

napoleon_google_docstring = True
napoleon_numpy_docstring = True

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_logo = "_static/icon.png"
html_css_files = ['custom.css']

html_theme_options = {
	"navigation_with_keys": True,  # optional: enables left/right arrows
	"sidebar_hide_name": False,    # optional: shows project name
}
html_static_path = ['_static']
