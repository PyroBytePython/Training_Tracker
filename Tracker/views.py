from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView, DeleteView, TemplateView,
)

from Tracker.forms import WorkoutForm, ExerciseForm, SetForm
from Tracker.models import Workout, Exercise
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'Tracker/menu.html'
    login_url = 'users:login'


class WorkoutListView(LoginRequiredMixin, ListView):
    """Представление списка тренировок"""
    model = Workout
    template_name = "workout_list.html"
    context_object_name = "workouts"
    paginate_by = 15

    def get_queryset(self):
        queryset = Workout.objects.filter(user=self.request.user).order_by("-date")

        comment = self.request.GET.get("comment")
        if comment:
            queryset = queryset.search_comment(comment)
        return queryset


class WorkoutCreateView(LoginRequiredMixin, CreateView):
    """Создание тренировки"""
    form_class = WorkoutForm
    template_name = "form.html"
    success_url = reverse_lazy("workout:workout_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class WorkoutDetailView(LoginRequiredMixin, DetailView):
    """Вывод 1 тренировки"""
    model = Workout
    template_name = 'workout_detail.html'
    context_object_name = 'workout'

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)


class WorkoutUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление тренировки"""
    model = Workout
    template_name = 'workout_update.html'
    form_class = WorkoutForm

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)


class WorkoutDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление тренировки"""
    model = Workout
    template_name = 'workout_confirm_delete.html'
    success_url = reverse_lazy('tracker:workout_list')

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)


class ExerciseCreateView(LoginRequiredMixin, CreateView):
    """Создание упражнений"""
    form_class = ExerciseForm
    template_name = "form.html"
    context_object_name = 'exercises'

    def form_valid(self, form):
        form.instance.workout_id = self.kwargs['workout_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tracker:workout_detail', kwargs={'pk': self.kwargs['workout_id']})


class SetCreateView(LoginRequiredMixin, CreateView):
    """Создание подходов"""
    form_class = SetForm
    template_name = "form.html"
    context_object_name = 'sets'

    def form_valid(self, form):
        form.instance.exercise_id = self.kwargs['exercise_id']
        return super().form_valid(form)

    def get_success_url(self):
        exercise = Exercise.objects.select_related('workout').get(id=self.kwargs['exercise_id'])
        return reverse('tracker:workout_detail', kwargs={'pk': exercise.workout.id})
