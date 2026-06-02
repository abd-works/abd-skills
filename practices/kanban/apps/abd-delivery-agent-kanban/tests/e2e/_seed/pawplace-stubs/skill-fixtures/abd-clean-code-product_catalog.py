"""Product catalog search — clean-code stub (fixture mode)."""


def search_products(catalog, keyword: str) -> list:
    if not keyword:
        return []
    needle = keyword.lower()
    return [p for p in catalog if needle in p["name"].lower()]
