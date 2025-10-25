# faculty/views.py
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import FacultyUser, FacultyProfile, JournalPublication, ConferencePublication, ResearchProject, Patents, Copyright, PhdGuidance, BookChapter, BooksAuthored, ConsultancyProjects, EditorialRoles
from .forms import Step1Form, Step2Form, Step3Form, JournalPublicationForm, ConferencePublicationForm, ResearchProjectForm, PatentForm, CopyrightForm, PhdGuidanceForm, BookChapterForm, BooksAuthoredForm, ConsultancyProjectsForm, EditorialRolesForm
import random
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from itertools import chain



otp_storage = {}  # Temporary dictionary to hold OTPs (use Redis in production)

def signup(request):

    """
    In the signup function, when a user submits the signup form, it collects their full name, email, and password, then checks if the email is already registered and whether the passwords match. If valid, it generates a 6-digit OTP using Python’s random.randint() and stores it temporarily in a dictionary called otp_storage (which acts like a cache). The OTP is then emailed to the user using Django’s send_mail() function. Meanwhile, the user’s information (except OTP) is stored in the session as temp_user so it can be retrieved later for verification. After sending the OTP, the user is redirected to the OTP verification page.
    """

    if request.method == "POST":
        full_name = request.POST['full_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if FacultyUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('signup')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        # Generate OTP
        otp = str(random.randint(100000, 999999))
        otp_storage[email] = otp

        # Send OTP via email
        send_mail(
            subject='Faculty Portal Verification Code',
            message=f'Your verification code is: {otp}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )

        # Temporarily store user data (can use session)
        request.session['temp_user'] = {
            'full_name': full_name,
            'email': email,
            'password': password,
        }

        return redirect('verify_otp')

    return render(request, 'Signup.html')


def verify_otp(request):

    """
    In the verify_otp function, when the user submits the OTP form, the entered OTP is compared with the one stored in otp_storage. If they match, a new FacultyUser record is created with the user’s details, marking the account as verified (is_verified=True). The temporary OTP and session data are then deleted, and a success message is shown before redirecting the user to the login page. If the OTP is incorrect or the session has expired, appropriate error messages are displayed, prompting the user to retry.
    """


    if request.method == "POST":
        entered_otp = request.POST['otp']
        temp_user = request.session.get('temp_user')

        if not temp_user:
            messages.error(request, "Session expired. Please sign up again.")
            return redirect('signup')

        email = temp_user['email']
        if otp_storage.get(email) == entered_otp:
            FacultyUser.objects.create(
                full_name=temp_user['full_name'],
                email=email,
                password=temp_user['password'],
                is_verified=True
            )
            del otp_storage[email]
            del request.session['temp_user']
            messages.success(request, "Account verified successfully!")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('verify_otp')

    return render(request, 'Verify_otp.html')


def login_view(request):

    """
    In the login_view function, when a POST request is made (i.e., the user submits the login form), it retrieves the entered email and password. It then tries to find a matching user in the FacultyUser model using the provided email. If the email doesn’t exist, an error message is shown. If the user exists but hasn’t verified their email yet (is_verified is False), the user is prompted to verify it first. Otherwise, the entered password is checked against the stored one — either directly or using Django’s check_password() for hashed passwords. If the password matches, the user’s ID is stored in the session (request.session['user_id']), effectively logging them in, and they are redirected to the dashboard with a success message. If the password doesn’t match, an “Invalid password” error appears. If the request method is not POST, the login page is simply rendered.
    """

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = FacultyUser.objects.get(email=email)
            if not user.is_verified:
                messages.error(request, "Please verify your email first!")
                return redirect('login')

            if user.password == password or check_password(password, user.password):
                request.session['user_id'] = str(user.user_id)
                messages.success(request, "Login successful!")

                

                return redirect('dashboard')
            else:
                messages.error(request, "Invalid password.")
                return redirect('login')
        except FacultyUser.DoesNotExist:
            messages.error(request, "Email not registered.")
            return redirect('login')

    return render(request, 'login.html')





def logout_view(request):

    """
    The logout_view function is simpler — it checks if there’s an active session containing user_id, and if so, deletes it to log the user out. Afterward, a success message is displayed, and the user is redirected back to the login page.
    """

    if 'user_id' in request.session:
        del request.session['user_id']
    messages.success(request, "Logged out successfully!")
    return redirect('login')


def dashboard(request):


    """
    The dashboard function first checks whether the user is logged in by verifying the presence of 'user_id' in the session. If not, it redirects to the login page. Once verified, it retrieves the logged-in user’s data from the FacultyUser model and fetches their associated profile from the FacultyProfile model. To enhance user experience, it calculates the profile completion percentage by checking how many profile fields (such as department, designation, or ORCID ID) are filled out of the total available. This completion percentage, along with user and profile details, is then passed to the dashboard.html template for rendering.
    """

    # ✅ Check if user is logged in
    if 'user_id' not in request.session:
        return redirect('login')

    # ✅ Fetch user and related profile
    user = FacultyUser.objects.get(user_id=request.session['user_id'])
    profile = FacultyProfile.objects.filter(user=user).first()

    # ✅ Calculate profile completion percentage
    if profile:
        fields = [
            profile.profile_image, profile.school_faculty, profile.department,
            profile.designation, profile.highest_qualification, profile.area_of_specialization,
            profile.orcid_id, profile.scopus_id, profile.google_scholar, profile.vidwaan_id
        ]
        filled_fields = sum(1 for f in fields if f)
        total_fields = len(fields)
        profile_completion = int((filled_fields / total_fields) * 100)
    else:
        profile_completion = 0

    # ✅ Render the dashboard template
    return render(request, 'dashboard.html', {
        'user': user,
        'profile': profile,
        'profile_completion': profile_completion
    })


reset_otp_storage = {}  # Store OTPs temporarily (use Redis in production)

def reset_password_request(request):


    """
    The reset_password_request function handles the first step of the password recovery process. When the user submits their registered email, it checks if that email exists in the FacultyUser model. If it does, a 6-digit OTP is generated using random.randint() and temporarily stored in the reset_otp_storage dictionary (a placeholder for caching, ideally replaced with Redis in production). This OTP is then sent to the user’s email using Django’s send_mail() function. The email address is also saved in the session (reset_email) for later verification, and a success message is shown before redirecting the user to the OTP verification page. If the email isn’t registered, an error message is displayed.
    """

    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = FacultyUser.objects.get(email=email)
            otp = str(random.randint(100000, 999999))
            reset_otp_storage[email] = otp

            # Send OTP to email
            send_mail(
                subject='Password Reset OTP',
                message=f'Your password reset OTP is: {otp}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False
            )

            request.session['reset_email'] = email
            messages.success(request, 'OTP sent to your email.')
            return redirect('verify_reset_otp')
        except FacultyUser.DoesNotExist:
            messages.error(request, 'Email not registered.')
    return render(request, 'reset_password.html')


def verify_reset_otp(request):


    """
    The verify_reset_otp function verifies the OTP entered by a user during password recovery. It retrieves the stored OTP using the email from the session and checks its validity. If valid and the new password fields match, it updates the user’s password in the database, removes temporary data, and redirects to the login page with a success message. If the OTP is incorrect, the passwords don’t match, or the session has expired, appropriate error messages are displayed, prompting the user to retry.
    """

    if request.method == 'POST':
        email = request.session.get('reset_email')
        entered_otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not email:
            messages.error(request, 'Session expired. Try again.')
            return redirect('reset_password')

        if reset_otp_storage.get(email) != entered_otp:
            messages.error(request, 'Invalid OTP. Try again.')
            return redirect('verify_reset_otp')

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('verify_reset_otp')

        # Update password
        user = FacultyUser.objects.get(email=email)
        user.password = new_password
        user.save()

        del reset_otp_storage[email]
        del request.session['reset_email']

        messages.success(request, 'Password reset successful! You can now log in.')
        return redirect('login')

    return render(request, 'verify_reset_otp.html')


def profile_completion(request):


    """
    The profile_completion function ensures a logged-in user can complete their profile in multiple steps. It retrieves or creates a FacultyProfile linked to the user, loads three form sections (Step1Form, Step2Form, and Step3Form), and passes them to the profile_completion.html page. This allows users to fill out their profile information in a structured manner.
    """

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = FacultyUser.objects.get(user_id=user_id)
    profile, created = FacultyProfile.objects.get_or_create(user=user)

    step1_form = Step1Form(instance=profile)
    step2_form = Step2Form(instance=profile)
    step3_form = Step3Form(instance=profile)

    return render(request, 'profile_completion.html', {
        'step1_form': step1_form,
        'step2_form': step2_form,
        'step3_form': step3_form,
    })


def save_step(request, step):


    """
    The save_step function saves data from each step of the profile completion form. Depending on which step is being saved (1, 2, or 3), it processes the corresponding form. If the form data is valid, it saves the progress. Once the third step is completed, the user’s is_first_login flag is set to False, indicating the profile is complete. Responses are sent as JSON objects to support asynchronous updates (AJAX).
    """


    user_id = request.session.get('user_id')
    user = FacultyUser.objects.get(user_id=user_id)
    profile, created = FacultyProfile.objects.get_or_create(user=user)

    if step == '1':
        form = Step1Form(request.POST, request.FILES, instance=profile)
    elif step == '2':
        form = Step2Form(request.POST, instance=profile)
    elif step == '3':
        form = Step3Form(request.POST, instance=profile)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid step'})

    if form.is_valid():
        form.save()
        if step == '3':
            user.is_first_login = False
            user.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors})


