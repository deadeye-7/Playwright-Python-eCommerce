import pytest
from playwright.sync_api import sync_playwright
from login import *

import os
from datetime import datetime

# Create folder with timestamp
timestamp = datetime.now().strftime("%d-%m-%Y %H-%M")
screenshot_dir= os.path.join("/Users/jubairshome/Documents/myGitRepo/Playwright-python-automation/Web UI - SauceDemo/Screenshots", timestamp)
os.makedirs(screenshot_dir, exist_ok=True)

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
    expected_product_name = "Sauce Labs Backpack"

    login = SuccessfulLogin(page, username, password, screenshot_dir)
    result = login.validation(expected_url, inventory_count, expected_product_name)
    assert "Passed" in result, result

def test_unsuccessful_login(page):
    # Invalid credentials for unsuccessful login
    username = "invalid_user"
    password = "wrong_password"

    login = UnsuccessfulLogin(page, username, password, screenshot_dir)
    result = login.validation()
    assert "Passed" in result, result

def test_locked_out_user(page):
    # Locked out user credentials
    username = "locked_out_user"
    password = "secret_sauce"

    login = LockedOut(page, username, password, screenshot_dir)
    result = login.validation()
    assert "Passed" in result, result

def test_problem_user_login(page):
    # Problematic user credentials
    username = "problem_user"
    password = "secret_sauce"

    login = ProblemLogin(page, username, password, screenshot_dir)
    result = login.validation()
    assert "Passed" in result, result

def test_performance_glitch_user_login(page):
    # Performance glitch user credentials
    username = "performance_glitch_user"
    password = "secret_sauce"
    expected_url = "https://www.saucedemo.com/inventory.html"
    expected_login_time = 1

    login = PerformanceGlitchLogin(page, username, password, screenshot_dir)
    result = login.validation(expected_url, expected_login_time)
    assert "Passed" in result, result