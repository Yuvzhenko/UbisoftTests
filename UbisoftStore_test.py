import re
import pytest
from playwright.sync_api import sync_playwright, expect
from pages.cart_page import CartPage
from pages.main_page import MainPage
from pages.product_page import ProductPage

URL = "https://store.ubisoft.com"

def open_page(page, link):
    page.goto(link)

    privacy_accept_button = page.locator("#onetrust-accept-btn-handler")
    privacy_accept_button.wait_for(timeout=5000)
    if privacy_accept_button.is_visible():
        privacy_accept_button.wait_for(state="visible")
        privacy_accept_button.click()

def test_main_page_search(page):
    main = MainPage(page)
    main.open(URL)

    main.search_for("Assassin's Creed")

    expect(main.suggestion.first).to_contain_text("Assassin's Creed", timeout=10000)

menu_items = [
    ("menu-games","Бестселери","category-best-sellers"),
    ("menu-games","Безкоштовні ігри","free-pc-games"),
    ("menu-games","Новинки","category-latest-releases"),
    ("menu-games","Класичні хіти","category-classics"),
    ("menu-games","Rainbow Six Siege","tom-clancy-s-rainbow-six"),
    ("menu-games","Assassin's Creed Shadows","assassins-creed-shadows"),
    ("menu-games","Avatar: Frontiers of Pandora","avatar--frontiers-of-pandora"),
    ("menu-games","Assassin's Creed Mirage","assassin-s-creed-mirage"),
    ("menu-games","Assassin's Creed Valhalla","assassins-creed--valhalla"),
    ("menu-games","Anno 117: Pax Romana","anno-117--pax-romana"),
    ("menu-games","The Division 2","tom-clancys-the-division-2"),
    ("menu-games","The Crew Motorfest","the-crew-motorfest"),
    ("menu-games","Star Wars Outlaws","star-wars-outlaws"),
    ("menu-games","Skull & Bones","skull-and-bones"),
    ("menu-games","Anno 1800","anno-1800"),
    ("menu-games","Rocksmith+","rocksmithplus"),
    ("menu-dlc","For Honor","dlc-brands-for-honor"),
    ("menu-dlc","Far Cry 6","dlc-brands-far-cry-6"),
    ("menu-dlc","Rainbow Six Siege","dlc-brands-six-siege"),
    ("menu-dlc","Assassin's Creed Shadows","dlc-brands-assassin-creed-shadows"),
    ("menu-dlc","Avatar Frontiers of Pandora","dlc-brands-avatar-frontiers-of-pandora"),
    ("menu-dlc","Assassin's Creed Mirage","dlc-brands-assassin-creed-mirage"),
    ("menu-dlc","Assassin's Creed Valhalla","dlc-brands-assassin-creed-valhalla"),
    ("menu-dlc","Anno 117: Pax Romana","dlc-brands-anno-117"),
    ("menu-dlc","The Division 2","dlc-brands-the-division-2"),
    ("menu-dlc","The Crew Motorfest","dlc-brands-the-crew-motorfest"),
    ("menu-dlc","Star Wars Outlaws","dlc-brands-star-wars-outlaws"),
    ("menu-dlc","Skull & Bones","dlc-brands-skull-and-bones"),
    ("menu-dlc","Anno 1800","dlc-brands-anno-1800"),
    ("menu-dlc","Валюта","dlc-type-currency"),
    ("menu-dlc","Сезонна перепустка","dlc-type-season-pass"),
    ("menu-dlc","Доповнення","dlc-type-extensions"),
    ("menu-dlc","набори","dlc-type-packs"),
    ("menu-dlc","Скіни та косметичні засоби","dlc-type-skins-cosmetics"),
    ("menu-ubisoft-plus-main-nav","Overview","ubisoftplus"),
    ("menu-ubisoft-plus-main-nav","Games","ubisoftplus/games"),
    ("menu-ubisoft-plus-main-nav","Premium","ubisoftplus/premium"),
    ("menu-ubisoft-plus-main-nav","Classics","ubisoftplus/classics")
]

@pytest.mark.parametrize("category, item_name, expected_url", menu_items)
def test_main_page_categories(page, category, item_name, expected_url):
    main = MainPage(page)
    main.open(URL)

    main.click_category(category, item_name)

    expect(page).to_have_url(re.compile(f".*{expected_url}"), timeout=10000)

def test_add_to_cart(page):
    main = MainPage(page)
    product = ProductPage(page)
    cart = CartPage(page)
    main.open(URL)

    expected_name = main.product_title.first.inner_text().strip()

    main.click_first_product()
        
    product.add_to_cart()

    expect(cart.item_name.first).to_contain_text(expected_name, timeout=10000)

def test_delete_from_cart(page):
    main = MainPage(page)
    product = ProductPage(page)
    cart = CartPage(page)
    main.open(URL)

    main.click_first_product()

    product.add_to_cart()

    cart.remove_first_item()

    expect(cart.empty_msg).to_be_visible(timeout=10000)

def test_search_filter(page):
    main = MainPage(page)
    product = ProductPage(page)
    main.open(URL)

    main.search_for("Assassin's Creed")

    main.filter_button.wait_for(timeout=5000)

    main.open_filters()

    main.apply_dlc_filter()

    main.first_product_card.wait_for(state="visible", timeout=15000)
    main.first_product_card.click()

    expect(product.dlc_badge).to_be_visible(timeout=5000)

footer_current_page_items = [
    ("Exclusive benefits", "ubisoft-store-benefits"),
    ("Rewards", "rewards"),
    ("About Ubisoft", "ubisoft.com"),
    ("Careers", "company/careers/working-at-ubisoft"),
    ("Creator Program", "creatorsprogram"),
    ("Games", "games"),
    ("Additional Content", "dlc"),
    ("Deals", "deals"),
    ("Ubisoft+", "ubisoftplus"),
    ("Rocksmith+", "rocksmithplus"),
    ("Ubisoft Connect PC launcher", "ubisoft-connect"),
    ("Support", "purchases-and-rewards")
]

@pytest.mark.parametrize("text, expected_url", footer_current_page_items)
def test_footer_current_page(page, text, expected_url):
    main = MainPage(page)
    main.open(URL)
        
    main.click_footer_link(text)

    expect(page).to_have_url(re.compile(expected_url))

footer_new_page_items = [
    ("Simplified refund", "refund-policy"),
    ("Ubisoft Gear Shop", "ubisoftgearshop")
]

@pytest.mark.parametrize("text, expected_url", footer_new_page_items)
def test_footer_new_page(page, text, expected_url):
    main = MainPage(page)

    main.open(URL)

    with page.context.expect_event("page") as new_page_info:
        main.click_footer_link(text)
        
    new_page = new_page_info.value

    expect(new_page).to_have_url(re.compile(expected_url))