from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from lists.models import Item
from lists.models import List


def home_page(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html")


def view_list(request: HttpRequest, list_id: str) -> HttpResponse:
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(request, "list.html", {"list": list_})


def new_list(request: HttpRequest) -> HttpResponse:
    list_ = List.objects.create()
    Item.objects.create(text=request.POST["item_text"], list=list_)
    return redirect(f"/lists/{list_.id}/")


def add_item(request: HttpRequest, list_id: str) -> HttpResponse:
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST["item_text"], list=list_)
    return redirect(f"/lists/{list_.id}/")
