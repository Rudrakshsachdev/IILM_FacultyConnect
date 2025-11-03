from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from django.contrib.auth import get_user_model


from django.utils import timezone
from datetime import timedelta

from cloudinary.models import CloudinaryField

class EmailOTP(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        # OTP valid for 10 minutes
        return timezone.now() > self.created_at + timedelta(minutes=15)

    def __str__(self):
        return f"{self.email} - {self.otp}"
    
class PasswordResetOTP(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        from datetime import timedelta
        return timezone.now() > self.created_at + timedelta(minutes=15)


class FacultyUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, full_name, password, **extra_fields)


class FacultyUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    is_first_login = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    ROLE_CHOICES = [
        ('faculty', 'Faculty'),
        ('dean', 'Dean'),
        ('cluster_head', 'Cluster Head'),
        ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='faculty')

    objects = FacultyUserManager()

    def __str__(self):
        return self.email


class FacultyProfile(models.Model):
    user = models.OneToOneField(FacultyUser, on_delete=models.CASCADE)
    profile_image = CloudinaryField('profile_image', folder='profile_images', blank=True, null=True)
    EMP_ID = models.CharField(max_length=50, unique=True)
    school_faculty = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    highest_qualification = models.CharField(max_length=255)
    area_of_specialization = models.CharField(max_length=255)
    orcid_id = models.CharField(max_length=100)
    scopus_id = models.CharField(max_length=100)
    google_scholar = models.URLField()
    vidwaan_id = models.CharField(max_length=100)

    def __str__(self):
        return self.user.full_name





User = get_user_model()

class JournalPublication(models.Model):
    INDEX_CHOICES = [
        ('SCI', 'SCI'),
        ('SCIE', 'SCIE'),
        ('Scopus', 'Scopus'),
        ('WoS', 'Web of Science'),
        ('ESCI', 'ESCI'),
        ('UGC', 'UGC'),
        ('Other', 'Other'),
    ]

    FUNDING_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title_of_paper = models.CharField(max_length=255)
    first_author = models.CharField(max_length=255)
    author_position = models.CharField(max_length=255)
    corresponding_author = models.CharField(max_length=255)
    journal_name = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    issn = models.CharField(max_length=50, blank=True, null=True)
    volume = models.CharField(max_length=50, blank=True, null=True)
    issue = models.CharField(max_length=50, blank=True, null=True)
    page_no = models.CharField(max_length=50, blank=True, null=True)
    month_of_publication = models.CharField(max_length=50)
    year_of_publication = models.IntegerField()
    indexed_in = models.CharField(max_length=20, choices=INDEX_CHOICES)
    other_index = models.CharField(max_length=255, blank=True, null=True)
    impact_factor = models.CharField(max_length=50, blank=True, null=True)
    doi_link = models.URLField(blank=True, null=True)
    funding_acknowledged = models.CharField(max_length=3, choices=FUNDING_CHOICES)
    pdf_upload = CloudinaryField(
        'pdf',
        resource_type='raw',
        folder='journal_publications'
    )
    no_of_other_authors_from_iilm = models.PositiveIntegerField(default=0)

    # 🟢 CLUSTER HEAD REVIEW
    cluster_head_status = models.CharField(
        max_length=30,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('revision', 'Sent for Revision'),
        ],
        default='pending'
    )
    cluster_head_remarks = models.TextField(blank=True, null=True)

    # 🟢 DEAN REVIEW
    dean_status = models.CharField(
        max_length=30,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    dean_remarks = models.TextField(blank=True, null=True)

    # 🟢 (Optional) — Overall consolidated status for quick filtering
    status_choices = [
        ('submitted', 'Submitted'),
        ('approved_by_cluster', 'Approved by Cluster Head'),
        ('rejected_by_cluster', 'Rejected by Cluster Head'),
        ('approved_by_dean', 'Approved by Dean'),
        ('rejected_by_dean', 'Rejected by Dean'),
        ('revision', 'Sent for Revision'),
    ]
    status = models.CharField(max_length=30, choices=status_choices, default='submitted')

    remarks = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title_of_paper} ({self.user.full_name})"



