"""Canonical GitHub, npx, and HTML-preview URLs for the Foundry catalog generator."""

GITHUB_ORG = "abd-works"
GITHUB_REPO = "abd-skills"
GITHUB_DEFAULT_BRANCH = "main"

GITHUB_REPO_URL = f"https://github.com/{GITHUB_ORG}/{GITHUB_REPO}"
GITHUB_BLOB_MAIN = f"{GITHUB_REPO_URL}/blob/{GITHUB_DEFAULT_BRANCH}/"
GITHUB_TREE_MAIN = f"{GITHUB_REPO_URL}/tree/{GITHUB_DEFAULT_BRANCH}/"
GITHUB_RAW_MAIN = (
    f"https://raw.githubusercontent.com/{GITHUB_ORG}/{GITHUB_REPO}/{GITHUB_DEFAULT_BRANCH}/"
)

HTMLPREVIEW_PREFIX = f"https://htmlpreview.github.io/?{GITHUB_BLOB_MAIN}"

# Open Agent Skills / skills.sh package slug (unchanged from skills index publish).
NPX_SKILLS_REPO_SLUG = "agilebydesign/agilebydesign-skills"

# Legacy repo slugs rewritten when syncing bootcamp slide links.
LEGACY_GITHUB_REPO_SLUGS = ("agilebydesign-skills", "abd-skill")
