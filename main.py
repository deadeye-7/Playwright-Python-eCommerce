from playwright.sync_api import sync_playwright
from login import *
from logout import *
from cart import *
from checkout import *

import os
from datetime import datetime

# Create folder with timestamp
timestamp = datetime.now().strftime("%d-%m-%Y %H-%M")
screenshot_dir= os.path.join("/Users/jubairshome/Documents/myGitRepo/Playwright-python-automation/Web UI - SauceDemo/Screenshots", timestamp)
os.makedirs(screenshot_dir, exist_ok=True)
print(f"Test run screenshots will be saved in: {screenshot_dir}")

with sync_playwright() as playwright:
    # Launch a browser
    browser = playwright.chromium.launch(headless=False)
    # Create a new page
    page = browser.new_page()

    
    print("======Test Login======")

    # Case 1: Unsuccessful Login
    username = "normal_user"
    password = "secret_sauce"

    login = UnsuccessfulLogin(page, username, password, screenshot_dir)
    print(login.validation())

    # Case 2: Locked out
    username = "locked_out_user"
    password = "secret_sauce"

    login = LockedOut(page, username, password, screenshot_dir)
    print(login.validation())

    # Case 3: Problem Login
    username = "problem_user"
    password = "secret_sauce"

    login = ProblemLogin(page, username, password, screenshot_dir)
    print(login.validation())

    # Case 4: Performance Glitch Login
    username = "performance_glitch_user"
    password = "secret_sauce"
    expected_url = "https://www.saucedemo.com/inventory.html"
    expected_login_time = 1

    login = PerformanceGlitchLogin(page, username, password, screenshot_dir)
    print(login.validation(expected_url,expected_login_time))
    
    # Case 5: Successful Login
    username = "standard_user"
    password = "secret_sauce"
    expected_url = "https://www.saucedemo.com/inventory.html"
    expected_inventory_count = 6
    expected_product_name = "Sauce Labs Backpack"

    login = SuccessfulLogin(page,username,password, screenshot_dir)
    print(login.validation(expected_url,expected_inventory_count,expected_product_name))

    
    print("======Test Add Product======")

    products_to_add = ["Sauce Labs Backpack","Sauce Labs Fleece Jacket","Sauce Labs Bolt T-Shirt","Sauce Labs Onesie"]
    for product_name in products_to_add:
        cart = AddProduct(page, product_name, screenshot_dir)
        added_from_inventory = cart.inventory_page_validation()
        print(added_from_inventory)
   
        added_from_cart = cart.cart_page_validation()
        print(added_from_cart)

        added_from_product_details = cart.productdetails_page_validation()
        print(added_from_product_details)

        # Navigate back to inventory page
        back_to_products_button_locator  = page.locator("#back-to-products")
        back_to_products_button_locator.click()
    
        print("------------------------")

    
    # Remove product from the cart
    print("======Test Remove Product======")
    
    cart = RemoveProduct(page,"Sauce Labs Backpack", screenshot_dir)
    remove_from_inventory = cart.remove_product_from_inventory_page()
    print(remove_from_inventory)

    cart = RemoveProduct(page,"Sauce Labs Fleece Jacket", screenshot_dir)
    remove_from_cart = cart.remove_product_from_cart_page()
    print(remove_from_cart)

    cart = RemoveProduct(page,"Sauce Labs Bolt T-Shirt", screenshot_dir)
    remove_from_product_details = cart.remove_product_from_productdetails_page()
    print(remove_from_product_details)
    
    # Checkout product
    print("======Test Checkout======")

    checkout = Checkout(page, screenshot_dir)

    # Verifying checkout step 1
    first_name = "John"
    last_name = "Doe"
    zip_code = "1212"
    expecxted_checkout_step1_url = "https://www.saucedemo.com/checkout-step-one.html"

    checkout_step1 = checkout.checkout_step1_validation(first_name,last_name,zip_code, expecxted_checkout_step1_url)
    print(checkout_step1)

    # Verifying checkout step 2
    sub_total = "7.99"
    tax = "0.64"
    total = "8.63"
    expecxted_checkout_step2_url = "https://www.saucedemo.com/checkout-step-two.html"

    #page.pause()
    checkout_step2 = checkout.checkout_step2_validation(sub_total, tax, total, expecxted_checkout_step2_url)
    print(checkout_step2)
    
    # Verifying checkout success step
    expected_complete_title = "Thank you for your order!"
    expected_complete_msg = "Your order has been dispatched, and will arrive just as fast as the pony can get there!"
    expected_checkout_complete_url = "https://www.saucedemo.com/checkout-complete.html"

    checkout_complete = checkout.checkout_complete_validation(expected_complete_title, expected_complete_msg, expected_checkout_complete_url)
    print(checkout_complete)
    
    # Verifying checkout complete step
    expecxted_inventory_page_url = "https://www.saucedemo.com/inventory.html"

    # Verifying inventory page redirection
    checkout_return_to_inventory_page = checkout.checkout_back_to_inventory(expecxted_inventory_page_url)
    print(checkout_return_to_inventory_page)
    
    # Logout
    print("======Test Logout======")
    
    logout = Logout(page, screenshot_dir)
    print(logout.validation())
    
    print("======Test Ends Here======")
    browser.close()





