from django.test.client import Client

import pytest
from pytest_django.asserts import assertTemplateUsed
from pytest_django.asserts import assertRedirects

from lists.models import Item
from lists.models import List


@pytest.mark.django_db
def test_displays_only_items_for_that_list(client: Client) -> None:
    correct_list = List.objects.create()
    Item.objects.create(text="itemey 1", list=correct_list)
    Item.objects.create(text="itemey 2", list=correct_list)

    other_list = List.objects.create()
    Item.objects.create(text="other list item 1", list=other_list)
    Item.objects.create(text="other list item 2", list=other_list)

    response = client.get(f"/lists/{correct_list.id}/")

    assert "itemey 1" in response.content.decode()
    assert "itemey 2" in response.content.decode()
    assert "other list item 1" not in response.content.decode()
    assert "other list item 2" not in response.content.decode()


@pytest.mark.django_db
def test_uses_list_template(client: Client) -> None:
    list_ = List.objects.create()
    response = client.get(f"/lists/{list_.id}/")
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
    new_list = List.objects.first()
    assertRedirects(response, f"/lists/{new_list.id}/")


@pytest.mark.django_db
def test_can_save_a_POST_request_to_an_existing_list(client: Client) -> None:
    other_list = List.objects.create()
    correct_list = List.objects.create()

    client.post(
        f"/lists/{correct_list.id}/add_item",
        data={"item_text": "A new item for an existing list"},
    )

    assert Item.objects.count() == 1
    new_item = Item.objects.first()
    assert new_item.text == "A new item for an existing list"
    assert new_item.list == correct_list


@pytest.mark.django_db
def test_redirects_to_list_view(client: Client) -> None:
    other_list = List.objects.create()
    correct_list = List.objects.create()

    response = client.post(
        f"/lists/{correct_list.id}/add_item",
        data={"item_text": "A new item for an existing list"},
    )

    assertRedirects(response, f"/lists/{correct_list.id}/")


@pytest.mark.django_db
def test_passes_correct_list_to_template(client: Client) -> None:
    other_list = List.objects.create()
    correct_list = List.objects.create()
    response = client.get(f"/lists/{correct_list.id}/")
    assert response.context["list"] == correct_list
