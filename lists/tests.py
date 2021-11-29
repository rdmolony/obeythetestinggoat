from django.http import HttpRequest, response
from django.test.client import Client
from django.urls import resolve

import pytest
from pytest_django.asserts import assertTemplateUsed

from lists.models import Item
from lists.views import home_page


def test_root_url_resolves_to_home_page_view() -> None:
    found = resolve("/")
    assert found.func == home_page


def test_home_page_returns_correct_html(client: Client) -> None:
    response = client.get("/")

    html = response.content.decode("utf8")
    assert html.startswith("<html>")
    assert "<title>To-Do lists</title>" in html
    assert html.endswith("</html>")


def test_uses_home_template(client: Client) -> None:
    response = client.get("/")
    assertTemplateUsed(response, 'home.html')


def test_can_save_a_POST_request(client: Client) -> None:
    response = client.post("/", data={"item_text": "A new list item"})
    assert "A new list item" in response.content.decode()
    assertTemplateUsed(response, "home.html")


@pytest.mark.django_db
def test_saving_and_retrieving_items(client: Client) -> None:
    first_item = Item()
    first_item.text = "The first (ever) list item"
    first_item.save()

    second_item = Item()
    second_item.text = "Item the second"
    second_item.save()

    saved_items = Item.objects.all()
    assert saved_items.count() == 2

    first_saved_item = saved_items[0]
    second_saved_item = saved_items[1]
    assert first_saved_item.text == "The first (ever) list item"
    assert second_saved_item.text == "Item the second"