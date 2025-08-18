from django.db import models
import random

from users.models import User
from .validators import validate_weight, validate_reps


class WorkoutQuerySet(models.QuerySet):
    def search_comment(self, comment):
        return self.filter(comment=comment)


class Workout(models.Model):
    """Модель создания тренировки"""

    date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата тренировки", help_text="Дата тренировки"
    )
    comment = models.TextField(
        null=True,
        blank=True,
        verbose_name="Комментарий",
        help_text="Заметка о тренировке",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='workouts'
    )

    class Meta:
        verbose_name = "Тренировка"
        verbose_name_plural = "Тренировки"
        ordering = ["-date"]

    def __str__(self):
        return f"Тренировка от {self.date.strftime('%d.%m.%Y')}"


class Exercise(models.Model):
    """Модель упражнений для тренировки"""

    MUSCLE_GROUPS = [
        ("chest", "Грудь"),
        ("back", "Спина"),
        ("arms", "Руки"),
        ("legs", "Ноги"),
        ("core", "Пресс"),
        ("cardio", "Кардио"),
    ]

    name = models.CharField(
        max_length=250,
        verbose_name="Название упражнения",
        help_text="Укажите название упражнения",
    )
    muscle_group = models.CharField(
        max_length=100,
        choices=MUSCLE_GROUPS,
        verbose_name="Группа мышц",
        help_text="Выберите необходимую группу мышц",
    )
    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
        verbose_name="Тренировка",
        related_name="exercises",
    )

    class Meta:
        verbose_name = "Упражнение"
        verbose_name_plural = "Упражнения"

    def __str__(self):
        return f"{self.name} ({self.get_muscle_group_display()})"


class Set(models.Model):
    """Модель подходов упражнений"""

    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        verbose_name="Упражнение",
        related_name="sets",
    )
    weight = models.FloatField(
        verbose_name="Вес",
        help_text="Вес в кг",
        validators=[validate_weight],
        default=0,
    )
    reps = models.PositiveIntegerField(
        verbose_name="Количество повторений",
        validators=[validate_reps],
    )
    rest_after_set = models.PositiveIntegerField(
        verbose_name="Отдых после подхода",
        help_text="Отдых после подхода в секундах",
        blank=True,
        null=True,
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Иконка"
    )

    ICONS = [
        "bi-barbell",  # штанга
        "bi-trophy",  # трофей
        "bi-stopwatch",  # секундомер
        "bi-lightning-charge",  # энергия
        "bi-fire",  # интенсивность
        "bi-heart-pulse",  # сердечный ритм
        "bi-award",  # награда
        "bi-speedometer2",  # скорость
        "bi-shield-check"  # выносливость
    ]

    def save(self, *args, **kwargs):
        if not self.icon:
            self.icon = random.choice(self.ICONS)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Подход"
        verbose_name_plural = "Подходы"

    def __str__(self):
        return f"{self.weight} кг × {self.reps} повт."
