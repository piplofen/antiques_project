from django.shortcuts import render

def index(request):
    context = {}
    context["title"] = "Антиквариат"
    return render(request, "core/core_alt.html", context=context)