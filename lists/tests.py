from django.http import HttpRequest, response
from django.test.client import Client
from django.urls import resolve

from lists.views import home_page
from pytest_django.asserts import assertTemplateUsed

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
