class ProductPage:
    def __init__(self, page):
        self.page = page
        self.title = page.locator(".c-pdp-banner__product-name")
        self.dlc_badge = page.locator(".c-pdp-banner__dlc")
        self.get_the_game_btn = page.locator(".button.btn-connect-blue.get-the-game")
        self.add_to_cart_btn = page.get_by_role("button", name="Add to cart")
        self.add_to_wishlist_btn = page.locator(".tooltip-trigger.pdp-add-to-wishlist.button.add-to-wishlist.inverse.button-with-svg")
    def get_product_name(self):
        return self.title.first.inner_text().strip()

    def add_to_cart(self):
        self.get_the_game_btn.filter(visible=True).first.click()
        self.add_to_cart_btn.wait_for(state="visible", timeout = 10000)
        self.add_to_cart_btn.click()