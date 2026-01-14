from django.test import TestCase
from django.contrib.auth.models import User
from .models import Team, Activity, Leaderboard, Workout, UserProfile

class BasicModelTests(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name='Test Team')
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = UserProfile.objects.get(user=self.user)
        self.profile.team = self.team
        self.profile.save()
        self.activity = Activity.objects.create(user=self.user, activity_type='Run', duration=10, team=self.team)
        self.leaderboard = Leaderboard.objects.create(team=self.team, points=50)
        self.workout = Workout.objects.create(name='Test Workout', description='desc', suggested_for='Test')

    def test_team(self):
        self.assertEqual(self.team.name, 'Test Team')

    def test_user_profile(self):
        self.assertEqual(self.profile.team, self.team)

    def test_activity(self):
        self.assertEqual(self.activity.user, self.user)

    def test_leaderboard(self):
        self.assertEqual(self.leaderboard.team, self.team)

    def test_workout(self):
        self.assertEqual(self.workout.name, 'Test Workout')
