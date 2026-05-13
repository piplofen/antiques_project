from django.shortcuts import render

def index(request):
    context = {}
    context["title"] = "Услуги"
    return render(request, "services/content.html", context=context)
