from django.contrib import admin
from .models import Team, Activity, Leaderboard, Workout, UserProfile

admin.site.register(Team)
admin.site.register(Activity)
admin.site.register(Leaderboard)
admin.site.register(Workout)
admin.site.register(UserProfile)
