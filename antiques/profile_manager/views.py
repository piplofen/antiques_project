from django.shortcuts import render
from core.models import Profile

def profile_view(request):
    context = {}
    context["title"] = "Профиль"
    context["user"] = request.user
    return render(request, "profile_manager/profile.html", context=context)

def edit_view(request):
    context = {}
    context["title"] = "Редактирование профиля"
    context["user"] = request.user
    context["gender_choices"] = Profile.GENDER_CHOICES
    return render(request, "profile_manager/profile_edit.html", context=context)