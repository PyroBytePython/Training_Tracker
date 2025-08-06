from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils import timezone

from Tracker.models import Workout, Exercise, Set


class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = ["date", "comment"]

    def clean_date(self):
        date = self.cleaned_date["date"]
        if date > timezone.now():
            raise ValidationError("Не может быть в будущем")
        return date


class ExerciseForm(ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'muscle_group']


class SetForm(ModelForm):
    class Meta:
        model = Set
        fields = ['weight', 'reps', 'rest_after_set']

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
