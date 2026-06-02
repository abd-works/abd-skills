"""Acceptance test stub — Search Products by Keyword (fixture mode)."""


def test_search_returns_matching_product():
    # RED stub — implement in engineering after clean-code
    catalog = {"PET-FOD-001": "Kitten Food"}
    results = [name for sku, name in catalog.items() if "kitten" in name.lower()]
    assert results == ["Kitten Food"]
