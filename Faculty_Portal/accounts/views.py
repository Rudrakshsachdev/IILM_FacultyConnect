# faculty/views.py
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import FacultyUser, FacultyProfile, JournalPublication
from .forms import Step1Form, Step2Form, Step3Form, JournalPublicationForm
import random
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse

otp_storage = {}  # Temporary dictionary to hold OTPs (use Redis in production)

def signup(request):
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
    if 'user_id' in request.session:
        del request.session['user_id']
    messages.success(request, "Logged out successfully!")
    return redirect('login')


def dashboard(request):
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


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import JournalPublication


def cluster_head_dashboard(request):
    # Show all submissions that are still pending or need review
    submissions = JournalPublication.objects.filter(status='submitted').order_by('-submitted_at')
    return render(request, 'cluster_head_dashboard.html', {'submissions': submissions})



def review_submission(request, submission_id):
    submission = get_object_or_404(JournalPublication, id=submission_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        remarks = request.POST.get('remarks')

        if status not in ['approved_by_cluster', 'rejected_by_cluster', 'revision']:
            messages.error(request, 'Invalid status.')
            return redirect('review_submission', submission_id=submission.id)

        submission.status = status
        submission.remarks = remarks
        submission.save()

        messages.success(request, f"Submission '{submission.title_of_paper}' reviewed successfully.")
        return redirect('cluster_head_dashboard')

    return render(request, 'review_submission.html', {'submission': submission})
