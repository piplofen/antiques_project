from django.shortcuts import render

def profile_view(request):
    context = {}
    context["title"] = "Профиль"
    context["user"] = request.user
    return render(request, "profile_manager/profile.html", context=context)