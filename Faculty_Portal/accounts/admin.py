from django.contrib import admin
from .models import FacultyUser, FacultyProfile, JournalPublication,ConferencePublication, ResearchProject, Copyright, Patents, PhdGuidance, BookChapter, BooksAuthored, ConsultancyProjects, EditorialRoles, ReviewerRoles, AwardsAchievements

# Register your models here.

admin.site.register(FacultyUser)
admin.site.register(FacultyProfile)
admin.site.register(JournalPublication)
admin.site.register(ConferencePublication)
admin.site.register(ResearchProject)
admin.site.register(Patents)
admin.site.register(Copyright)
admin.site.register(PhdGuidance)
admin.site.register(BookChapter)
admin.site.register(BooksAuthored)
admin.site.register(ConsultancyProjects)
admin.site.register(EditorialRoles)
admin.site.register(ReviewerRoles)
admin.site.register(AwardsAchievements)