from playwright.sync_api import Page

class Logout:
    def __init__(self, page:Page):
        self.page = page
        self.login_url = "https://www.saucedemo.com/"

        menu_icon_locator = page.locator("#react-burger-menu-btn")
        menu_panel_locator = ".bm-item-list"
        logout_menu_locator = page.locator("#logout_sidebar_link")

        # Perform log out
        menu_icon_locator.click()
        page.wait_for_selector(menu_panel_locator,timeout=5000)
        logout_menu_locator.click()

    def validation(self):
        # Verify the login url after logout
        if (self.page.url == self.login_url):
            return f"\033[92m Passed => Successfully Logout\033[0m"
        else:
            return f"\033[91m Failed => Successful Logout: Logout failed.\033[0m"

