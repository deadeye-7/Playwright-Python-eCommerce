from playwright.sync_api import Page
import time
from screenshot_on_failure import screenshot_on_failure

class Login:
    def __init__(self, page:Page, username, password, screenshot_dir):
        self.page = page
        self.screenshot_dir = screenshot_dir
        login_url = "https://www.saucedemo.com/"

        username_locator = page.locator("#user-name")
        password_locator = page.locator("#password")
        login_button_locator = page.locator("#login-button")

        # Navigate to the login page
        page.goto(login_url)

        # Perform login with given username and password
        username_locator.fill(username)
        password_locator.fill(password)
        login_button_locator.click()

class SuccessfulLogin(Login):
    def validation(self, expected_url,expected_inventory_count, expected_product_name):
        inventory_items_locator = self.page.locator(".inventory_list .inventory_item")
        product_image_locator = self.page.locator("#item_4_title_link .inventory_item_name")
        
        # Verify inventory page url, total inventory items & a given product name
        if (
            self.page.url == expected_url and    
            inventory_items_locator.count() == expected_inventory_count and
            product_image_locator.text_content() == expected_product_name
        ):
            return f"\033[92m Passed => Successful Login\033[0m"
        else:
            filename = "Successful login_failure.png"
            screenshot_on_failure (self.page, self.screenshot_dir, filename)
            return f"\033[91m Failed => Successful login: Login was successful but validation failed.\033[0m"

class UnsuccessfulLogin(Login):
    def validation(self):       
        expected_error_msg = "Epic sadface: Username and password do not match any user in this service"
        error_msg_locator = self.page.locator("h3[data-test='error']")
        
        # Verify the error message
        if (error_msg_locator.text_content() == expected_error_msg):
            return f"\033[92m Passed => Unsuccessful Login\033[0m"
        else:
            filename = "Successful login_failure.png"
            screenshot_on_failure (self.page, self.screenshot_dir, filename)
            return f"\033[91m Failed => Unsuccessful login: Didn't display the correct error message.\033[0m"
            
    
class LockedOut(Login):
    def validation(self):
        expected_error_msg = "Epic sadface: Sorry, this user has been locked out."
        error_msg_locator = self.page.locator("h3[data-test='error']")
        
        # Verify the error message
        if (error_msg_locator.text_content() == expected_error_msg):
            return f"\033[92m Passed => Locked out Login => Passed\033[0m"
        else:
            filename = "Lockedout login_failure.png"
            screenshot_on_failure (self.page, self.screenshot_dir, filename)
            return f"\033[91m Failed => Locked out Login: Didn't display the correct error message.\033[0m"
        

class ProblemLogin(Login):
    def validation(self):
        product_image_locator = self.page.locator("img[alt='Sauce Labs Backpack']")
        product_name_locator = self.page.locator("#item_4_title_link > .inventory_item_name") 
        product_description_locator = self.page.locator("body > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2)")
        product_price_locator = self.page.locator("body > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1)")
        add_to_cart_button_locator = self.page.locator("#add-to-cart-sauce-labs-backpack")

        # Get actual values from inventory page 
        product_image_url = product_image_locator.get_attribute("src")
        product_name = product_name_locator.text_content()  
        product_description = product_description_locator.text_content()
        product_price = product_price_locator.text_content()
        add_to_cart_button_text = add_to_cart_button_locator.text_content()

        # Navigate to the product details page
        product_locator = self.page.locator("#item_4_title_link > .inventory_item_name")
        product_locator.click()

        product_details_name_locator = self.page.locator(".inventory_details_name.large_size")
        product_details_image_locator = self.page.locator("img[alt='Sauce Labs Fleece Jacket']")
        product_details_desc_locator = self.page.locator(".inventory_details_desc.large_size")
        product_details_price_locator = self.page.locator(".inventory_details_price")
        product_details_cart_button_locator = self.page.locator("#add-to-cart")
        
        # Compare values between inventory page and product details page
        if (       
            product_details_name_locator.text_content() == product_name and
            product_details_image_locator.get_attribute("src") == product_image_url and
            product_details_desc_locator.text_content() == product_description and
            product_details_price_locator.text_content() == product_price and
            product_details_cart_button_locator.text_content() == add_to_cart_button_text
        ):
            return f"\033[92m Passed => Problem Login\033[0m"
        else:
            filename = "Problem login_failure.png"
            screenshot_on_failure (self.page, self.screenshot_dir, filename)
            return f"\033[91m Failed => Problem Login: Didn't display correct product data.\033[0m"
            
        
            
class PerformanceGlitchLogin(Login):
    def __init__(self, page:Page, username, password, screenshot_dir):
        # Start capturing time
        start_time = time.time()
        
        # Perform login from super class
        super().__init__(page, username, password, screenshot_dir)

        # End capturing time
        end_time = time.time()

        self.login_duration = end_time - start_time


    def validation(self, expected_url,expected_login_time):
        # Compare the actual login duration and url with actul
        if (
            self.login_duration < 1 and
            self.page.url == expected_url
        ):
            return f"\033[92m Passed => Performance glitch Login\033[0m"
        elif (self.login_duration > expected_login_time):
            return f"\033[91m Failed => Performance glitch Login: Login took longer than expected. Login time: {self.login_duration:.2f} sec\033[0m"
        else:
            filename = "Performance glitch login_failure.png"
            screenshot_on_failure (self.page, self.screenshot_dir, filename)
            return f"\033[91m Failed => Performance glitch Login: Login did not navigate to the expected URL.\033[0m"
        