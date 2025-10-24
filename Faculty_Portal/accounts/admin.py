from django.contrib import admin
from .models import FacultyUser, FacultyProfile, JournalPublication,ConferencePublication, ResearchProject

# Register your models here.

admin.site.register(FacultyUser)
admin.site.register(FacultyProfile)
admin.site.register(JournalPublication)
admin.site.register(ConferencePublication)
admin.site.register(ResearchProject)