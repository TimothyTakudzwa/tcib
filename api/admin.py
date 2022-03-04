from django.contrib import admin
from .models import Participant, User

# Register your models here.
@admin.register(Participant)
class ParticipantAdminAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Participant._meta.fields]

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [f.name for f in User._meta.fields]