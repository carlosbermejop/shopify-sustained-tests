from src.pageobjects.shopify_pageobjects import PAGE_OBJECTS
import time


def handle_cookies_shoopify(browser, handled_cookies):
    cookies_btn_by_id = browser.find_by_id(
        PAGE_OBJECTS["elem"]["cookies_btn_by_id"], wait_time=2
    )
    if (
        handled_cookies == False
        and cookies_btn_by_id
        and cookies_btn_by_id.is_visible(wait_time=2)
    ):
        cookies_btn_by_id.click()
        time.sleep(1)
        print("Cookie banner dealt with!")
        return True
    else:
        print("Cookie banner was not found")
        return False
