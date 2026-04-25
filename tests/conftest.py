import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    """
    إنشاء متصفح للجلسة كاملة
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    """
    إنشاء صفحة جديدة لكل اختبار
    """
    context = browser.new_context()
    page = context.new_page()
    yield page
    page.close()
    context.close()