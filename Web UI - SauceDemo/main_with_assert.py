from playwright.sync_api import sync_playwright
from login import *
from logout import *
from cart import *
from checkout import *


with sync_playwright() as playwright:
    # Launch a browser
    browser = playwright.chromium.launch(headless=False)

    # Create a new page
    page = browser.new_page()
    
    print("======Test Login======")

    # Case 1: Unsuccessful Login
    login = UnsuccessfulLogin(page,"normal_user", "secret_sauce")
    assert login.validation(), "Unsucessful login is not validated"
    print("Case 1: Unsuccessful Login")

    # Case 2: Locked out
    locked_out = LockedOut(page, "locked_out_user","secret_sauce")
    login_locked_out = locked_out.validation()
    assert login_locked_out, "Locked out login is not validated"
    print("Case 2: Locked out")

    # Case 3: Problem Login
    problem_after_login = ProblemLogin(page,"problem_user","secret_sauce")
    login_problem = problem_after_login.validation()
    assert login_problem, "Problem after login is not validated"
    print("Case 3: Problem Login")

    # Case 4: Performance Glitch Login
    performance_glitch_login = PerformanceGlitchLogin(page,"performance_glitch_user","secret_sauce")
    
    # Check the login duration is within the limit
    assert performance_glitch_login.login_duration < 6, "It didn't meet the performance criteria"
    print(f"=> Login time: {performance_glitch_login.login_duration:.2f} sec")
    
    login_problem = performance_glitch_login.validation("https://www.saucedemo.com/inventory.html")
    assert login_problem, "User was not logged in successfully."
    print("Case 4: Performance glitch Login")

    # Case 5: Successful Login
    successful_login = SuccessfulLogin(page,"standard_user", "secret_sauce")
    login_passed = successful_login.validation("https://www.saucedemo.com/inventory.html", 6)
    assert login_passed,"User was not logged in successfully."
    print("Case 5: Successful Login")
    

    
    #page.pause()
    # Add products to Cart
    print("======Test Add Product======")

    products_to_add = ["Sauce Labs Backpack","Sauce Labs Fleece Jacket","Sauce Labs Bolt T-Shirt","Sauce Labs Onesie"]
    for product_name in products_to_add:
        cart = AddProduct(page, product_name)
        inventory_page = cart.inventory_page_validation()
        assert inventory_page, f"{product_name} is not added in inventory page"

        cart_page = cart.cart_page_validation()
        assert cart_page, f"{product_name} is not added in cart page"

        product_page = cart.productdetails_page_validation()
        assert product_page, f"{product_name} is not added in product page"

        page.locator("#back-to-products").click()
    
        print(f"{product_name} added to the cart successfully")

    
    # Remove product from the cart
    print("======Test Remove Product======")
    
    cart = RemoveProduct(page,"Sauce Labs Backpack")
    remove_from_inventory = cart.remove_product_from_inventory_page()
    assert remove_from_inventory, f"{cart.product_name} is not removed from inventory page"
    print(f"Case 1:{cart.product_name} removed successfully")

    cart = RemoveProduct(page,"Sauce Labs Fleece Jacket")
    remove_from_cart = cart.remove_product_from_cart_page()
    assert remove_from_cart, f"{cart.product_name} is not removed from cart page"
    print(f"Case 2:{cart.product_name} removed successfully")

    cart = RemoveProduct(page,"Sauce Labs Bolt T-Shirt")
    remove_from_product = cart.remove_product_from_productdetails_page()
    assert remove_from_product, f"{cart.product_name} is not removed from product page"
    print(f"Case 3:{cart.product_name} removed successfully")

    # Checkout
    print("======Test Checkout======")
    checkout = Checkout(page)

    checkout_step1 = checkout.checkout_step1_validation("John", "Doe", "1212")
    assert checkout_step1, "There were some problems with checkout step1"
    
    checkout_step2 = checkout.checkout_step2_validation("7.99","0.64","8.63")
    assert checkout_step2, "There were some problems with checkout step2"

    checkout_success = checkout.checkout_complete_validation("Thank you for your order!","Your order has been dispatched, and will arrive just as fast as the pony can get there!")
    assert checkout_success, "There were some problems with checkout complete"

    checkout_complete = checkout.checkout_back_to_inventory()
    assert checkout_complete, "There were some problems with navigating back to inventory page"

    print("Products checked out successfully")
    
    # Logout
    print("======Test Logout======")
    
    logout = Logout(page)
    logout.validation()
    print("Logged out successfully")

    print("======Test Ends Here======")
    browser.close()





