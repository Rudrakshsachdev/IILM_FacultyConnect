# faculty/urls.py
from django.contrib import admin
from django.urls import path
from accounts import views  

# URL patterns for the faculty portal application
urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # ✅ handles empty path

    path('dashboard/', views.dashboard, name='dashboard'),  # ✅ handles empty path

    path('admin/', admin.site.urls),

    path('signup/', views.signup, name='signup'),

    path('verify-otp/', views.verify_otp, name='verify_otp'),

    path('login/', views.login_view, name='login'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),

    # Password reset URLs
    path('reset-password/', views.reset_password_request, name='reset_password'),

    path('verify-reset-otp/', views.verify_reset_otp, name='verify_reset_otp'),

    path('profile-completion/', views.profile_completion, name='profile_completion'),

    path('save-step/<str:step>/', views.save_step, name='save_step'),

    path('journal-publication/', views.journal_publication, name='journal_publication'),

    path('cluster-head/dashboard/', views.cluster_head_dashboard, name='cluster_head_dashboard'),

    path('cluster-head/review-journal/<int:submission_id>/', views.review_submission_journal, name='review_submission_journal'),

    path('my-submissions/', views.my_submissions, name='my_submissions'),

    path('dean-dashboard/', views.dean_dashboard, name='dean_dashboard'),

    path('dean-review-journal/<int:pk>/', views.dean_review_journal, name='dean_review_journal'),

    path('research-form/', views.research_form, name='research_form'),

    path('conference-publication/', views.conference_publication, name='conference_publication'),

    path('cluster-head/review-conference/<int:submission_id>/', views.review_submission_conference, name='review_submission_conference'),

    path('dean-review-conference/<int:pk>/', views.dean_review_conference, name='dean_review_conference'),

    path('research-project/', views.research_project, name='research_project'),
]
