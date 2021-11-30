from django.http import HttpRequest, response
from django.test.client import Client
from django.urls import resolve

import pytest
from pytest_django.asserts import assertContains
from pytest_django.asserts import assertTemplateUsed

from lists.models import Item
from lists.views import home_page


def test_root_url_resolves_to_home_page_view() -> None:
    found = resolve("/")
    assert found.func == home_page


@pytest.mark.django_db
def test_home_page_returns_correct_html(client: Client) -> None:
    response = client.get("/")

    html = response.content.decode("utf8")
    assert html.startswith("<html>")
    assert "<title>To-Do lists</title>" in html
    assert html.endswith("</html>")


@pytest.mark.django_db
def test_home_view_uses_home_template(client: Client) -> None:
    response = client.get("/")
    assertTemplateUsed(response, 'home.html')


@pytest.mark.django_db
def test_can_save_a_POST_request(client: Client) -> None:
    response = client.post("/", data={"item_text": "A new list item"})

    assert Item.objects.count() == 1
    new_item = Item.objects.first()
    assert new_item.text == "A new list item"


@pytest.mark.django_db
def test_redirects_after_POST(client: Client) -> None:
    response = client.post("/",  data={"item_text": "A new list item"})
    assert response.status_code == 302
    assert response["location"] == "/lists/the-only-list-in-the-world/"


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


@pytest.mark.django_db
def test_only_saves_items_when_necessary(client: Client) -> None:
    response = client.get("/")
    assert Item.objects.count() == 0


@pytest.mark.django_db
def test_list_view_displays_all_items(client: Client) -> None:
    Item.objects.create(text="itemey 1")
    Item.objects.create(text="itemey 2")

    response = client.get("/lists/the-only-list-in-the-world/")

    assert "itemey 1" in response.content.decode()
    assert "itemey 2" in response.content.decode() 


@pytest.mark.django_db
def test_list_view_uses_list_template(client: Client) -> None:
    response = client.get("/lists/the-only-list-in-the-world/")
    assertTemplateUsed(response, "list.html")