class ConferencePublication(models.Model):
    INDEX_CHOICES = [
        ('SCI', 'SCI'),
        ('SCIE', 'SCIE'),
        ('Scopus', 'Scopus'),
        ('WoS', 'Web of Science'),
        ('ESCI', 'ESCI'),
        ('UGC', 'UGC'),
        ('Other', 'Other'),
    ]

    FUNDING_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    TYPE_CHOICES = [
        ('National', 'National'),
        ('International', 'International'),
    ]

    MODE_CHOICES = [
        ('Online', 'Online'),
        ('Offline', 'Offline'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title_of_paper = models.CharField(max_length=255)
    author_position = models.CharField(max_length=255)
    first_author = models.CharField(max_length=255)
    corresponding_author = models.CharField(max_length=255)
    conference_name = models.CharField(max_length=255)
    organizing_body = models.CharField(max_length=255)
    isbn = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    mode = models.CharField(max_length=50, choices=MODE_CHOICES)
    location = models.CharField(max_length=255)
    date_of_presentation = models.DateField()
    doi_link = models.URLField(blank=True, null=True)
    indexed_in = models.CharField(max_length=20, choices=INDEX_CHOICES)
    other_index = models.CharField(max_length=255, blank=True, null=True)
    funding_acknowledged = models.CharField(max_length=3, choices=FUNDING_CHOICES)
    pdf_upload = CloudinaryField(
        'pdf',
        resource_type='raw',
        folder='journal_publications'
    )
    no_of_other_authors_from_iilm = models.PositiveIntegerField(default=0)

    # 🟢 CLUSTER HEAD REVIEW
    cluster_head_status = models.CharField(
        max_length=30,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('revision', 'Sent for Revision'),
        ],
        default='pending'
    )
    cluster_head_remarks = models.TextField(blank=True, null=True)

    # 🟢 DEAN REVIEW
    dean_status = models.CharField(
        max_length=30,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    dean_remarks = models.TextField(blank=True, null=True)

    # 🟢 OVERALL CONSOLIDATED STATUS
    status_choices = [
        ('submitted', 'Submitted'),
        ('approved_by_cluster', 'Approved by Cluster Head'),
        ('rejected_by_cluster', 'Rejected by Cluster Head'),
        ('approved_by_dean', 'Approved by Dean'),
        ('rejected_by_dean', 'Rejected by Dean'),
        ('revision', 'Sent for Revision'),
    ]
    status = models.CharField(max_length=30, choices=status_choices, default='submitted')

    remarks = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title_of_paper} ({self.user.full_name})"


class ResearchProject(models.Model):
    STATUS_CHOICES = [
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Submitted', 'Submitted'),
        ('Approved', 'Approved'),
        ('Cancelled', 'Cancelled'),
        ('On Hold', 'On Hold'),
    ]

    OUTCOME_CHOICES = [
        ('Publication', 'Publication'),
        ('Patent', 'Patent'),
        ('Product', 'Product'),
    ]

    FUNDING_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=255)
    funding_agency = models.CharField(max_length=255)
    principal_investigator = models.CharField(max_length=255)
    co_pi = models.CharField(max_length=255, blank=True, null=True)
    amount_sanctioned = models.DecimalField(max_digits=12, decimal_places=2)
    duration_from = models.DateField()
    duration_to = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    outcome = models.CharField(max_length=20, choices=OUTCOME_CHOICES)
    pdf_upload = CloudinaryField(
        'pdf',
        resource_type='raw',
        folder='journal_publications'
    )
    no_of_other_authors_from_iilm = models.PositiveIntegerField(default=0)

    # 🟢 CLUSTER HEAD REVIEW
    cluster_head_status = models.CharField(
        max_length=30,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('revision', 'Sent for Revision'),
        ],
        default='pending'
    )
    cluster_head_remarks = models.TextField(blank=True, null=True)

    # 🟢 DEAN REVIEW
    dean_status = models.CharField(
        max_length=30,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    dean_remarks = models.TextField(blank=True, null=True)

    status_choices = [
        ('submitted', 'Submitted'),
        ('approved_by_cluster', 'Approved by Cluster Head'),
        ('rejected_by_cluster', 'Rejected by Cluster Head'),
        ('approved_by_dean', 'Approved by Dean'),
        ('rejected_by_dean', 'Rejected by Dean'),
        ('revision', 'Sent for Revision'),
    ]
    overall_status = models.CharField(max_length=30, choices=status_choices, default='submitted')

    remarks = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.project_title} ({self.user.full_name})"
    

