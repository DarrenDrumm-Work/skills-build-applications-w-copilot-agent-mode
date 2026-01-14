from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from octofit_tracker import settings

from django.db import connection

# Define models for demonstration if not already present
from django.apps import apps

User = get_user_model()

# Define Team, Activity, Leaderboard, Workout models if not present
if not apps.is_installed('octofit_tracker'):
    class Team(models.Model):
        name = models.CharField(max_length=100, unique=True)
        class Meta:
            app_label = 'octofit_tracker'

    class Activity(models.Model):
        user = models.CharField(max_length=100)
        activity_type = models.CharField(max_length=100)
        duration = models.IntegerField()
        team = models.CharField(max_length=100)
        class Meta:
            app_label = 'octofit_tracker'

    class Leaderboard(models.Model):
        team = models.CharField(max_length=100)
        points = models.IntegerField()
        class Meta:
            app_label = 'octofit_tracker'

    class Workout(models.Model):
        name = models.CharField(max_length=100)
        description = models.TextField()
        suggested_for = models.CharField(max_length=100)
        class Meta:
            app_label = 'octofit_tracker'
else:
    Team = apps.get_model('octofit_tracker', 'Team')
    Activity = apps.get_model('octofit_tracker', 'Activity')
    Leaderboard = apps.get_model('octofit_tracker', 'Leaderboard')
    Workout = apps.get_model('octofit_tracker', 'Workout')

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete all data
        User.objects.all().delete()
        if Team:
            Team.objects.all().delete()
        if Activity:
            Activity.objects.all().delete()
        if Leaderboard:
            Leaderboard.objects.all().delete()
        if Workout:
            Workout.objects.all().delete()

        # Create Teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')


        # Create Users (super heroes)
        users = [
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'team': marvel},
            {'username': 'captainamerica', 'email': 'cap@marvel.com', 'team': marvel},
            {'username': 'batman', 'email': 'batman@dc.com', 'team': dc},
            {'username': 'superman', 'email': 'superman@dc.com', 'team': dc},
        ]
        user_objs = {}
        for u in users:
            user = User.objects.create_user(username=u['username'], email=u['email'], password='password')
            user.profile.team = u['team']
            user.profile.save()
            user_objs[u['username']] = user

        # Create Activities using User and Team instances
        Activity.objects.create(user=user_objs['ironman'], activity_type='Running', duration=30, team=marvel)
        Activity.objects.create(user=user_objs['batman'], activity_type='Cycling', duration=45, team=dc)

        # Create Leaderboard using Team instances
        Leaderboard.objects.create(team=marvel, points=100)
        Leaderboard.objects.create(team=dc, points=80)

        # Create Workouts
        Workout.objects.create(name='Hero HIIT', description='High intensity for heroes', suggested_for='Marvel')
        Workout.objects.create(name='Super Strength', description='Strength training for super heroes', suggested_for='DC')

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
