from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from django.contrib.auth import get_user_model


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

    objects = FacultyUserManager()

    def __str__(self):
        return self.email


class FacultyProfile(models.Model):
    user = models.OneToOneField(FacultyUser, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/')
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
    pdf_upload = models.FileField(upload_to='journal_papers/')
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
