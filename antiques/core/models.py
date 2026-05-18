import os
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings

# 🔹 Динамический путь для аватара (вычисляется при загрузке файла)
def user_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    # Безопасно используем ID пользователя вместо username
    return f"avatars/{instance.user.id}/{filename}"

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Profile(models.Model):
    GENDER_CHOICES = (
        ("М", "Мужской"),
        ("Ж", "Женский")
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to=user_avatar_path, null=True, blank=True, verbose_name="Аватар")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    phone_number = models.CharField(max_length=12, null=True, blank=True, verbose_name="Мобильный телефон")
    patronymic = models.CharField(max_length=50, null=True, blank=True, verbose_name="Отчество")  # ✅ добавлен max_length
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name="Город")  # ✅ добавлен max_length
    birthday = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    about = models.TextField(null=True, blank=True, verbose_name="О себе")

    def __str__(self):
        return f"Профиль {self.user.email}"  # ✅ username заменён на email

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"