from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self, url: str):
        self.page.goto(url)

        self.privacy_accept_button = self.page.locator("#onetrust-accept-btn-handler")
        self.privacy_accept_button.wait_for(timeout=5000)

        if self.privacy_accept_button.is_visible():
            self.privacy_accept_button.wait_for(state="visible")
            self.privacy_accept_button.click()