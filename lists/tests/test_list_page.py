from django.test.client import Client

import pytest
from pytest_django.asserts import assertTemplateUsed

from lists.models import Item


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