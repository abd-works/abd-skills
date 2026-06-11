"""
Playwright conftest for catalog kanban acceptance tests.
Provides a per-test Chromium page with a clean session.
"""

import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as pw:
        b = pw.chromium.launch(headless=True)
        yield b
        b.close()


@pytest.fixture()
def context(browser: Browser) -> BrowserContext:
    ctx = browser.new_context()
    yield ctx
    ctx.close()


@pytest.fixture()
def page(context: BrowserContext) -> Page:
    p = context.new_page()
    yield p
    p.close()