class Patents(models.Model):
    PATENT_STATUS_CHOICES = [
        ('filed', 'Filed'),
        ('published', 'Published'),
        ('granted', 'Granted')
    ]

    JURISDICTION_CHOICES = [
        ('india', 'India'),
        ('international', 'International')
    ]

    PATENT_TYPE_CHOICES = [
        ('utility', 'Utility'),
        ('design', 'Design'),
        ('process', 'Process')
    ]

    REVIEW_STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('approved_by_cluster', 'Approved by Cluster Head'),
        ('rejected_by_cluster', 'Rejected by Cluster Head'),
        ('approved_by_dean', 'Approved by Dean'),
        ('rejected_by_dean', 'Rejected by Dean'),
        ('revision', 'Sent for Revision'),
    ]

    CLUSTER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('revision', 'Sent for Revision'),
    ]

    DEAN_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(FacultyUser, on_delete=models.CASCADE)
    title_of_patent = models.CharField(max_length=255)
    inventors = models.TextField()
    patent_number = models.CharField(max_length=100)
    patent_status = models.CharField(max_length=20, choices=PATENT_STATUS_CHOICES)
    date_published = models.DateField(blank=True, null=True)
    date_granted = models.DateField(blank=True, null=True)
    jurisdiction = models.CharField(max_length=20, choices=JURISDICTION_CHOICES)
    patent_type = models.CharField(max_length=20, choices=PATENT_TYPE_CHOICES)
    pdf_upload = CloudinaryField(
        'pdf',
        resource_type='raw',
        folder='journal_publications'
    )
    no_of_other_authors_from_iilm = models.PositiveIntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)
    reviewed_at = models.DateTimeField(auto_now=True)

    # Cluster Head Review
    cluster_head_status = models.CharField(max_length=30, choices=CLUSTER_STATUS_CHOICES, default='pending')
    cluster_head_remarks = models.TextField(blank=True, null=True)

    # Dean Review
    dean_status = models.CharField(max_length=30, choices=DEAN_STATUS_CHOICES, default='pending')
    dean_remarks = models.TextField(blank=True, null=True)

    # Overall status
    status = models.CharField(max_length=30, choices=REVIEW_STATUS_CHOICES, default='submitted')

    def __str__(self):
        return f"{self.title_of_patent} ({self.user.full_name})"


class Copyright(models.Model):
    TYPE_OF_WORK_CHOICES = [
        ('software', 'Software'),
        ('manual', 'Manual'),
        ('course_material', 'Course Material'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title_of_work = models.CharField(max_length=255)
    type_of_work = models.CharField(max_length=50, choices=TYPE_OF_WORK_CHOICES)
    authors = models.TextField()
    registration_number = models.CharField(max_length=100)
    date_of_grant = models.DateField()
    pdf_upload = CloudinaryField(
        'pdf',
        resource_type='raw',
        folder='journal_publications'
    )
    no_of_other_authors_from_iilm = models.PositiveIntegerField(default=0)

    # 🟢 CLUSTER HEAD REVIEW
    cluster_head_status = models.CharField(
        max_length=30,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('revision', 'Sent for Revision'),
        ],
        default='pending'
    )
    cluster_head_remarks = models.TextField(blank=True, null=True)

    # 🟢 DEAN REVIEW
    dean_status = models.CharField(
        max_length=30,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    dean_remarks = models.TextField(blank=True, null=True)

    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('approved_by_cluster', 'Approved by Cluster Head'),
        ('rejected_by_cluster', 'Rejected by Cluster Head'),
        ('approved_by_dean', 'Approved by Dean'),
        ('rejected_by_dean', 'Rejected by Dean'),
        ('revision', 'Sent for Revision'),
    ]
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='submitted')

    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title_of_work} ({self.user.full_name})"


