import os
import random
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Создаёт или обновляет профиль пользователя"""
    profile, _ = UserProfile.objects.get_or_create(user=instance)

    if not profile.avatar:  # если аватар не задан
        defaults_path = os.path.join(settings.MEDIA_ROOT, 'avatars', 'defaults')
        default_avatars = os.listdir(defaults_path)
        if default_avatars:
            random_avatar = random.choice(default_avatars)
            profile.avatar = f'avatars/defaults/{random_avatar}'
            profile.save()
