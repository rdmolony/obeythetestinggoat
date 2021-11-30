from django.test.client import Client

import pytest
from pytest_django.asserts import assertTemplateUsed
from pytest_django.asserts import assertRedirects

from lists.models import Item


@pytest.mark.django_db
def test_displays_all_items(client: Client) -> None:
    Item.objects.create(text="itemey 1")
    Item.objects.create(text="itemey 2")

    response = client.get("/lists/the-only-list-in-the-world/")

    assert "itemey 1" in response.content.decode()
    assert "itemey 2" in response.content.decode()


@pytest.mark.django_db
def test_uses_list_template(client: Client) -> None:
    response = client.get("/lists/the-only-list-in-the-world/")
    assertTemplateUsed(response, "list.html")


@pytest.mark.django_db
def test_can_save_a_POST_request(client: Client) -> None:
    response = client.post("/lists/new", data={"item_text": "A new list item"})

    assert Item.objects.count() == 1
    new_item = Item.objects.first()
    assert new_item.text == "A new list item"


@pytest.mark.django_db
def test_redirects_after_POST(client: Client) -> None:
    response = client.post("/lists/new", data={"item_text": "A new list item"})

    assertRedirects(response, "/lists/the-only-list-in-the-world/")