class PhdGuidance(models.Model):
    ROLE_CHOICES = [
        ('supervisor', 'Supervisor'),
        ('co_supervisor', 'Co-Supervisor'),
        ('advisor', 'Advisor'),
        ('committee_member', 'Committee Member'),
    ]

    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('thesis_submitted', 'Thesis Submitted'),
        ('awarded', 'Awarded'),
        ('discontinued', 'Discontinued'),
    ]

    YES_NO_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    REVIEW_STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('approved_by_cluster', 'Approved by Cluster Head'),
        ('rejected_by_cluster', 'Rejected by Cluster Head'),
        ('approved_by_dean', 'Approved by Dean'),
        ('rejected_by_dean', 'Rejected by Dean'),
        ('revision', 'Sent for Revision'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name_of_scholar = models.CharField(max_length=255)
    outside_iilm = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    thesis_title = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phd_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    date_of_completion = models.DateField(null=True, blank=True)
    other_supervisors = models.TextField(blank=True, null=True)
    pdf_upload = CloudinaryField(
        'pdf',
        resource_type='raw',
        folder='journal_publications'
    )
    no_of_other_authors_from_iilm = models.PositiveIntegerField(default=0)

    # 🟢 CLUSTER HEAD REVIEW
    cluster_head_status = models.CharField(
        max_length=30,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('revision', 'Sent for Revision'),
        ],
        default='pending'
    )
    cluster_head_remarks = models.TextField(blank=True, null=True)

    # 🟢 DEAN REVIEW
    dean_status = models.CharField(
        max_length=30,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    dean_remarks = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=30, choices=REVIEW_STATUS_CHOICES, default='submitted')

    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.name_of_scholar} ({self.user.full_name})"
    
class BookChapter(models.Model):
    YES_NO_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    REVIEW_STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('approved_by_cluster', 'Approved by Cluster Head'),
        ('rejected_by_cluster', 'Rejected by Cluster Head'),
        ('approved_by_dean', 'Approved by Dean'),
        ('rejected_by_dean', 'Rejected by Dean'),
        ('revision', 'Sent for Revision'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chapter_title = models.CharField(max_length=255)
    book_title = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20)
    publication_year = models.PositiveIntegerField()
    indexed = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    author_position = models.CharField(max_length=100)
    corresponding_author = models.CharField(max_length=255)
    pdf_upload = CloudinaryField(
        'pdf',
        resource_type='raw',
        folder='journal_publications'
    )
    no_of_other_authors_from_iilm = models.PositiveIntegerField(default=0)


    # 🟢 CLUSTER HEAD REVIEW
    cluster_head_status = models.CharField(
        max_length=30,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('revision', 'Sent for Revision'),
        ],
        default='pending'
    )
    cluster_head_remarks = models.TextField(blank=True, null=True)

    # 🟢 DEAN REVIEW
    dean_status = models.CharField(
        max_length=30,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    dean_remarks = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=30, choices=REVIEW_STATUS_CHOICES, default='submitted')

    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.chapter_title} ({self.user.username})"


