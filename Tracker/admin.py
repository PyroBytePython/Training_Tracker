from django.contrib import admin
from .models import Workout, Set, Exercise


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('date', 'comment', 'user')
    list_filter = ('date',)
    search_fields = ('date', 'comment')
    ordering = ['-date']


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'muscle_group', 'workout')
    list_filter = ('name', 'muscle_group')
    search_fields = ('name', 'muscle_group')
    ordering = ['-name']


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'weight', 'reps', 'rest_after_set')
    list_filter = ('weight', 'reps')
    search_fields = ('weight', 'reps')

