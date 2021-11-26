from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render

def home_page(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<html><title>To-Do lists</title></html>")