class BooksAuthored(models.Model):
    BOOK_TYPE_CHOICES = [
        ('authored', 'Authored'),
        ('edited', 'Edited'),
    ]

    YES_NO_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    REVIEW_STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('approved_by_cluster', 'Approved by Cluster Head'),
        ('rejected_by_cluster', 'Rejected by Cluster Head'),
        ('approved_by_dean', 'Approved by Dean'),
        ('rejected_by_dean', 'Rejected by Dean'),
        ('revision', 'Sent for Revision'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=255)
    authored_or_edited = models.CharField(max_length=10, choices=BOOK_TYPE_CHOICES)
    publisher = models.CharField(max_length=255)
    isbn = models.CharField(max_length=50)
    publication_year = models.PositiveIntegerField()
    indexed = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    authors_or_editors = models.TextField()
    no_of_other_authors_from_iilm = models.PositiveIntegerField(default=0)
    pdf_upload = CloudinaryField(
        'pdf',
        resource_type='raw',
        folder='journal_publications'
    )

    # Cluster Head Review
    cluster_head_status = models.CharField(
        max_length=30,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('revision', 'Sent for Revision'),
        ],
        default='pending'
    )
    cluster_head_remarks = models.TextField(blank=True, null=True)

    # Dean Review
    dean_status = models.CharField(
        max_length=30,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    dean_remarks = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=30, choices=REVIEW_STATUS_CHOICES, default='submitted')

    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.book_title} ({self.user.username})"
    

class ConsultancyProjects(models.Model):
    YES_NO_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    REVIEW_STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('approved_by_cluster', 'Approved by Cluster Head'),
        ('rejected_by_cluster', 'Rejected by Cluster Head'),
        ('approved_by_dean', 'Approved by Dean'),
        ('rejected_by_dean', 'Rejected by Dean'),
        ('revision', 'Sent for Revision'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=255)

    industry_partner = models.CharField(max_length=255)
    duration = models.CharField(max_length=100)

    amount_received = models.DecimalField(max_digits=12, decimal_places=2)
    role = models.CharField(max_length=100)

    outcomes = models.TextField()
    mou_signed = models.CharField(max_length=3, choices=YES_NO_CHOICES)

    no_of_other_authors_from_iilm = models.PositiveIntegerField(default=0)
    pdf_upload = CloudinaryField(
        'pdf',
        resource_type='raw',
        folder='journal_publications'
    )

    # Cluster Head Review
    cluster_head_status = models.CharField(
        max_length=30,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('revision', 'Sent for Revision'),
        ],
        default='pending'
    )
    cluster_head_remarks = models.TextField(blank=True, null=True)

    # Dean Review
    dean_status = models.CharField(
        max_length=30,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    dean_remarks = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=30, choices=REVIEW_STATUS_CHOICES, default='submitted')

    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.project_title} ({self.user.username})"


class EditorialRoles(models.Model):
    ROLE_CHOICES = [
        ('editor_in_chief', 'Editor-in-Chief'),
        ('associate_editor', 'Associate Editor'),
        ('section_editor', 'Section Editor'),
        ('review_editor', 'Review Editor'),
        ('guest_editor', 'Guest Editor'),
    ]

    REVIEW_STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('approved_by_cluster', 'Approved by Cluster Head'),
        ('rejected_by_cluster', 'Rejected by Cluster Head'),
        ('approved_by_dean', 'Approved by Dean'),
        ('rejected_by_dean', 'Rejected by Dean'),
        ('revision', 'Sent for Revision'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    journal_name = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    editorial_role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    pdf_upload = CloudinaryField(
        'pdf',
        resource_type='raw',
        folder='journal_publications'
    )
    no_of_other_editors_from_iilm = models.PositiveIntegerField(default=0)

    # Cluster Head Review
    cluster_head_status = models.CharField(
        max_length=30,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('revision', 'Sent for Revision'),
        ],
        default='pending'
    )
    cluster_head_remarks = models.TextField(blank=True, null=True)

    # Dean Review
    dean_status = models.CharField(
        max_length=30,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    dean_remarks = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=30, choices=REVIEW_STATUS_CHOICES, default='submitted')

    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.journal_name} ({self.user.username})"
    

