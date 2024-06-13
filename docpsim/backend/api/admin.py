from django.contrib import admin
from .models import Games, Teams, TeamMembers, Checkpoints, Unlocked, Comments, Achievements

admin.site.register(Games)
admin.site.register(Teams)
admin.site.register(TeamMembers)
admin.site.register(Checkpoints)
admin.site.register(Unlocked)
admin.site.register(Comments)
admin.site.register(Achievements)
