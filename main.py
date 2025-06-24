import os
from splinter import Browser
from contextlib import contextmanager
from dotenv import load_dotenv
from src.helpers.helpers import handle_cookies_shoopify
from src.pageobjects.shopify_pageobjects import PAGE_OBJECTS
import time
from selenium.webdriver.common.keys import Keys
import random
import json


HANDLED_COOKIES = False


@contextmanager
def browser_setup():
    browser = Browser("chrome")
    try:
        yield browser
    finally:
        browser.quit()


def purchase_product(browser):
    seconds = 30
    max_time = int(seconds)
    start_time = time.time()
    while (time.time() - start_time) < max_time:
        browser.visit(os.getenv("SHOPIFY_BASE_URL"))
        try:
            print("\nAttempting new order!")
            login_into_shopify(browser)
            global HANDLED_COOKIES
            HANDLED_COOKIES = handle_cookies_shoopify(browser, HANDLED_COOKIES)

            array_of_products = None
            with open("products.json", "r") as file:
                array_of_products = json.load(file)
            random_product_ISBN = random.choice(array_of_products)

            search_product_by_isbn(random_product_ISBN)
            buy_now_btn_by_css = browser.find_by_css(
                PAGE_OBJECTS["elem"]["buy_now_btn_by_css"]
            )
            buy_now_btn_by_css.click()

            card_info = {
                "card_number": os.getenv("CARD_NUMBER"),
                "card_expiration": 1133,
                "card_security_code": os.getenv("CARD_SECURITY_CODE"),
                "card_holder_name": os.getenv("CARD_HOLDER_NAME"),
            }

            buyer_info = {
                "buyer_name": "Automation",
                "buyer_surname": "Automatez",
                "address_name": "Avenida de Castilla 12",
                "postcode": "28830",
                "city": "San Fernando",
                "province": "Madrid",
            }

            invoice_info = {"document_type": "nif", "document_number": "99345262M"}

            complete_product_purchase(
                "oxfordpremiumqa@gmail.com", card_info, buyer_info, invoice_info, None
            )
            time.sleep(5)
        except Exception as e:
            print(f"ERROR: {e}")
            pass


def login_into_shopify(browser):
    login_with_password_by_class = browser.find_by_css(
        PAGE_OBJECTS["elem"]["login_with_password_by_class"], wait_time=5
    )
    if login_with_password_by_class and login_with_password_by_class.is_visible():
        login_with_password_by_class.click()
        password_input_by_id = browser.find_by_id(
            PAGE_OBJECTS["elem"]["password_input_by_id"]
        )
        password_input_by_id.type(os.getenv("SHOPIFY_PASSWORD"))
        login_btn_by_name = browser.find_by_name(
            PAGE_OBJECTS["elem"]["login_btn_by_name"]
        )
        login_btn_by_name.click()


def search_product_by_isbn(isbn):
    magnifying_glass_btn_by_css = browser.find_by_css(
        PAGE_OBJECTS["elem"]["magnifying_glass_btn_by_css"]
    )
    magnifying_glass_btn_by_css.click()
    search_input_by_id = browser.find_by_id(PAGE_OBJECTS["elem"]["search_input_by_id"])
    search_input_by_id.type(isbn)
    search_btn_by_css = browser.find_by_css(PAGE_OBJECTS["elem"]["search_btn_by_css"])
    search_btn_by_css.click()
    time.sleep(1)
    first_result_product_card_by_css = browser.find_by_css(
        PAGE_OBJECTS["elem"]["first_result_product_card_by_css"]
    )
    first_result_product_card_by_css.click()


def complete_product_purchase(
    email_address, card_info, buyer_info, invoice_info, coupon
):

    email_input_by_id = browser.find_by_id(
        PAGE_OBJECTS["elem"]["email_input_by_id"], wait_time=5
    )
    email_input_by_id.type(email_address)

    iframes = browser.find_by_css("iframe.card-fields-iframe")

    with browser.get_iframe(iframes[0]) as number_iframe:
        card_number_input_by_id = number_iframe.find_by_id(
            PAGE_OBJECTS["elem"]["card_number_input_by_id"], wait_time=5
        )
        card_number_input_by_id.type(card_info["card_number"])

    with browser.get_iframe(iframes[1]) as expiration_date_iframe:
        expiration_date_input_by_id = expiration_date_iframe.find_by_id(
            PAGE_OBJECTS["elem"]["expiration_date_input_by_id"]
        )
        browser.type("expiry", "09")
        time.sleep(1)
        browser.type("expiry", "35")

    with browser.get_iframe(iframes[2]) as security_code_iframe:
        security_code_input_by_id = security_code_iframe.find_by_id(
            PAGE_OBJECTS["elem"]["security_code_input_by_id"]
        )
        security_code_input_by_id.type(card_info["card_security_code"])

    with browser.get_iframe(iframes[len(iframes) - 1]) as card_holder_name_iframe:
        card_holder_name_input_by_id = card_holder_name_iframe.find_by_id(
            PAGE_OBJECTS["elem"]["card_holder_name_input_by_id"]
        )
        card_holder_name_input_by_id.type(card_info["card_holder_name"])

    buyer_name_input_by_id = browser.find_by_id(
        PAGE_OBJECTS["elem"]["buyer_name_input_by_id"]
    )
    buyer_name_input_by_id.type(buyer_info["buyer_name"])
    buyer_surname_input_by_id = browser.find_by_id(
        PAGE_OBJECTS["elem"]["buyer_surname_input_by_id"]
    )
    buyer_surname_input_by_id.type(buyer_info["buyer_surname"])
    address_input_by_id = browser.find_by_id(
        PAGE_OBJECTS["elem"]["address_input_by_id"]
    )
    address_input_by_id.type(buyer_info["address_name"])
    postcode_input_by_id = browser.find_by_id(
        PAGE_OBJECTS["elem"]["postcode_input_by_id"]
    )
    postcode_input_by_id.type(buyer_info["postcode"])
    city_input_by_id = browser.find_by_id(PAGE_OBJECTS["elem"]["city_input_by_id"])
    city_input_by_id.type(buyer_info["city"])

    checkboxes = browser.find_by_css('input[type="checkbox"]')

    invoice_checkbox = checkboxes[0]
    invoice_checkbox.click()

    id_card_type_select_box_by_id = browser.find_by_id(
        PAGE_OBJECTS["elem"]["id_card_type_select_box_by_id"]
    )
    id_card_type_select_box_by_id.select(invoice_info["document_type"])

    id_card_number_input_by_id = browser.find_by_id(
        PAGE_OBJECTS["elem"]["id_card_number_input_by_id"]
    )
    id_card_number_input_by_id.type(invoice_info["document_number"])

    terms_and_conditions_checkbox = checkboxes[1]
    terms_and_conditions_checkbox.click()

    checkout_btn_by_id = browser.find_by_id(PAGE_OBJECTS["elem"]["checkout_btn_by_id"])
    checkout_btn_by_id.click()

    result_text = browser.find_by_text(
        f"¡Gracias, {buyer_info["buyer_name"]}!", wait_time=10
    )
    assert result_text.is_visible()
    print("Order completed correctly, waiting 60 seconds...\n\n")
    # time.sleep(60)


if __name__ == "__main__":
    load_dotenv()
    with browser_setup() as browser:
        purchase_product(browser)