class ReviewerRoles(models.Model):
    INDEXING_CHOICES = [
        ('sci', 'SCI'),
        ('scopus', 'Scopus'),
        ('other', 'Other'),
    ]

    REVIEW_STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('approved_by_cluster', 'Approved by Cluster Head'),
        ('rejected_by_cluster', 'Rejected by Cluster Head'),
        ('approved_by_dean', 'Approved by Dean'),
        ('rejected_by_dean', 'Rejected by Dean'),
        ('revision', 'Sent for Revision'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    journal_or_conference_name = models.CharField(max_length=255)
    publisher_or_organizer = models.CharField(max_length=255)
    frequency_of_review = models.CharField(max_length=100)
    indexing_of_journal = models.CharField(max_length=20, choices=INDEXING_CHOICES)
    pdf_upload = CloudinaryField(
        'pdf',
        resource_type='raw',
        folder='journal_publications'
    )

    # Cluster Head Review
    cluster_head_status = models.CharField(
        max_length=30,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('revision', 'Sent for Revision'),
        ],
        default='pending'
    )
    cluster_head_remarks = models.TextField(blank=True, null=True)

    # Dean Review
    dean_status = models.CharField(
        max_length=30,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    dean_remarks = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=30, choices=REVIEW_STATUS_CHOICES, default='submitted')

    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.journal_or_conference_name} ({self.user.username})"


class AwardsAchievements(models.Model):
    LEVEL_CHOICES = [
        ('institutional', 'Institutional'),
        ('state', 'State'),
        ('national', 'National'),
        ('international', 'International'),
    ]

    REVIEW_STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('approved_by_cluster', 'Approved by Cluster Head'),
        ('rejected_by_cluster', 'Rejected by Cluster Head'),
        ('approved_by_dean', 'Approved by Dean'),
        ('rejected_by_dean', 'Rejected by Dean'),
        ('revision', 'Sent for Revision'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title_of_award = models.CharField(max_length=255)
    awarding_body = models.CharField(max_length=255)
    level = models.CharField(max_length=30, choices=LEVEL_CHOICES)
    date = models.DateField()
    nature_of_contribution = models.TextField()
    pdf_upload = CloudinaryField(
        'pdf',
        resource_type='raw',
        folder='journal_publications'
    )

    # Cluster Head Review
    cluster_head_status = models.CharField(
        max_length=30,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('revision', 'Sent for Revision'),
        ],
        default='pending'
    )
    cluster_head_remarks = models.TextField(blank=True, null=True)

    # Dean Review
    dean_status = models.CharField(
        max_length=30,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    dean_remarks = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=30, choices=REVIEW_STATUS_CHOICES, default='submitted')

    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title_of_award} ({self.user.username})"




class IndustryCollaboration(models.Model):
    MOU_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    REVIEW_STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('approved_by_cluster', 'Approved by Cluster Head'),
        ('rejected_by_cluster', 'Rejected by Cluster Head'),
        ('approved_by_dean', 'Approved by Dean'),
        ('rejected_by_dean', 'Rejected by Dean'),
        ('revision', 'Sent for Revision'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    industry_name = models.CharField(max_length=255, verbose_name="Industry / Organization Name")
    nature_of_collaboration = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    outcomes = models.CharField(max_length=255, help_text="(e.g., Internship / Research / Product / Course Developed)")
    mou_signed = models.CharField(max_length=10, choices=MOU_CHOICES)
    pdf_upload = CloudinaryField(
        'pdf',
        resource_type='raw',
        folder='journal_publications'
    )

    # Cluster Head Review
    cluster_head_status = models.CharField(
        max_length=30,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('revision', 'Sent for Revision'),
        ],
        default='pending'
    )
    cluster_head_remarks = models.TextField(blank=True, null=True)

    # Dean Review
    dean_status = models.CharField(
        max_length=30,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    dean_remarks = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=30, choices=REVIEW_STATUS_CHOICES, default='submitted')

    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.industry_name} ({self.user.username})"
