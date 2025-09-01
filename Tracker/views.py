import json

from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.timezone import make_aware, now
from django.views import View
from django.views.generic import (
    CreateView, ListView, UpdateView, DeleteView, TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime

from Tracker.forms import WorkoutForm, ExerciseForm, SetForm, WorkoutEventForm
from Tracker.models import Workout, Exercise, Set, WorkoutEvent


class HomeView(TemplateView):
    """Главная страница"""
    template_name = "tracker/landing.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("tracker:menu")
        return super().dispatch(request, *args, **kwargs)


class WorkoutListView(LoginRequiredMixin, ListView):
    """Список тренировок пользователя"""
    model = Workout
    template_name = "tracker/workout_list.html"
    context_object_name = "workouts"
    paginate_by = 10

    def get_queryset(self):
        queryset = Workout.objects.filter(user=self.request.user).order_by("-date")
        comment = self.request.GET.get("comment")
        if comment:
            queryset = queryset.search_comment(comment)
        return queryset


class WorkoutCreateView(LoginRequiredMixin, CreateView):
    """Создание тренировки"""
    form_class = WorkoutForm
    template_name = "tracker/workout_form.html"
    success_url = reverse_lazy("tracker:workout_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class WorkoutUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление тренировки"""
    model = Workout
    template_name = "tracker/workout_update.html"
    form_class = WorkoutForm
    success_url = reverse_lazy("tracker:workout_list")

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)


class WorkoutDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление тренировки"""
    model = Workout
    template_name = "tracker/workout_confirm_delete.html"
    success_url = reverse_lazy("tracker:workout_list")

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)


class ExerciseListView(LoginRequiredMixin, ListView):
    """Список упражнений для тренировки пользователя"""
    model = Exercise
    template_name = "tracker/exercise_list.html"
    context_object_name = "exercises"
    paginate_by = 10

    def get_queryset(self):
        workout = get_object_or_404(Workout, id=self.kwargs["workout_id"], user=self.request.user)
        self._workout = workout
        return workout.exercises.order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["workout"] = getattr(self, "_workout", None)
        return context


class ExerciseCreateView(LoginRequiredMixin, CreateView):
    """Создание упражнения"""
    form_class = ExerciseForm
    template_name = "tracker/exercise_form.html"

    def form_valid(self, form):
        workout = get_object_or_404(Workout, pk=self.kwargs["workout_id"], user=self.request.user)
        form.instance.workout = workout
        self.object = form.save()
        return redirect("tracker:exercise_list", workout_id=workout.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["workout"] = get_object_or_404(Workout, pk=self.kwargs["workout_id"], user=self.request.user)
        return context


class ExerciseUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление упражнений"""
    model = Exercise
    form_class = ExerciseForm
    template_name = "tracker/exercise_update.html"

    def get_queryset(self):
        return Exercise.objects.filter(workout__user=self.request.user, workout_id=self.kwargs["workout_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["workout"] = self.object.workout
        return context

    def get_success_url(self):
        return reverse_lazy("tracker:exercise_list", kwargs={"workout_id": self.object.workout.id})


class ExerciseDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление упражнения"""
    model = Exercise
    template_name = "tracker/exercise_confirm_delete.html"

    def get_queryset(self):
        return Exercise.objects.filter(workout__user=self.request.user, workout_id=self.kwargs["workout_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["workout"] = self.object.workout
        return context

    def get_success_url(self):
        return reverse_lazy("tracker:exercise_list", kwargs={"workout_id": self.object.workout.id})


class SetCreateView(LoginRequiredMixin, CreateView):
    """Создание подхода"""
    form_class = SetForm
    template_name = "tracker/set_form.html"

    def form_valid(self, form):
        exercise = get_object_or_404(Exercise, pk=self.kwargs["exercise_id"], workout__user=self.request.user)
        form.instance.exercise = exercise
        return super().form_valid(form)

    def get_success_url(self):
        exercise = Exercise.objects.select_related("workout").get(id=self.kwargs["exercise_id"])
        return reverse("tracker:exercise_list", kwargs={"workout_id": exercise.workout.id})


class ExerciseSetsView(LoginRequiredMixin, TemplateView):
    """Подходи"""
    template_name = "tracker/exercise_sets.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exercise = get_object_or_404(
            Exercise,
            id=self.kwargs["pk"],
            workout__user=self.request.user,
        )

        sets = exercise.sets.order_by("-id")

        context["exercise"] = exercise
        context["sets"] = sets
        return context


class SetDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление подхода"""
    model = Set
    template_name = "tracker/set_confirm_delete.html"
    pk_url_kwarg = "set_id"

    def get_queryset(self):
        return Set.objects.filter(exercise__workout__user=self.request.user)

    def get_success_url(self):
        exercise_id = self.object.exercise.id
        return reverse("tracker:exercise_sets", kwargs={"pk": exercise_id})


class SetUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление подхода"""
    model = Set
    form_class = SetForm
    template_name = "tracker/set_update.html"
    pk_url_kwarg = "set_id"

    def get_queryset(self):
        return Set.objects.filter(exercise__workout__user=self.request.user)

    def get_success_url(self):
        return reverse("tracker:exercise_sets", kwargs={"pk": self.object.exercise.id})


class MenuView(LoginRequiredMixin, TemplateView):
    """Меню с кнопками"""
    template_name = "tracker/menu.html"


class WorkoutEventsJsonView(LoginRequiredMixin, View):
    """Отдаём тренировки пользователя в формате JSON для FullCalendar (только в нужном диапазоне)"""

    def get(self, request, *args, **kwargs):
        start = request.GET.get("start")
        end = request.GET.get("end")

        qs = WorkoutEvent.objects.filter(user=request.user)
        if start and end:
            # FullCalendar отдаёт ISO-строки → приводим к datetime
            try:
                start_dt = make_aware(datetime.fromisoformat(start))
                end_dt = make_aware(datetime.fromisoformat(end))
                qs = qs.filter(start__range=[start_dt, end_dt])
            except Exception:
                pass

        data = [
            {
                "id": event.id,
                "title": event.title,
                "start": event.start.isoformat(),
                "status": event.status,
            }
            for event in qs
        ]
        return JsonResponse(data, safe=False)


class CalendarView(LoginRequiredMixin, TemplateView):
    """Страница с календарём"""
    template_name = "tracker/calendar.html"


class WorkoutEventCreateView(LoginRequiredMixin, CreateView):
    """Создание тренировки"""
    model = WorkoutEvent
    form_class = WorkoutEventForm
    template_name = "tracker/event_form.html"
    success_url = reverse_lazy("tracker:calendar")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class WorkoutEventUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование тренировки"""
    model = WorkoutEvent
    form_class = WorkoutEventForm
    template_name = "tracker/event_update.html"

    def get_queryset(self):
        return WorkoutEvent.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse("tracker:calendar")


class WorkoutEventDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление тренировки"""
    model = WorkoutEvent
    template_name = "tracker/event_confirm_delete.html"
    success_url = reverse_lazy("tracker:calendar")

    def get_queryset(self):
        return WorkoutEvent.objects.filter(user=self.request.user)


class UpcomingWorkoutsJsonView(LoginRequiredMixin, View):
    """Отдаём только будущие тренировки"""

    def get(self, request, *args, **kwargs):
        events = (
            WorkoutEvent.objects
            .filter(user=request.user, start__gte=now().date())
            .order_by("start")[:5]
        )
        data = [
            {
                "id": e.id,
                "title": e.title,
                "start": e.start.isoformat(),
                "status": e.status,
            }
            for e in events
        ]
        return JsonResponse(data, safe=False)


class WorkoutEventStatusUpdateView(LoginRequiredMixin, View):
    """Смена статуса тренировки (AJAX)"""

    def post(self, request, pk, *args, **kwargs):
        try:
            event = WorkoutEvent.objects.get(pk=pk, user=request.user)
        except WorkoutEvent.DoesNotExist:
            return JsonResponse({"error": "not found"}, status=404)

        try:
            data = json.loads(request.body.decode("utf-8"))
        except Exception:
            return JsonResponse({"error": "invalid json"}, status=400)

        status = data.get("status")
        if status not in dict(WorkoutEvent.STATUS_CHOICES):
            return JsonResponse({"error": "invalid status"}, status=400)

        event.status = status
        event.save(update_fields=["status"])
        return JsonResponse({"success": True, "status": event.status})
