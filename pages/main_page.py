import re
from .base_page import BasePage

class MainPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.input = page.locator(".ais-SearchBox-input")
        self.suggestion = page.locator(".algolia-searched-phrase")

        self.subcategory_item = page.locator(".subcategory-item")

        self.product_title = page.locator(".product-tiles_product-card_components_ProductTile_ProductDetails__title")

        self.filter_button = page.get_by_role("button", name=re.compile("Filters|Фільтри", re.IGNORECASE))
        self.filter_type_section = page.locator(".refinement.accordion-element.product_type.tag-commander-event")
        self.apply_filter_button = page.locator(".button.btn-dblue.js-apply-filters-algolia")
        self.first_product_card = page.locator(".product-tile.card:visible").first

        self.footer = page.locator("#footer")
        self.wishlist_icon = page.locator("#wishlist-status-icon")
    
    def search_for(self, text: str):
        self.input.press_sequentially(text, delay=1)
    
    def click_category(self, category_id: str, item_name: str):
        self.page.locator(f"#{category_id}").click()

        item = self.page.locator(".subcategory-item").get_by_text(item_name).filter(visible=True).first
        item.click()
    
    def open_filters(self):
        if self.filter_button.is_visible():
            self.filter_button.first.wait_for(state="visible")
            self.filter_button.first.click()

    def apply_dlc_filter(self):
        self.filter_type_section.click()

        dlc_filter = self.filter_type_section.get_by_text(re.compile("DLC")).filter(visible=True).first

        dlc_filter.wait_for(state="visible", timeout=10000)
        dlc_filter.click()
        self.apply_filter_button.click()

    def click_footer_link(self, text: str):
        self.footer.get_by_text(text).first.click()
    
    def click_first_product(self):
        self.product_title.first.click()
    
    def get_url(self):
        return self.page.url
