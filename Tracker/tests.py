from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from Tracker.models import Workout


User = get_user_model()


class WorkoutListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        # создаём одну тренировку
        Workout.objects.create(user=self.user, date="2025-01-01")

    def test_view_returns_200_for_logged_in_user(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("tracker:workout_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("workouts", response.context)