def journal_publication(request):
    

    """
    The journal_publication function allows logged-in users to submit details about their journal publications. It checks for user authentication, processes the submitted form data, and saves a new JournalPublication record linked to the user. Upon successful submission, a success message is displayed, and the user is redirected to the dashboard. If there are form errors, they are communicated back to the user for correction."""

    if 'user_id' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        form = JournalPublicationForm(request.POST, request.FILES)
        if form.is_valid():
            publication = form.save(commit=False)
            user = FacultyUser.objects.get(user_id=request.session['user_id'])
            publication.user = user
            publication.save()
            messages.success(request, "Journal publication submitted successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = JournalPublicationForm()

    return render(request, 'journal_publication_form.html', {'form': form})



def cluster_head_dashboard(request):


    """
    The cluster_head_dashboard function displays all journal publication submissions that are pending or need review by the cluster head. It retrieves these submissions from the database and renders them in the cluster_head_dashboard.html template.
    """
    journal_publications = JournalPublication.objects.filter(status='submitted').order_by('-submitted_at')

    conference_publications = ConferencePublication.objects.filter(status='submitted').order_by('-submitted_at')

    research_projects = ResearchProject.objects.filter(overall_status='submitted').order_by('-submitted_at')

    patent_submissions = Patents.objects.filter(status='submitted').order_by('-submitted_at')

    copyright_submissions = Copyright.objects.filter(status='submitted').order_by('-submitted_at')

    phd_guidance_submissions = PhdGuidance.objects.filter(status='submitted').order_by('-submitted_at')

    book_chapter_submissions = BookChapter.objects.filter(status='submitted').order_by('-submitted_at')

    books_authored_submissions = BooksAuthored.objects.filter(status='submitted').order_by('-submitted_at')

    consultancy_projects_submissions = ConsultancyProjects.objects.filter(status='submitted').order_by('-submitted_at')

    editorial_roles_submissions = EditorialRoles.objects.filter(status='submitted').order_by('-submitted_at')

    for sub in journal_publications:
        sub.submission_type = 'Journal Publication'
        sub.review_url = reverse('review_submission_journal', args=[sub.id])
    
    for sub in conference_publications:
        sub.submission_type = 'Conference Publication'
        sub.review_url = reverse('review_submission_conference', args=[sub.id])
    
    for sub in research_projects:
        sub.submission_type = 'Research Project'
        sub.review_url = reverse('review_submission_research', args=[sub.id])

    for sub in patent_submissions:
        sub.submission_type = 'Patent Submission'
        sub.review_url = reverse('review_submission_patent', args=[sub.id])
    
    for sub in copyright_submissions:
        sub.submission_type = 'Copyright Submission'
        sub.review_url = reverse('review_submission_copyright', args=[sub.id])
    
    for sub in phd_guidance_submissions:
        sub.submission_type = 'PhD Guidance'
        sub.review_url = reverse('review_submission_phd_guidance', args=[sub.id])
    
    for sub in book_chapter_submissions:
        sub.submission_type = 'Book Chapter'
        sub.review_url = reverse('review_submission_book_chapter', args=[sub.id])
    
    for sub in books_authored_submissions:
        sub.submission_type = 'Books Authored'
        sub.review_url = reverse('review_submission_books_authored', args=[sub.id])
    
    for sub in consultancy_projects_submissions:
        sub.submission_type = 'Consultancy Project'
        sub.review_url = reverse('review_submission_consultancy_project', args=[sub.id])
    
    for sub in editorial_roles_submissions:
        sub.submission_type = 'Editorial Roles'
        sub.review_url = reverse('review_submission_editorial_roles', args=[sub.id])

    all_submissions = sorted(
        list(journal_publications) + list(conference_publications) + list(research_projects) + list(patent_submissions) + list(copyright_submissions) + list(phd_guidance_submissions) + list(book_chapter_submissions) + list(books_authored_submissions) + list(consultancy_projects_submissions) + list(editorial_roles_submissions),
        key=lambda x: x.submitted_at,
        reverse=True
    )
    return render(request, 'cluster_head_dashboard.html', {'submissions': all_submissions})



def review_submission_journal(request, submission_id):


    """
    The review_submission function allows a cluster head to review individual journal publication submissions. It retrieves the specific submission by its ID and processes the review form submitted by the cluster head. Depending on the selected status (approved, rejected, or revision), it updates the submission’s cluster_head_status and overall status accordingly, along with any remarks provided. After saving the changes, it redirects back to the cluster head dashboard with a success message. If the request method is not POST, it simply renders the review_submission.html template with the submission details.
    """

    submission = get_object_or_404(JournalPublication, id=submission_id)

    if request.method == 'POST':
        status = request.POST.get('status')  # 'approved_by_cluster', 'rejected_by_cluster', 'revision'
        remarks = request.POST.get('remarks')

        if status not in ['approved_by_cluster', 'rejected_by_cluster', 'revision']:
            messages.error(request, 'Invalid status.')
            return redirect('review_submission_journal', submission_id=submission.id)

        # Map status to cluster_head_status
        if status == 'approved_by_cluster':
            submission.cluster_head_status = 'approved'
            submission.status = 'approved_by_cluster'
        elif status == 'rejected_by_cluster':
            submission.cluster_head_status = 'rejected'
            submission.status = 'rejected_by_cluster'
        elif status == 'revision':
            submission.cluster_head_status = 'revision'
            submission.status = 'revision'

        submission.cluster_head_remarks = remarks
        submission.save()

        messages.success(request, f"Submission '{submission.title_of_paper}' reviewed successfully.")
        return redirect('cluster_head_dashboard')

    return render(request, 'review_submission_journal.html', {'submission': submission})



def my_submissions(request):

    """
    The my_submissions function retrieves and displays all journal publication submissions made by the logged-in user. It first checks if the user is authenticated by verifying the presence of 'user_id' in the session. If not authenticated, it redirects to the login page. Once authenticated, it fetches the user’s submissions from the JournalPublication model and renders them in the my_submissions.html template.
    """

    if 'user_id' not in request.session:
        return redirect('login')

    user_uuid = request.session['user_id']
    user = FacultyUser.objects.get(user_id=user_uuid)
    
    journal_submissions = JournalPublication.objects.filter(user=user).order_by('-submitted_at')

    conference_submissions = ConferencePublication.objects.filter(user=user).order_by('-submitted_at')

    research_submissions = ResearchProject.objects.filter(user=user).order_by('-submitted_at')

    patent_submissions = Patents.objects.filter(user=user).order_by('-submitted_at')

    copyright_submissions = Copyright.objects.filter(user=user).order_by('-submitted_at')

    phd_guidance_submissions = PhdGuidance.objects.filter(user=user).order_by('-submitted_at')

    book_chapter_submissions = BookChapter.objects.filter(user=user).order_by('-submitted_at')

    books_authored_submissions = BooksAuthored.objects.filter(user=user).order_by('-submitted_at')

    consultancy_project_submissions = ConsultancyProjects.objects.filter(user=user).order_by('-submitted_at')

    editorial_roles_submissions = EditorialRoles.objects.filter(user=user).order_by('-submitted_at')

    for sub in journal_submissions:
        sub.submission_type = 'Journal Publication'
        
    for sub in conference_submissions:
        sub.submission_type = 'Conference Publication'
        

    for sub in research_submissions:
        sub.submission_type = 'Research Project'
    
    for sub in patent_submissions:
        sub.submission_type = 'Patent Submission'
    
    for sub in copyright_submissions:
        sub.submission_type = 'Copyright Submission'
    
    for sub in phd_guidance_submissions:
        sub.submission_type = 'PhD Guidance'
    
    for sub in book_chapter_submissions:
        sub.submission_type = 'Book Chapter'
    
    for sub in books_authored_submissions:
        sub.submission_type = 'Books Authored'
    
    for sub in consultancy_project_submissions:
        sub.submission_type = 'Consultancy Project'
    
    for sub in editorial_roles_submissions:
        sub.submission_type = 'Editorial Roles'
        

    submissions = sorted(
        chain(journal_submissions, conference_submissions, research_submissions, patent_submissions, copyright_submissions, phd_guidance_submissions, book_chapter_submissions, books_authored_submissions, consultancy_project_submissions, editorial_roles_submissions),
        key=lambda x: x.submitted_at,
        reverse=True
    )

    approved_count = sum(1 for sub in submissions if sub.dean_status == 'approved_by_dean')
    pending_count = sum(1 for sub in submissions if sub.dean_status in ['submitted', 'pending'])

    return render(request, 'my_submissions.html', {'submissions': submissions, 'approved_count': approved_count, 'pending_count': pending_count})


def dean_dashboard(request):

    """
    The dean_dashboard function displays all journal publication submissions that were approved by the cluster head. It retrieves these submissions from the database and renders them in the dean_dashboard.html template.
    """
    journal_submissions = JournalPublication.objects.filter(status='approved_by_cluster').order_by('-submitted_at')

    for sub in journal_submissions:
        sub.review_url = reverse('dean_review_journal', args=[sub.id])
        sub.submission_type = 'Journal Publication'
    
    conference_submissions = ConferencePublication.objects.filter(status='approved_by_cluster').order_by('-submitted_at')

    for sub in conference_submissions:
        sub.review_url = reverse('dean_review_conference', args=[sub.id])
        sub.submission_type = 'Conference Publication'
    
    research_submissions = ResearchProject.objects.filter(overall_status='approved_by_cluster').order_by('-submitted_at')

    for sub in research_submissions:
        sub.review_url = reverse('dean_review_research', args=[sub.id])
        sub.submission_type = 'Research Project'

    patent_submissions = Patents.objects.filter(status='approved_by_cluster').order_by('-submitted_at')

    for sub in patent_submissions:
        sub.review_url = reverse('dean_review_patent', args=[sub.id])
        sub.submission_type = 'Patent Submission'
    
    copyright_submissions = Copyright.objects.filter(status='approved_by_cluster').order_by('-submitted_at')

    for sub in copyright_submissions:
        sub.review_url = reverse('dean_review_copyright', args=[sub.id])
        sub.submission_type = 'Copyright Submission'

    phd_guidance_submissions = PhdGuidance.objects.filter(status='approved_by_cluster').order_by('-submitted_at')

    for sub in phd_guidance_submissions:
        sub.review_url = reverse('dean_review_phd_guidance', args=[sub.id])
        sub.submission_type = 'PhD Guidance'

    book_chapter_submissions = BookChapter.objects.filter(status='approved_by_cluster').order_by('-submitted_at')

    for sub in book_chapter_submissions:
        sub.review_url = reverse('dean_review_book_chapter', args=[sub.id])
        sub.submission_type = 'Book Chapter'

    books_authored_submissions = BooksAuthored.objects.filter(status='approved_by_cluster').order_by('-submitted_at')

    for sub in books_authored_submissions:
        sub.review_url = reverse('dean_review_books_authored', args=[sub.id])
        sub.submission_type = 'Books Authored'

    consultancy_project_submissions = ConsultancyProjects.objects.filter(status='approved_by_cluster').order_by('-submitted_at')

    for sub in consultancy_project_submissions:
        sub.review_url = reverse('dean_review_consultancy_project', args=[sub.id])
        sub.submission_type = 'Consultancy Project'
    

    editorial_roles_submissions = EditorialRoles.objects.filter(status='approved_by_cluster').order_by('-submitted_at')

    for sub in editorial_roles_submissions:
        sub.review_url = reverse('dean_review_editorial_roles', args=[sub.id])
        sub.submission_type = 'Editorial Roles'


    all_submissions = sorted(
        list(journal_submissions) + list(conference_submissions) + list(research_submissions) + list(patent_submissions) + list(copyright_submissions) + list(phd_guidance_submissions) + list(book_chapter_submissions) + list(books_authored_submissions) + list(consultancy_project_submissions) + list(editorial_roles_submissions),
        key=lambda x: x.submitted_at,
        reverse=True
    )

    return render(request, 'dean_dashboard.html', {'submissions': all_submissions})


def dean_review_journal(request, pk):


    """
    The dean_review_journal function allows the dean to review individual journal publication submissions. It retrieves the specific submission by its ID and processes the review form submitted by the dean. Depending on the selected action (approve or reject), it updates the submission’s dean_status and overall status accordingly, along with any remarks provided. After saving the changes, it redirects back to the dean dashboard with a success message. If the request method is not POST, it simply renders the dean_review.html template with the submission details.
    """

    submission = get_object_or_404(JournalPublication, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        remarks = request.POST.get('remarks')

        # Validate and set dean review status
        if action == 'approve':
            submission.dean_status = 'approved'
            submission.status = 'approved_by_dean'
        elif action == 'reject':
            submission.dean_status = 'rejected'
            submission.status = 'rejected_by_dean'
        else:
            messages.error(request, "Invalid action.")
            return redirect('dean_review', pk=pk)

        # Save remarks separately for dean
        submission.dean_remarks = remarks
        submission.save()

        messages.success(request, f"Submission '{submission.title_of_paper}' reviewed by Dean successfully.")
        return redirect('dean_dashboard')

    return render(request, 'dean_review_journal.html', {'submission': submission})

def research_form(request):
    return render(request, 'research_forms.html')

def conference_publication(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        form = ConferencePublicationForm(request.POST, request.FILES)
        if form.is_valid():
            publication = form.save(commit=False)
            user = FacultyUser.objects.get(user_id=request.session['user_id'])
            publication.user = user
            publication.save()
            messages.success(request, "Conference publication submitted successfully.")
            return redirect('my_submissions')
    else:
        form = ConferencePublicationForm()
    return render(request, 'conference_publication.html', {'form': form})


def review_submission_conference(request, submission_id):
    submission = get_object_or_404(ConferencePublication, id=submission_id)

    if request.method == 'POST':
        status = request.POST.get('status')  # 'approved_by_cluster', 'rejected_by_cluster', 'revision'
        remarks = request.POST.get('remarks')

        if status not in ['approved_by_cluster', 'rejected_by_cluster', 'revision']:
            messages.error(request, 'Invalid status.')
            return redirect('review_submission_conference', submission_id=submission.id)

        # Map status to cluster_head_status
        if status == 'approved_by_cluster':
            submission.cluster_head_status = 'approved'
            submission.status = 'approved_by_cluster'
        elif status == 'rejected_by_cluster':
            submission.cluster_head_status = 'rejected'
            submission.status = 'rejected_by_cluster'
        elif status == 'revision':
            submission.cluster_head_status = 'revision'
            submission.status = 'revision'

        submission.cluster_head_remarks = remarks
        submission.save()

        messages.success(request, f"Submission '{submission.title_of_paper}' reviewed successfully.")
        return redirect('cluster_head_dashboard')
    return render(request, 'review_submission_conference.html', {'submission': submission})


def dean_review_conference(request, pk):
    submission = get_object_or_404(ConferencePublication, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        remarks = request.POST.get('remarks')

        # Validate and set dean review status
        if action == 'approve':
            submission.dean_status = 'approved'
            submission.status = 'approved_by_dean'
        elif action == 'reject':
            submission.dean_status = 'rejected'
            submission.status = 'rejected_by_dean'
        else:
            messages.error(request, "Invalid action.")
            return redirect('dean_review_conference', pk=pk)

        # Save remarks separately for dean
        submission.dean_remarks = remarks
        submission.save()

        messages.success(request, f"Submission '{submission.title_of_paper}' reviewed by Dean successfully.")
        return redirect('dean_dashboard')

    return render(request, 'dean_review_conference.html', {'submission': submission})

def research_project(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        form = ResearchProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            user = FacultyUser.objects.get(user_id=request.session['user_id'])
            project.user = user
            project.save()
            messages.success(request, "Research project submitted successfully.")
            return redirect('my_submissions')
    else:
        form = ResearchProjectForm()
    return render(request, 'research_project.html', {'form': form})

def review_submission_research(request, submission_id):
    submission = get_object_or_404(ResearchProject, id=submission_id)

    if request.method == 'POST':
        status = request.POST.get('status')  # 'approved_by_cluster', 'rejected_by_cluster', 'revision'
        remarks = request.POST.get('remarks')

        if status not in ['approved_by_cluster', 'rejected_by_cluster', 'revision']:
            messages.error(request, 'Invalid status.')
            return redirect('review_submission_research', submission_id=submission.id)

        # Map status to cluster_head_status
        if status == 'approved_by_cluster':
            submission.cluster_head_status = 'approved'
            submission.overall_status = 'approved_by_cluster'
        elif status == 'rejected_by_cluster':
            submission.cluster_head_status = 'rejected'
            submission.overall_status = 'rejected_by_cluster'
        elif status == 'revision':
            submission.cluster_head_status = 'revision'
            submission.overall_status = 'revision'

        submission.cluster_head_remarks = remarks
        submission.save()

        messages.success(request, f"Submission '{submission.project_title}' reviewed successfully.")
        return redirect('cluster_head_dashboard')
    return render(request, 'review_submission_research.html', {'submission': submission})

def dean_review_research(request, pk):
    submission = get_object_or_404(ResearchProject, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        remarks = request.POST.get('remarks')

        # Validate and set dean review status
        if action == 'approve':
            submission.dean_status = 'approved'
            submission.overall_status = 'approved_by_dean'
        elif action == 'reject':
            submission.dean_status = 'rejected'
            submission.overall_status = 'rejected_by_dean'
        else:
            messages.error(request, "Invalid action.")
            return redirect('dean_review_research', pk=pk)

        # Save remarks separately for dean
        submission.dean_remarks = remarks
        submission.save()

        messages.success(request, f"Submission '{submission.project_title}' reviewed by Dean successfully.")
        return redirect('dean_dashboard')

    return render(request, 'dean_review_research.html', {'submission': submission})


def patent_submission(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        form = PatentForm(request.POST, request.FILES)
        if form.is_valid():
            patent = form.save(commit=False)
            user = FacultyUser.objects.get(user_id=request.session['user_id'])
            patent.user = user
            patent.save()
            messages.success(request, "Patent submitted successfully.")
            return redirect('my_submissions')
    else:
        form = PatentForm()
    return render(request, 'patent_submission.html', {'form': form})


def review_submission_patent(request, submission_id):
    submission = get_object_or_404(Patents, id=submission_id)

    if request.method == 'POST':
        status = request.POST.get('status')  # 'approved_by_cluster', 'rejected_by_cluster', 'revision'
        remarks = request.POST.get('remarks')

        if status not in ['approved_by_cluster', 'rejected_by_cluster', 'revision']:
            messages.error(request, 'Invalid status.')
            return redirect('review_submission_patent', submission_id=submission.id)

        # Map status to cluster_head_status
        if status == 'approved_by_cluster':
            submission.cluster_head_status = 'approved'
            submission.status = 'approved_by_cluster'
        elif status == 'rejected_by_cluster':
            submission.cluster_head_status = 'rejected'
            submission.status = 'rejected_by_cluster'
        elif status == 'revision':
            submission.cluster_head_status = 'revision'
            submission.status = 'revision'

        submission.cluster_head_remarks = remarks
        submission.save()

        messages.success(request, f"Submission '{submission.title_of_patent}' reviewed successfully.")
        return redirect('cluster_head_dashboard')
    return render(request, 'review_submission_patent.html', {'submission': submission})

def dean_review_patent(request, pk):
    submission = get_object_or_404(Patents, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        remarks = request.POST.get('remarks')

        # Validate and set dean review status
        if action == 'approve':
            submission.dean_status = 'approved'
            submission.status = 'approved_by_dean'
        elif action == 'reject':
            submission.dean_status = 'rejected'
            submission.status = 'rejected_by_dean'
        else:
            messages.error(request, "Invalid action.")
            return redirect('dean_review_patent', pk=pk)

        # Save remarks separately for dean
        submission.dean_remarks = remarks
        submission.save()

        messages.success(request, f"Submission '{submission.title_of_patent}' reviewed by Dean successfully.")
        return redirect('dean_dashboard')

    return render(request, 'dean_review_patent.html', {'submission': submission})


def copyright_submission(request):

    if 'user_id' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        form = CopyrightForm(request.POST, request.FILES)
        if form.is_valid():
            copyright = form.save(commit=False)
            user = FacultyUser.objects.get(user_id=request.session['user_id'])
            copyright.user = user
            copyright.save()
            messages.success(request, "Copyright submitted successfully.")
            return redirect('my_submissions')
    else:
        form = CopyrightForm()
    return render(request, 'copyright_submission.html', {'form': form})


def review_submission_copyright(request, submission_id):
    submission = get_object_or_404(Copyright, id=submission_id)

    if request.method == 'POST':
        status = request.POST.get('status')  # 'approved_by_cluster', 'rejected_by_cluster', 'revision'
        remarks = request.POST.get('remarks')

        if status not in ['approved_by_cluster', 'rejected_by_cluster', 'revision']:
            messages.error(request, 'Invalid status.')
            return redirect('review_submission_copyright', submission_id=submission.id)

        # Map status to cluster_head_status
        if status == 'approved_by_cluster':
            submission.cluster_head_status = 'approved'
            submission.status = 'approved_by_cluster'
        elif status == 'rejected_by_cluster':
            submission.cluster_head_status = 'rejected'
            submission.status = 'rejected_by_cluster'
        elif status == 'revision':
            submission.cluster_head_status = 'revision'
            submission.status = 'revision'

        submission.cluster_head_remarks = remarks
        submission.save()

        messages.success(request, f"Submission '{submission.title_of_work}' reviewed successfully.")
        return redirect('cluster_head_dashboard')
    return render(request, 'review_submission_copyright.html', {'submission': submission})


def dean_review_copyright(request, pk):
    submission = get_object_or_404(Copyright, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        remarks = request.POST.get('remarks')

        # Validate and set dean review status
        if action == 'approve':
            submission.dean_status = 'approved'
            submission.status = 'approved_by_dean'
        elif action == 'reject':
            submission.dean_status = 'rejected'
            submission.status = 'rejected_by_dean'
        else:
            messages.error(request, "Invalid action.")
            return redirect('dean_review_copyright', pk=pk)

        # Save remarks separately for dean
        submission.dean_remarks = remarks
        submission.save()

        messages.success(request, f"Submission '{submission.title_of_work}' reviewed by Dean successfully.")
        return redirect('dean_dashboard')

    return render(request, 'dean_review_copyright.html', {'submission': submission})


def phd_guidance_submission(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        form = PhdGuidanceForm(request.POST, request.FILES)
        if form.is_valid():
            guidance = form.save(commit=False)
            user = FacultyUser.objects.get(user_id=request.session['user_id'])
            guidance.user = user
            guidance.save()
            messages.success(request, "PhD Guidance details submitted successfully.")
            return redirect('my_submissions')
    else:
        form = PhdGuidanceForm()
    return render(request, 'phd_guidance_submission.html', {'form': form})


def review_submission_phd_guidance(request, submission_id):
    submission = get_object_or_404(PhdGuidance, id=submission_id)

    if request.method == 'POST':
        status = request.POST.get('status')  # 'approved_by_cluster', 'rejected_by_cluster', 'revision'
        remarks = request.POST.get('remarks')

        if status not in ['approved_by_cluster', 'rejected_by_cluster', 'revision']:
            messages.error(request, 'Invalid status.')
            return redirect('review_submission_phd_guidance', submission_id=submission.id)

        # Map status to cluster_head_status
        if status == 'approved_by_cluster':
            submission.cluster_head_status = 'approved'
            submission.status = 'approved_by_cluster'
        elif status == 'rejected_by_cluster':
            submission.cluster_head_status = 'rejected'
            submission.status = 'rejected_by_cluster'
        elif status == 'revision':
            submission.cluster_head_status = 'revision'
            submission.status = 'revision'

        submission.cluster_head_remarks = remarks
        submission.save()

        messages.success(request, f"Submission '{submission.thesis_title}' reviewed successfully.")
        return redirect('cluster_head_dashboard')
    return render(request, 'review_submission_phd_guidance.html', {'submission': submission})


def dean_review_phd_guidance(request, pk):
    submission = get_object_or_404(PhdGuidance, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        remarks = request.POST.get('remarks')

        # Validate and set dean review status
        if action == 'approve':
            submission.dean_status = 'approved'
            submission.status = 'approved_by_dean'
        elif action == 'reject':
            submission.dean_status = 'rejected'
            submission.status = 'rejected_by_dean'
        else:
            messages.error(request, "Invalid action.")
            return redirect('dean_review_phd_guidance', pk=pk)

        # Save remarks separately for dean
        submission.dean_remarks = remarks
        submission.save()

        messages.success(request, f"Submission '{submission.thesis_title}' reviewed by Dean successfully.")
        return redirect('dean_dashboard')

    return render(request, 'dean_review_phd_guidance.html', {'submission': submission})


def book_chapter_submission(request):

    if 'user_id' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        form = BookChapterForm(request.POST, request.FILES)
        if form.is_valid():
            book_chapter = form.save(commit=False)
            user = FacultyUser.objects.get(user_id=request.session['user_id'])
            book_chapter.user = user
            book_chapter.save()
            messages.success(request, "Book Chapter submitted successfully.")
            return redirect('my_submissions')
    else:
        form = BookChapterForm()
    return render(request, 'book_chapter_submission.html', {'form': form})



def review_submission_book_chapter(request, submission_id):
    submission = get_object_or_404(BookChapter, id=submission_id)

    if request.method == 'POST':
        status = request.POST.get('status')  # 'approved_by_cluster', 'rejected_by_cluster', 'revision'
        remarks = request.POST.get('remarks')

        if status not in ['approved_by_cluster', 'rejected_by_cluster', 'revision']:
            messages.error(request, 'Invalid status.')
            return redirect('review_submission_book_chapter', submission_id=submission.id)

        # Map status to cluster_head_status
        if status == 'approved_by_cluster':
            submission.cluster_head_status = 'approved'
            submission.status = 'approved_by_cluster'
        elif status == 'rejected_by_cluster':
            submission.cluster_head_status = 'rejected'
            submission.status = 'rejected_by_cluster'
        elif status == 'revision':
            submission.cluster_head_status = 'revision'
            submission.status = 'revision'

        submission.cluster_head_remarks = remarks
        submission.save()

        messages.success(request, f"Submission '{submission.chapter_title}' reviewed successfully.")
        return redirect('cluster_head_dashboard')
    return render(request, 'review_submission_book_chapter.html', {'submission': submission})


def dean_review_book_chapter(request, pk):
    submission = get_object_or_404(BookChapter, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        remarks = request.POST.get('remarks')

        # Validate and set dean review status
        if action == 'approve':
            submission.dean_status = 'approved'
            submission.status = 'approved_by_dean'
        elif action == 'reject':
            submission.dean_status = 'rejected'
            submission.status = 'rejected_by_dean'
        else:
            messages.error(request, "Invalid action.")
            return redirect('dean_review_book_chapter', pk=pk)

        # Save remarks separately for dean
        submission.dean_remarks = remarks
        submission.save()

        messages.success(request, f"Submission '{submission.chapter_title}' reviewed by Dean successfully.")
        return redirect('dean_dashboard')

    return render(request, 'dean_review_book_chapter.html', {'submission': submission})


def books_authored_submission(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        form = BooksAuthoredForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            user = FacultyUser.objects.get(user_id=request.session['user_id'])
            book.user = user
            book.save()
            messages.success(request, "Book Authored details submitted successfully.")
            return redirect('my_submissions')
    else:
        form = BooksAuthoredForm()
    return render(request, 'books_authored_submission.html', {'form': form})


def review_submission_books_authored(request, submission_id):
    submission = get_object_or_404(BooksAuthored, id=submission_id)

    if request.method == 'POST':
        status = request.POST.get('status')  # 'approved_by_cluster', 'rejected_by_cluster', 'revision'
        remarks = request.POST.get('remarks')

        if status not in ['approved_by_cluster', 'rejected_by_cluster', 'revision']:
            messages.error(request, 'Invalid status.')
            return redirect('review_submission_books_authored', submission_id=submission.id)

        # Map status to cluster_head_status
        if status == 'approved_by_cluster':
            submission.cluster_head_status = 'approved'
            submission.status = 'approved_by_cluster'
        elif status == 'rejected_by_cluster':
            submission.cluster_head_status = 'rejected'
            submission.status = 'rejected_by_cluster'
        elif status == 'revision':
            submission.cluster_head_status = 'revision'
            submission.status = 'revision'

        submission.cluster_head_remarks = remarks
        submission.save()

        messages.success(request, f"Submission '{submission.book_title}' reviewed successfully.")
        return redirect('cluster_head_dashboard')
    return render(request, 'review_submission_books_authored.html', {'submission': submission})


def dean_review_books_authored(request, pk):
    submission = get_object_or_404(BooksAuthored, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        remarks = request.POST.get('remarks')

        # Validate and set dean review status
        if action == 'approve':
            submission.dean_status = 'approved'
            submission.status = 'approved_by_dean'
        elif action == 'reject':
            submission.dean_status = 'rejected'
            submission.status = 'rejected_by_dean'
        else:
            messages.error(request, "Invalid action.")
            return redirect('dean_review_books_authored', pk=pk)

        # Save remarks separately for dean
        submission.dean_remarks = remarks
        submission.save()

        messages.success(request, f"Submission '{submission.book_title}' reviewed by Dean successfully.")
        return redirect('dean_dashboard')

    return render(request, 'dean_review_books_authored.html', {'submission': submission})

def consultancy_project(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        form = ConsultancyProjectsForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            user = FacultyUser.objects.get(user_id=request.session['user_id'])
            project.user = user
            project.save()
            messages.success(request, "Consultancy project submitted successfully.")
            return redirect('my_submissions')
    else:
        form = ConsultancyProjectsForm()
    return render(request, 'consultancy_projects.html', {'form': form})


def review_submission_consultancy_project(request, submission_id):
    submission = get_object_or_404(ConsultancyProjects, id=submission_id)

    if request.method == 'POST':
        status = request.POST.get('status')  # 'approved_by_cluster', 'rejected_by_cluster', 'revision'
        remarks = request.POST.get('remarks')

        if status not in ['approved_by_cluster', 'rejected_by_cluster', 'revision']:
            messages.error(request, 'Invalid status.')
            return redirect('review_submission_consultancy_project', submission_id=submission.id)

        # Map status to cluster_head_status
        if status == 'approved_by_cluster':
            submission.cluster_head_status = 'approved'
            submission.status = 'approved_by_cluster'
        elif status == 'rejected_by_cluster':
            submission.cluster_head_status = 'rejected'
            submission.status = 'rejected_by_cluster'
        elif status == 'revision':
            submission.cluster_head_status = 'revision'
            submission.status = 'revision'

        submission.cluster_head_remarks = remarks
        submission.save()

        messages.success(request, f"Submission '{submission.project_title}' reviewed successfully.")
        return redirect('cluster_head_dashboard')
    return render(request, 'review_submission_consultancy_project.html', {'submission': submission})


def dean_review_consultancy_project(request, pk):
    submission = get_object_or_404(ConsultancyProjects, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        remarks = request.POST.get('remarks')

        # Validate and set dean review status
        if action == 'approve':
            submission.dean_status = 'approved'
            submission.status = 'approved_by_dean'
        elif action == 'reject':
            submission.dean_status = 'rejected'
            submission.status = 'rejected_by_dean'
        else:
            messages.error(request, "Invalid action.")
            return redirect('dean_review_consultancy_project', pk=pk)

        # Save remarks separately for dean
        submission.dean_remarks = remarks
        submission.save()

        messages.success(request, f"Submission '{submission.project_title}' reviewed by Dean successfully.")
        return redirect('dean_dashboard')

    return render(request, 'dean_review_consultancy_project.html', {'submission': submission})



def editorial_roles(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        form = EditorialRolesForm(request.POST, request.FILES)
        if form.is_valid():
            role = form.save(commit=False)
            user = FacultyUser.objects.get(user_id=request.session['user_id'])
            role.user = user
            role.save()
            messages.success(request, "Editorial role submitted successfully.")
            return redirect('my_submissions')
    else:
        form = EditorialRolesForm()
    return render(request, 'editorial_roles.html', {'form': form})



def review_submission_editorial_roles(request, submission_id):
    submission = get_object_or_404(EditorialRoles, id=submission_id)

    if request.method == 'POST':
        status = request.POST.get('status')  # 'approved_by_cluster', 'rejected_by_cluster', 'revision'
        remarks = request.POST.get('remarks')

        if status not in ['approved_by_cluster', 'rejected_by_cluster', 'revision']:
            messages.error(request, 'Invalid status.')
            return redirect('review_submission_editorial_roles', submission_id=submission.id)

        # Map status to cluster_head_status
        if status == 'approved_by_cluster':
            submission.cluster_head_status = 'approved'
            submission.status = 'approved_by_cluster'
        elif status == 'rejected_by_cluster':
            submission.cluster_head_status = 'rejected'
            submission.status = 'rejected_by_cluster'
        elif status == 'revision':
            submission.cluster_head_status = 'revision'
            submission.status = 'revision'

        submission.cluster_head_remarks = remarks
        submission.save()

        messages.success(request, f"Submission '{submission.editorial_role}' reviewed successfully.")
        return redirect('cluster_head_dashboard')
    return render(request, 'review_submission_editorial_roles.html', {'submission': submission})



def dean_review_editorial_roles(request, pk):
    submission = get_object_or_404(EditorialRoles, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        remarks = request.POST.get('remarks')

        # Validate and set dean review status
        if action == 'approve':
            submission.dean_status = 'approved'
            submission.status = 'approved_by_dean'
        elif action == 'reject':
            submission.dean_status = 'rejected'
            submission.status = 'rejected_by_dean'
        else:
            messages.error(request, "Invalid action.")
            return redirect('dean_review_editorial_roles', pk=pk)

        # Save remarks separately for dean
        submission.dean_remarks = remarks
        submission.save()

        messages.success(request, f"Submission '{submission.editorial_role}' reviewed by Dean successfully.")
        return redirect('dean_dashboard')

    return render(request, 'dean_review_editorial_roles.html', {'submission': submission})