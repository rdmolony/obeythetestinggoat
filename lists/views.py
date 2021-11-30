from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from lists.models import Item


def home_page(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        Item.objects.create(text=request.POST["item_text"])
        return redirect("/lists/the-only-list-in-the-world/")
    
    items = Item.objects.all()
    return render(request, "home.html")


def view_list(request: HttpRequest) -> HttpResponse:
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})