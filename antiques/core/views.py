from django.shortcuts import render

def index(request):
    context = {}
    context["title"] = "Антиквариат"
    return render(request, "core/core.html", context=context)