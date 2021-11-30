from django.test.client import Client
from django.urls import resolve

import pytest
from pytest_django.asserts import assertTemplateUsed

from lists.models import Item
from lists.views import home_page


def test_root_url_resolves_to_home_page_view() -> None:
    found = resolve("/")
    assert found.func == home_page


@pytest.mark.django_db
def test_returns_correct_html(client: Client) -> None:
    response = client.get("/")

    html = response.content.decode("utf8")
    assert html.startswith("<html>")
    assert "<title>To-Do lists</title>" in html
    assert html.endswith("</html>")


@pytest.mark.django_db
def test_uses_home_template(client: Client) -> None:
    response = client.get("/")
    assertTemplateUsed(response, 'home.html')


@pytest.mark.django_db
def test_can_save_a_POST_request(client: Client) -> None:
    response = client.post("/", data={"item_text": "A new list item"})

    assert Item.objects.count() == 1
    new_item = Item.objects.first()
    assert new_item.text == "A new list item"


@pytest.mark.django_db
def test_only_saves_items_when_necessary(client: Client) -> None:
    response = client.get("/")
    assert Item.objects.count() == 0

