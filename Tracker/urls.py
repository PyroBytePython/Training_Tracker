from django.urls import path
from .views import (
    MenuView,
    WorkoutListView,
    WorkoutCreateView,
    WorkoutUpdateView,
    WorkoutDeleteView,
    ExerciseCreateView,
    SetCreateView, ExerciseListView, ExerciseUpdateView, ExerciseDeleteView, ExerciseSetsView, SetDeleteView,
    SetUpdateView, CalendarView, WorkoutEventsJsonView, WorkoutEventCreateView, WorkoutEventUpdateView,
    WorkoutEventDeleteView, UpcomingWorkoutsJsonView, WorkoutEventStatusUpdateView
)

app_name = 'tracker'

urlpatterns = [
    path('', MenuView.as_view(), name='menu'),

    # Workout routes
    path('workouts/', WorkoutListView.as_view(), name='workout_list'),
    path('workouts/create/', WorkoutCreateView.as_view(), name='workout_create'),
    path('workouts/<int:pk>/update/', WorkoutUpdateView.as_view(), name='workout_update'),
    path('workouts/<int:pk>/delete/', WorkoutDeleteView.as_view(), name='workout_delete'),

    # Exercise routes
    path('workouts/<int:workout_id>/exercises/create/', ExerciseCreateView.as_view(), name='exercise_create'),
    path('workouts/<int:workout_id>/exercises/', ExerciseListView.as_view(), name='exercise_list'),
    path('workouts/<int:workout_id>/exercises/<int:pk>/update/', ExerciseUpdateView.as_view(), name='exercise_update'),
    path('workouts/<int:workout_id>/exercises/<int:pk>/delete/', ExerciseDeleteView.as_view(), name='exercise_delete'),

    # Set routes
    path('exercises/<int:exercise_id>/sets/create/', SetCreateView.as_view(), name='set_create'),
    path('exercise/<int:pk>/sets/', ExerciseSetsView.as_view(), name='exercise_sets'),
    path('sets/<int:set_id>/delete/', SetDeleteView.as_view(), name='set_delete'),
    path('sets/<int:set_id>/edit/', SetUpdateView.as_view(), name='set_edit'),

    # Events routes
    path("calendar/", CalendarView.as_view(), name="calendar"),
    path("calendar/events/", WorkoutEventsJsonView.as_view(), name="calendar-events"),
    path("calendar/upcoming/", UpcomingWorkoutsJsonView.as_view(), name="calendar-upcoming"),
    path("calendar/add/", WorkoutEventCreateView.as_view(), name="calendar-add"),
    path("calendar/<int:pk>/edit/", WorkoutEventUpdateView.as_view(), name="calendar-edit"),
    path("calendar/<int:pk>/delete/", WorkoutEventDeleteView.as_view(), name="calendar-delete"),
    path("calendar/<int:pk>/status/", WorkoutEventStatusUpdateView.as_view(), name="calendar-status", )
]
