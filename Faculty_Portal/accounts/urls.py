# faculty/urls.py
from django.contrib import admin
from django.urls import path
from accounts import views  


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
    path('cluster-head/review/<int:submission_id>/', views.review_submission, name='review_submission'),
]
