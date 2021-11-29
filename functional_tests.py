import socket
import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def _get_host_ipaddess() -> str:
    host_name = socket.gethostname()
    host_ipaddress = socket.gethostbyname(host_name)
    return host_ipaddress


@pytest.fixture
def webdriver_init() -> webdriver.Remote:
    browser = webdriver.Remote(
        command_executor="http://selenium:4444/wd/hub",
        desired_capabilities=DesiredCapabilities.CHROME,
    )
    yield browser
    browser.quit()


def check_for_row_in_list_table(browser: webdriver.Remote, row_text: str) -> None:
    table = browser.find_element_by_id("id_list_table")
    rows = table.find_elements_by_tag_name("tr")
    assert row_text in [row.text for row in rows]


@pytest.mark.django_db
def test_can_start_a_list_and_retrieve_it_later(
    webdriver_init: webdriver.Remote,
) -> None:
    browser = webdriver_init
    host_ipaddress = _get_host_ipaddess()

    # Edith has heard about a cool new online to-do app. She goes
    # to check out its homepage
    browser.get(f"http://{host_ipaddress}:8000")

    # She notices the page title and header mention to-do lists
    assert "To-Do" in browser.title
    header_text = browser.find_element_by_tag_name("h1").text
    assert "To-Do" in header_text

    # She is invited to enter a to-do item straight away
    inputbox = browser.find_element_by_id("id_new_name")
    assert inputbox.get_attribute("placeholder") == "Enter a to-do item"

    # She types "Buy peacock feathers" into a text box (Edith's hobby
    # is tying fly-fishing lures)
    inputbox.send_keys("Buy peacock feathers")

    # When she hits enter, the page updates, and now the page lists
    # "1: Buy peacock feathers" as an item in a to-do list
    inputbox.send_keys(Keys.ENTER)
    time.sleep(1)
    check_for_row_in_list_table(browser, "1: Buy peacock feathers")

    # There is still a text box inviting her to add another item. She
    # enters "Use peacock feathers to make a fly" (Edith is very methodical)
    inputbox = browser.find_element_by_id("id_new_name")
    inputbox.send_keys("Use peacock feathers to make a fly")
    inputbox.send_keys(Keys.ENTER)
    time.sleep(1)

    # The page updates again, and now shows both items on her list
    check_for_row_in_list_table(browser, "1: Buy peacock feathers")
    check_for_row_in_list_table(browser, "2: Use peacock feathers to make a fly")

    # Edith wonders whether the site will remember her list. Then she sees
    # that the site has generated a unique URL for her -- there is some
    # explanatory text to that effect.
    pytest.fail("Finish the test!")

    # She visits that URL - her to-do list is still there.

    # Satisfied, she goes back to sleep
