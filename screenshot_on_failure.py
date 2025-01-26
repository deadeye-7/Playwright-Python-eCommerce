import os
from playwright.sync_api import Page

def screenshot_on_failure(page:Page, screenshot_dir, filename):
    # Concatenating file directory with the filenae
    screenshot_path = os.path.join(screenshot_dir, filename)

    # Taking the sceenshot
    page.screenshot(path=screenshot_path, full_page=True)