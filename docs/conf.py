"""Sphinx configuration for the Torn SDK documentation."""

from __future__ import annotations

import os
import sys
from datetime import date
from pathlib import Path
from tomllib import loads

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

sys.path.insert(0, str(SRC))

project = "Torn SDK"
author = "Rincorpes"
copyright = f"{date.today().year}, {author}"


def _docs_version() -> str:
    """Read the package version without importing the SDK."""
    if env_version := os.getenv("DOCS_VERSION"):
        return env_version

    project_data = loads((ROOT / "pyproject.toml").read_text("utf-8"))
    return project_data["project"]["version"]


release = _docs_version()
version = release

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_design",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

myst_enable_extensions = ["colon_fence", "deflist", "fieldlist"]

autosummary_generate = True
autodoc_member_order = "bysource"
autodoc_preserve_defaults = True
autodoc_typehints = "signature"
autodoc_default_options = {
    "members": True,
    "inherited-members": True,
    "show-inheritance": True,
}

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_param = True
napoleon_use_rtype = True

html_theme = "furo"
html_title = project

REPO_URL = "https://github.com/rincorpes/torn-sdk"
PYPI_URL = "https://pypi.org/project/torn-sdk/"

html_theme_options = {
    "source_repository": f"{REPO_URL}/",
    "source_branch": "main",
    "source_directory": "docs/",
    "navigation_with_keys": True,
    "top_of_page_buttons": ["view", "edit"],
    "light_css_variables": {
        "color-brand-primary": "#0F766E",
        "color-brand-content": "#0B7285",
        "color-background-primary": "#FAFCFD",
        "color-background-secondary": "#EEF4F7",
        "color-code-background": "#F4F8FA",
    },
    "dark_css_variables": {
        "color-brand-primary": "#4FD1C5",
        "color-brand-content": "#7DD3FC",
        "color-background-primary": "#0F1720",
        "color-background-secondary": "#17202A",
        "color-code-background": "#111B24",
    },
}
