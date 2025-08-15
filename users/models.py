import random

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Создание пользователя"""
    email = models.EmailField(
        unique=True,
        verbose_name='Почта'
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name='Почта подтверждена'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class VerificationCode(models.Model):
    """Создание кода верификации"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    code = models.CharField(
        max_length=6,
        verbose_name='Код'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    is_used = models.BooleanField(
        default=False,
        verbose_name='Используется'
    )

    @classmethod
    def generate_code(cls, user):
        code = str(random.randint(100000, 999999))
        return cls.objects.create(user=user, code=code)


class UserProfile(models.Model):
    """Профиль пользователя"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    avatar = models.ImageField(
        verbose_name='Аватар пользователя',
        blank=True,
        null=True,
        upload_to='avatars/',
    )

    bio = models.TextField(
        blank=True,
        verbose_name='Описание о себе'
    )

    joined_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания профиля'
    )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user.username
