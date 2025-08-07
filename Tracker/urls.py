from django.urls import path
from .views import (
    HomeView,
    WorkoutListView,
    WorkoutCreateView,
    WorkoutDetailView,
    WorkoutUpdateView,
    WorkoutDeleteView,
    ExerciseCreateView,
    SetCreateView
)

app_name = 'Tracker'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    # Workout routes
    path('workouts/', WorkoutListView.as_view(), name='workout_list'),
    path('workouts/create/', WorkoutCreateView.as_view(), name='workout_create'),
    path('workouts/<int:pk>/', WorkoutDetailView.as_view(), name='workout_detail'),
    path('workouts/<int:pk>/update/', WorkoutUpdateView.as_view(), name='workout_update'),
    path('workouts/<int:pk>/delete/', WorkoutDeleteView.as_view(), name='workout_delete'),

    # Exercise routes
    path('workouts/<int:workout_id>/exercises/create/', ExerciseCreateView.as_view(), name='exercise_create'),

    # Set routes
    path('exercises/<int:exercise_id>/sets/create/', SetCreateView.as_view(), name='set_create'),
]