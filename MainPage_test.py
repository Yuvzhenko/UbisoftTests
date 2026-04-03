import re
import pytest
from playwright.sync_api import sync_playwright, expect

def open_page(page, link):
    page.goto(link)

    privacy_accept_button = page.locator("#onetrust-accept-btn-handler")
    privacy_accept_button.wait_for(timeout=5000)

    if privacy_accept_button.is_visible():
        privacy_accept_button.wait_for(state="visible")
        privacy_accept_button.click()

def test_main_page_search():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        open_page(page, "https://store.ubisoft.com")

        page.locator(".ais-SearchBox-input").press_sequentially("Assassin's Creed", delay=1)

        expect(page.locator(".algolia-searched-phrase").first).to_contain_text("Assassin's Creed", timeout=10000)

        browser.close()

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
    ("menu-spring-sale","Best Sellers","deals-best-sellers"),
    ("menu-spring-sale","Great Price","deals-great-prices"),
    ("menu-spring-sale","DLC Deals","deals-dlc"),
    ("menu-spring-sale","Assassin's Creed Shadows","assassins-creed-shadows"),
    ("menu-spring-sale","Assassin's Creed Mirage","assassin-s-creed-mirage"),
    ("menu-spring-sale","Assassin's Creed Valhalla","assassins-creed--valhalla"),
    ("menu-spring-sale","Anno 117: Pax Romana","anno-117--pax-romana"),
    ("menu-spring-sale","Avatar: Frontiers of Pandora","avatar--frontiers-of-pandora"),
    ("menu-spring-sale","The Division 2","tom-clancys-the-division-2"),
    ("menu-ubisoft-plus-main-nav","Overview","ubisoftplus"),
    ("menu-ubisoft-plus-main-nav","Games","ubisoftplus/games"),
    ("menu-ubisoft-plus-main-nav","Premium","ubisoftplus/premium"),
    ("menu-ubisoft-plus-main-nav","Classics","ubisoftplus/classics")
]

@pytest.mark.parametrize("category, item_name, expected_url", menu_items)
def test_main_page_categories(category, item_name, expected_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = True)
        page = browser.new_page()

        open_page(page, "https://store.ubisoft.com")

        page.locator(f"#{category}").click()

        page.locator(".subcategory-item").get_by_text(item_name).filter(visible=True).first
        page.locator(".subcategory-item").get_by_text(item_name).filter(visible=True).first.click()

        expect(page).to_have_url(re.compile(f".*{expected_url}"), timeout=10000)

        browser.close()

