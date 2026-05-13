from django.shortcuts import render

def index(request):
    context = {}
    context["title"] = "Форум"
    return render(request, "forum/content.html", context=context)