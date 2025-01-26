from playwright.sync_api import Page
from screenshot_on_failure import screenshot_on_failure

class Checkout():
    def __init__(self, page:Page, screenshot_dir):
        self.page = page
        self.screenshot_dir = screenshot_dir

        # Navigate to Cart page
        cart_button_locator = page.locator(".shopping_cart_link")
        cart_button_locator.click()

        # Click checkout button
        checkout_button_locator = page.locator("#checkout")
        checkout_button_locator.click()


    def checkout_step1_validation(self,first_name, last_name, zip_code, expecxted_checkout_step1_url):
        first_name_locator = "#first-name"
        last_name_locator = "#last-name"
        zip_code_locator = "#postal-code"


        # Perform checkout with given name and zip
        self.page.locator(first_name_locator).fill(first_name)
        self.page.locator(last_name_locator).fill(last_name)
        self.page.locator(zip_code_locator).fill(zip_code)
        
       # Verify checkout Step 1 URL
        if (self.page.url == expecxted_checkout_step1_url):
            return f"\033[92m Passed => Successfully completed checkout step 1\033[0m"
        else:
            filename = "Checkout_step_1_failure.png"
            screenshot_on_failure (self.page, self.screenshot_dir, filename)
            return f"\033[91m Failed => Failed to complete checkout step 1\033[0m"
        

    def checkout_step2_validation(self, sub_total, tax, total, expecxted_checkout_step2_url):
        # Click continue button
        continue_button_locator = self.page.locator("#continue")
        continue_button_locator.click()

        payment_lable_locator = self.page.locator("div[data-test='payment-info-label']")
        shipping_lable_locator = self.page.locator("div[data-test='shipping-info-label']")
        shipping_value_locator = self.page.locator("div[data-test='shipping-info-value']")
        total_lable_locator = self.page.locator("div[data-test='total-info-label']")
        subtotal_value_locator = self.page.locator(".summary_subtotal_label", has_text = sub_total)
        tax_value_locator = self.page.locator(".summary_tax_label", has_text = tax)
        total_value_locator = self.page.locator(".summary_total_label", has_text = total)

        # Verify checkout step 2 URL, page titles and price values
        if (
            self.page.url == expecxted_checkout_step2_url and 
            payment_lable_locator.text_content() == "Payment Information:" and
            shipping_lable_locator.text_content() == "Shipping Information:" and
            shipping_value_locator.text_content() == "Free Pony Express Delivery!" and
            total_lable_locator.text_content() == "Price Total" and
            subtotal_value_locator.count() == 1 and
            tax_value_locator.count() == 1 and
            total_value_locator.count() == 1
        ):
            return f"\033[92m Passed => Successfully completed checkout step 2\033[0m"
        else:
            filename = "Checkout_step_2_failure.png"
            screenshot_on_failure (self.page, self.screenshot_dir, filename)
            return f"\033[91m Failed => Failed to complete checkout step 2\033[0m"
    
    def checkout_complete_validation(self, expected_complete_title, expected_complete_msg, expected_complete_url):
        # Click on 'Finish' button
        finish_button_locator = self.page.locator("#finish")
        finish_button_locator.click()

        checkout_complete_title_locator = self.page.locator(".complete-header")
        checkout_complete_msg_locator = self.page.locator(".complete-text")

        # Verify checkout complete URL and success titke & message
        if (
            self.page.url == expected_complete_url and
            checkout_complete_title_locator.text_content() == expected_complete_title and
            checkout_complete_msg_locator.text_content() == expected_complete_msg
        ):
            return f"\033[92m Passed => Successfully completed checkout\033[0m"
        else:
            filename = "Checkout_complete_failure.png"
            screenshot_on_failure (self.page, self.screenshot_dir, filename)
            return f"\033[91m Failed => Failed to complete checkout\033[0m"
    
    def checkout_back_to_inventory(self, expecxted_inventory_page_url):
        # Navigate to the inventory page
        back_to_products_button_locator = self.page.locator("#back-to-products")
        back_to_products_button_locator.click()

        # Verify inventory page URL
        if (self.page.url == expecxted_inventory_page_url):
            return f"\033[92m Passed => Returned to the inventory page\033[0m"
        else:
            filename = "Checkout_back_to_inventory_failure.png"
            screenshot_on_failure (self.page, self.screenshot_dir, filename)
            return f"\033[91m Failed => Failed to return to the inventory page\033[0m"






