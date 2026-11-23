project = "SpotipyFree"
author = "Tzur Soffer"
copyright = "2026, Tzur Soffer"
release = "1.9.15"

extensions = ["myst_parser", "sphinx_sitemap"]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
root_doc = "index"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_title = "SpotipyFree documentation"
html_baseurl = "https://spotipyfree.readthedocs.io/en/latest/"
sitemap_url_scheme = "{link}"
html_theme_options = {
    "navigation_depth": 4,
    "collapse_navigation": False,
}
html_context = {
    "display_github": True,
    "github_user": "TzurSoffer",
    "github_repo": "spotipyFree",
    "github_version": "main",
    "conf_py_path": "/docs/",
}
html_meta = {
    "description": (
        "Guides, installation instructions, API coverage, and safety notes for "
        "Installation, usage, API reference, and examples for the SpotipyFree Python library."
    ),
    "keywords": (
        "SpotipyFree, Python, Spotify, Spotipy, music metadata, Python library"
    ),
    "robots": "index,follow",
}
