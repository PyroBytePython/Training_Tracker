from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils import timezone
from django import forms

from Tracker.models import Workout, Exercise, Set


class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = ["comment"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Добавляем placeholder для текстового поля
        self.fields['comment'].widget = forms.Textarea(attrs={
            'placeholder': 'Опишите вашу тренировку...',
            'class': 'form-control',
            'rows': 4
        })

    def clean_date(self):
        date = self.cleaned_data["date"]
        if date > timezone.now():
            raise ValidationError("Не может быть в будущем")
        return date

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user  # Устанавливаем пользователя
        if commit:
            instance.save()
        return instance


class ExerciseForm(ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'muscle_group']


class SetForm(ModelForm):
    class Meta:
        model = Set
        fields = ['weight', 'reps', 'exercise']

    def clean_weight(self):
        weight = self.cleaned_data["weight"]

        if weight < 0:
            raise ValidationError('Не может быть меньше 0')
        if weight > 500:
            raise ValidationError('Слишком тяжелый вес')
        return weight

    def clean_reps(self):
        reps = self.cleaned_data['reps']

        if reps < 1:
            raise ValidationError('Минимум 1 повторение')
