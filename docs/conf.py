# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
project = "AutoParser"
copyright = "2024, globaldothealth"
author = "globaldothealth"
# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.coverage",
    "sphinx.ext.graphviz",
    "sphinx_book_theme",
    "sphinxcontrib.mermaid",
    "myst_nb",
]
templates_path = [
    "_templates",
]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "venv",
    "README.md",
]
# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = "sphinx_book_theme"
html_logo = "images/logo.png"
html_title = "AutoParser"
html_static_path = ["_static"]

html_theme_options = {
    "repository_url": "https://github.com/globaldothealth/autoparser",
    "use_repository_button": True,
}
