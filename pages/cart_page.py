class CartPage:
    def __init__(self, page):
        self.page = page
        self.item_name = page.locator(".e-productitem__name-label")
        self.remove_btn = page.locator(".c-button--link.e-productitem__remove")
        self.empty_msg = page.get_by_text("Ваш кошик порожній.")
    
    def remove_first_item(self):
        self.remove_btn.first.click()