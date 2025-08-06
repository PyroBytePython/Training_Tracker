from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView, DeleteView,
)

from Tracker.forms import WorkoutForm, ExerciseForm, SetForm
from Tracker.models import Workout


class WorkoutListView(ListView):
    """Представление списка тренировок"""
    model = Workout
    template_name = "workout_list.html"
    context_object_name = "workouts"
    paginate_by = 15

    def get_queryset(self):
        queryset = Workout.objects.all().order_by("-date")

        comment = self.request.GET.get("comment")
        if comment:
            queryset = queryset.search_comment(comment)
        return queryset


class WorkoutCreateView(CreateView):
    """Создание тренировки"""
    form_class = WorkoutForm
    template_name = "form.html"
    success_url = reverse_lazy("workout:workout_list")


class WorkoutDetailView(DetailView):
    """Вывод 1 тренировки"""
    model = Workout
    template_name = 'workout_detail.html'
    context_object_name = 'workout'


class WorkoutUpdateView(UpdateView):
    """Обновление тренировки"""
    model = Workout
    template_name = 'workout_update.html'
    form_class = WorkoutForm


class WorkoutDeleteView(DeleteView):
    """Удаление тренировки"""
    model = Workout
    template_name = 'workout_confirm_delete.html'
    success_url = reverse_lazy('workout_list.html')


class ExerciseCreateView(CreateView):
    """Создание упражнений"""
    form_class = ExerciseForm
    template_name = "form.html"
    success_url = reverse_lazy("workout:exercises_list")
    context_object_name = 'exercises'


class SetCreateView(CreateView):
    """Создание подходов"""
    form_class = SetForm
    template_name = "form.html"
    success_url = reverse_lazy("workout:sets_list")
    context_object_name = 'sets'
