from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

def index(request):
    context = {}
    context["title"] = "Маркетплейс"
    return render(request, "core/content.html", context=context)

@ensure_csrf_cookie
@require_POST
def login_view(request):
    import json
    data = json.loads(request.body)
    user = authenticate(request, username=data.get('email'), password=data.get('password'))

    if user:
        login(request, user)
        print("Успешный вход")
        return JsonResponse({"success": True}, status=200)
    else:
        print("Не зашел")
        return JsonResponse({"error": "Неверный логин или пароль"}, status=401)

@ensure_csrf_cookie
@require_POST
def reg_view(request):
    import json
    from django.contrib.auth import get_user_model
    User = get_user_model()
    data = json.loads(request.body)

    email = data.get('email', '').lower().strip()
    password = data.get('password')
    password_confirm = data.get('password_confirm')
    first_name = data.get('first_name', '').strip()
    last_name = data.get('last_name', '').strip()

    errors = {}

    if not email or '@' not in email:
        errors['email'] = ['Введите корректный email']
    elif User.objects.filter(email=email).exists():
        errors['email'] = ['Пользователь с таким email уже существует']

    if not password or len(password) < 8:
        errors['password'] = ['Пароль должен содержать минимум 8 символов']
    elif password != password_confirm:
        errors['password_confirm'] = ['Пароли не совпадают']

    if not first_name:
        errors['first_name'] = ['Введите имя']

    if errors:
        return JsonResponse(errors, status=400)

    user = User.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )

    return JsonResponse({
        'success': True,
        'message': 'Регистрация успешна',
        'user': {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name
        }
    }, status=201)

def logout_view(request):
    logout(request)
    return redirect("home")