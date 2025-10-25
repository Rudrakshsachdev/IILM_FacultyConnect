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

    path('cluster-head/review-research/<int:submission_id>/', views.review_submission_research, name='review_submission_research'),

    path('dean-review-research/<int:pk>/', views.dean_review_research, name='dean_review_research'),

    path('patent-submission/', views.patent_submission, name='patent_submission'),

    path('cluster-head/review-patent/<int:submission_id>/', views.review_submission_patent, name='review_submission_patent'),

    path('dean-review-patent/<int:pk>/', views.dean_review_patent, name='dean_review_patent'),

    path('copyright-submission/', views.copyright_submission, name='copyright_submission'),

    path('cluster-head/review-copyright/<int:submission_id>/', views.review_submission_copyright, name='review_submission_copyright'),

    path('dean-review-copyright/<int:pk>/', views.dean_review_copyright, name='dean_review_copyright'),

    path('phd-guidance-submission/', views.phd_guidance_submission, name='phd_guidance_submission'),

    path('cluster-head/review-phd-guidance/<int:submission_id>/', views.review_submission_phd_guidance, name='review_submission_phd_guidance'),

    path('dean-review-phd-guidance/<int:pk>/', views.dean_review_phd_guidance, name='dean_review_phd_guidance'),

    path('book-chapter-submission/', views.book_chapter_submission, name='book_chapter_submission'),

    path('cluster-head/review-book-chapter/<int:submission_id>/', views.review_submission_book_chapter, name='review_submission_book_chapter'),

    path('dean-review-book-chapter/<int:pk>/', views.dean_review_book_chapter, name='dean_review_book_chapter'),

    path('books-authored-submission/', views.books_authored_submission, name='books_authored_submission'),

    path('cluster-head/review-books-authored/<int:submission_id>/', views.review_submission_books_authored, name='review_submission_books_authored'),

    path('dean-review-books-authored/<int:pk>/', views.dean_review_books_authored, name='dean_review_books_authored'),

    path('consultancy-project/', views.consultancy_project, name='consultancy_project'),

    path('cluster-head/review-consultancy-project/<int:submission_id>/', views.review_submission_consultancy_project, name='review_submission_consultancy_project'),

    path('dean-review-consultancy-project/<int:pk>/', views.dean_review_consultancy_project, name='dean_review_consultancy_project'),
]
