from playwright.sync_api import Page

class Cart:
    def __init__(self, page:Page, product_name):
        self.page = page
        self.product_name = product_name

        # Get the locators for the product and cart badge
        self.product_locator = self.page.get_by_text(product_name,exact=True) 
        self.cart_badge_locator = self.page.locator(".shopping_cart_badge")
        
        # Initialize product added count
        if self.cart_badge_locator.count() > 0:
            self.added_product = int(self.cart_badge_locator.text_content())
        else:
            self.added_product = 0


class AddProduct(Cart):
    def inventory_page_validation(self):
        add_button_locator = self.product_locator.locator("..").locator("..").locator("..").locator(".btn_inventory")
        remove_button_locator = self.product_locator.locator("..").locator("..").locator("..").locator(".btn_secondary")

        # Add product to cart
        add_button_locator.click()

        # Verify cart button text update and product count increment
        if (
            remove_button_locator.text_content() == "Remove" and
            int(self.cart_badge_locator.text_content()) == self.added_product+1
        ):
            return f"\033[92m Passed => '{self.product_name}' successfully added to the cart from the inventory page.\033[0m"
        else:
            return f"\033[91m Failed => Failed to add '{self.product_name}' to the cart from the inventory page.\033[0m"


    def cart_page_validation(self):       
        inventory_product_description_locator = self.product_locator.locator("..").locator("..").locator(".inventory_item_desc")
        inventory_product_price_locator = self.product_locator.locator("..").locator("..").locator("..").locator(".inventory_item_price")

        # Save product description and price for the inventory page
        self.inventory_product_description = inventory_product_description_locator.text_content()
        self.inventory_product_price = inventory_product_price_locator.text_content()

        # Navigate to the cart page
        cart_button_locator = self.page.locator(".shopping_cart_link")
        cart_button_locator.click()

        cart_product_description_locator = self.product_locator.locator("..").locator("..").locator(".inventory_item_desc")
        cart_product_price_locator = self.product_locator.locator("..").locator("..").locator(".inventory_item_price")

        # Compare product description & price between inventory & cart pages
        if (
            cart_product_description_locator.text_content() == self.inventory_product_description and
            cart_product_price_locator.text_content() == self.inventory_product_price
        ):
            return f"\033[92m Passed => '{self.product_name}' successfully added to the cart page.\033[0m"
        else:
            return f"\033[91m Failed => Failed to add '{self.product_name}' to the cart page.\033[0m"
    
    def productdetails_page_validation(self):
        # Navigate to the product details page
        self.product_locator.click()

        remove_button_locator = self.page.locator("#remove")

         # Verify the appearance of 'Remove' button       
        if (remove_button_locator.count() == 1):
            return f"\033[92m Passed => '{self.product_name}' successfully added to the product details page.\033[0m"
        else:
            return f"\033[91m Failed => Failed to add '{self.product_name}' to the product details page.\033[0m"

class RemoveProduct(Cart):
    def remove_product_from_inventory_page(self):
        # Abort due to empty cart
        if self.added_product==0:
            return f"\033[91m Failed => There is no product in the cart.\033[0m"
            
        # Remove the product from the inventory page
        remove_button_locator = self.product_locator.locator("..").locator("..").locator("..").locator(".btn_secondary")
        remove_button_locator.click()

        add_button_locator = self.product_locator.locator("..").locator("..").locator("..").locator(".btn_inventory")
        
        # Verify the "Add to cart" button reappears and cart count decrements
        if (   
            add_button_locator.text_content()=="Add to cart" and
            int(self.cart_badge_locator.text_content()) == self.added_product-1
        ):
            return f"\033[92m Passed => '{self.product_name}' successfully removed from the inventory page.\033[0m"
        else:
            return f"\033[91m Failed => Failed to remove '{self.product_name}' from the inventory page.\033[0m"
    
    def remove_product_from_cart_page(self):
        # Abort due to empty cart
        if self.added_product==0:
            return f"\033[91m Failed => There is no product in the cart.\033[0m"

        # Navigate to the cart page
        cart_button_locator = self.page.locator(".shopping_cart_link")
        cart_button_locator.click()

        # Remove the product from the cart page
        remove_button_locator = self.product_locator.locator("..").locator("..").locator(".btn_secondary")
        remove_button_locator.click()

        # Verify the cart count decrements correctly
        if (int(self.cart_badge_locator.text_content()) == self.added_product-1):
            return f"\033[92m Passed => '{self.product_name}' successfully removed from the cart page.\033[0m"
        else:
            return f"\033[91m Failed => Failed to remove '{self.product_name}' from the cart page.\033[0m"
    
    def remove_product_from_productdetails_page(self):
        # Abort due to empty cart
        if self.added_product==0:
            return f"\033[91m Failed => There is no product in the cart.\033[0m"
        
        # Navigate to product details page
        self.product_locator.click()

        # Remove the product from the product details page
        remove_button_locator = self.page.locator("#remove")
        remove_button_locator.click()

        add_button_locator = self.page.locator("#add-to-cart")
 
        # Verify the "Add to cart" button is available
        if (add_button_locator.count() == 1):
            return f"\033[92m Passed => '{self.product_name}' successfully removed from the product details page.\033[0m"
        else:
            return f"\033[91m Failed => Failed to remove '{self.product_name}' from the product details page.\033[0m"

    
    

   

        
        
        

        