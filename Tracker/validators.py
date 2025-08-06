from django.core.exceptions import ValidationError


def validate_reps(value):
    if value < 1:
        raise ValidationError("Минимум 1 повторение")


def validate_weight(value):
    if value < 0:
        raise ValidationError("Должен быть больше 0")
    if value > 500:
        raise ValidationError("Вес слишком большой")
