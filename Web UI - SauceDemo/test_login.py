import pytest
from playwright.sync_api import sync_playwright
from login import *

@pytest.fixture(scope="function")
def page():
    with sync_playwright() as playwright:
        # Setup Playwright browser and page
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        yield page
        # Teardown Playwright browser
        browser.close()

def test_successful_login(page):
    # Valid credentials for successful login
    username = "standard_user"
    password = "secret_sauce"
    expected_url = "https://www.saucedemo.com/inventory.html"
    inventory_count = 6

    login = SuccessfulLogin(page, username, password)
    assert login.validation(expected_url, inventory_count), \
        "Login was successful but validation failed."

def test_unsuccessful_login(page):
    # Invalid credentials for unsuccessful login
    username = "invalid_user"
    password = "wrong_password"

    login = UnsuccessfulLogin(page, username, password)
    assert login.validation(), \
        "Unsuccessful login did not display the correct error message."

def test_locked_out_user(page):
    # Locked out user credentials
    username = "locked_out_user"
    password = "secret_sauce"

    login = LockedOut(page, username, password)
    assert login.validation(), \
        "Locked-out error message was not displayed correctly."

def test_problem_user_login(page):
    # Problematic user credentials
    username = "problem_user"
    password = "secret_sauce"

    login = ProblemLogin(page, username, password)
    assert login.validation(), \
        "Problematic user did not display incorrect product data."

def test_performance_glitch_user_login(page):
    # Performance glitch user credentials
    username = "performance_glitch_user"
    password = "secret_sauce"
    expected_url = "https://www.saucedemo.com/inventory.html"

    login = PerformanceGlitchLogin(page, username, password)
    assert login.validation(expected_url), \
        "Performance glitch user login did not navigate to the expected URL."
    assert login.login_duration < 1, \
        "Login took longer than expected for performance glitch user."