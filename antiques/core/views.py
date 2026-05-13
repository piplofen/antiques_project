from django.shortcuts import render

def index(request):
    context = {}
    context["title"] = "Маркетплейс"
    return render(request, "core/content.html", context=context)