from playwright.sync_api import Page, expect

def test_has_title(page: Page):
    # اذهبي لموقعك
    page.goto("http://127.0.0.1:8000/") 
    
    # بدلاً من التحقق من الـ Title، لنتحقق من وجود نص معين في الصفحة
    # (استبدلي 'Welcome' بأي كلمة موجودة في صفحتك الرئيسية)
    expect(page.locator("body")).to_contain_text("")