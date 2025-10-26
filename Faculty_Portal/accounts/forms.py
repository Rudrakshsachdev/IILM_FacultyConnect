from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import FacultyProfile, JournalPublication, ConferencePublication, ResearchProject, Patents, Copyright, PhdGuidance, BookChapter, BooksAuthored, ConsultancyProjects, EditorialRoles, ReviewerRoles, AwardsAchievements



class Step1Form(forms.ModelForm):
    class Meta:
        model = FacultyProfile
        fields = ['profile_image']

class Step2Form(forms.ModelForm):
    class Meta:
        model = FacultyProfile
        fields = ['school_faculty', 'department', 'designation', 'highest_qualification', 'area_of_specialization']

class Step3Form(forms.ModelForm):
    class Meta:
        model = FacultyProfile
        fields = ['orcid_id', 'scopus_id', 'google_scholar', 'vidwaan_id']




class JournalPublicationForm(forms.ModelForm):
    class Meta:
        model = JournalPublication
        exclude = ['user', 'status', 'remarks', 'submitted_at', 'reviewed_at', 'cluster_head_status', 'cluster_head_remarks', 'dean_status', 'dean_remarks']
        widgets = {
            'month_of_publication': forms.TextInput(attrs={'placeholder': 'e.g. March'}),
            'year_of_publication': forms.NumberInput(attrs={'min': 1900, 'max': 2100}),
            'first_author': forms.TextInput(attrs={'placeholder': 'Enter the first author\'s name'}),
        }

class ConferencePublicationForm(forms.ModelForm):
    class Meta:
        model = ConferencePublication
        exclude = ['user', 'status', 'remarks', 'submitted_at', 'reviewed_at', 'cluster_head_status', 'cluster_head_remarks', 'dean_status', 'dean_remarks']
        widgets = {
            'month_of_conference': forms.TextInput(attrs={'placeholder': 'e.g. July'}),
            'year_of_conference': forms.NumberInput(attrs={'min': 1900, 'max': 2100}),
            'first_author': forms.TextInput(attrs={'placeholder': 'Enter the first author\'s name'}),
        }

class ResearchProjectForm(forms.ModelForm):
    class Meta:
        model = ResearchProject
        exclude = ['user', 'status', 'remarks', 'submitted_at', 'reviewed_at', 'cluster_head_status', 'cluster_head_remarks', 'dean_status', 'dean_remarks']
        fields = [
            'project_title',
            'funding_agency',
            'principal_investigator',
            'co_pi',
            'amount_sanctioned',
            'duration_from',
            'duration_to',
            'status',
            'outcome',
            'pdf_upload',
            'no_of_other_authors_from_iilm'
        ]
        widgets = {
            'duration_from': forms.DateInput(attrs={'type': 'date'}),
            'duration_to': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'outcome': forms.Select(attrs={'class': 'form-select'}),
        }

class PatentForm(forms.ModelForm):
    class Meta:
        model = Patents
        exclude = [
            'user',
            'status',
            'remarks',
            'submitted_at',
            'reviewed_at',
            'cluster_head_status',
            'cluster_head_remarks',
            'dean_status',
            'dean_remarks'
        ]
        widgets = {
            'date_published': forms.DateInput(attrs={'type': 'date'}),
            'date_granted': forms.DateInput(attrs={'type': 'date'}),
            'inventors': forms.TextInput(attrs={'placeholder': "Enter inventor(s) names"}),
            'title_of_patent': forms.TextInput(attrs={'placeholder': "Enter patent title"}),
            'patent_number': forms.TextInput(attrs={'placeholder': "Enter patent/application number"}),
            'no_of_other_authors_from_iilm': forms.NumberInput(attrs={'min': 0}),
        }


class CopyrightForm(forms.ModelForm):
    class Meta:
        model = Copyright
        exclude = [
            'user',
            'status',
            'cluster_head_status',
            'cluster_head_remarks',
            'dean_status',
            'dean_remarks',
            'submitted_at',
            'reviewed_at'
        ]
        widgets = {
            'title_of_work': forms.TextInput(attrs={'placeholder': 'Enter title of work'}),
            'authors': forms.TextInput(attrs={'placeholder': 'Enter author(s) name'}),
            'registration_number': forms.TextInput(attrs={'placeholder': 'Enter registration number'}),
            'date_of_grant': forms.DateInput(attrs={'type': 'date'}),
            'no_of_other_authors_from_iilm': forms.NumberInput(attrs={'min': 0}),
        }


class PhdGuidanceForm(forms.ModelForm):
    class Meta:
        model = PhdGuidance
        exclude = [
            'user',
            'status',
            'submitted_at',
            'reviewed_at',
            'cluster_head_status',
            'cluster_head_remarks',
            'dean_status',
            'dean_remarks'
        ]
        widgets = {
            'name_of_scholar': forms.TextInput(attrs={
                'placeholder': 'Enter scholar name',
                'class': 'form-control'
            }),
            'outside_iilm': forms.Select(attrs={
                'class': 'form-control'
            }),
            'thesis_title': forms.TextInput(attrs={
                'placeholder': 'Enter thesis title',
                'class': 'form-control'
            }),
            'role': forms.Select(attrs={
                'class': 'form-control'
            }),
            'phd_status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'date_of_completion': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'other_supervisors': forms.Textarea(attrs={
                'placeholder': 'Enter other supervisors/co-supervisors from IILM',
                'class': 'form-control',
                'rows': 2
            }),
            'no_of_other_authors_from_iilm': forms.NumberInput(attrs={
                'min': 0,
                'class': 'form-control'
            }),
            'pdf_upload': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
        }


class BookChapterForm(forms.ModelForm):
    class Meta:
        model = BookChapter
        fields = [
            'chapter_title',
            'book_title',
            'publisher',
            'isbn',
            'publication_year',
            'indexed',
            'author_position',
            'corresponding_author',
            'pdf_upload',
            'no_of_other_authors_from_iilm',
        ]
        widgets = {
            'chapter_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter chapter title'
            }),
            'book_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title'
            }),
            'publisher': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter publisher name'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter ISBN number'
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter publication year',
                'min': 1900,
                'max': 2100
            }),
            'indexed': forms.Select(attrs={
                'class': 'form-control'
            }),
            'author_position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., First Author, Second Author'
            }),
            'corresponding_author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter corresponding author name'
            }),
            'pdf_upload': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'no_of_other_authors_from_iilm': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Enter number of other IILM authors'
            }),
        }
        labels = {
            'chapter_title': 'Chapter Title',
            'book_title': 'Book Title',
            'publisher': 'Publisher',
            'isbn': 'ISBN',
            'publication_year': 'Publication Year',
            'indexed': 'Indexed (Yes/No)',
            'author_position': 'Author Position',
            'corresponding_author': 'Corresponding Author',
            'pdf_upload': 'Upload Copy (PDF)',
            'no_of_other_authors_from_iilm': 'No. of Other Authors from IILM',
        }

class BooksAuthoredForm(forms.ModelForm):
    class Meta:
        model = BooksAuthored
        exclude = [
            'user', 'status', 'cluster_head_status', 'cluster_head_remarks',
            'dean_status', 'dean_remarks', 'submitted_at', 'reviewed_at'
        ]
        widgets = {
            'book_title': forms.TextInput(attrs={'placeholder': 'Enter book title'}),
            'publisher': forms.TextInput(attrs={'placeholder': 'Enter publisher name'}),
            'isbn': forms.TextInput(attrs={'placeholder': 'Enter ISBN number'}),
            'publication_year': forms.NumberInput(attrs={'placeholder': 'Enter publication year'}),
            'authors_or_editors': forms.Textarea(attrs={'rows': 3, 'placeholder': 'List all authors/editors'}),
            'no_of_other_authors_from_iilm': forms.NumberInput(attrs={'min': 0}),
        }



class ConsultancyProjectsForm(forms.ModelForm):
    class Meta:
        model = ConsultancyProjects
        exclude = [
            'user', 'status', 'cluster_head_status', 'cluster_head_remarks',
            'dean_status', 'dean_remarks', 'submitted_at', 'reviewed_at'
        ]
        widgets = {
            'project_title': forms.TextInput(attrs={'placeholder': 'Enter project title'}),
            'industry_partner': forms.TextInput(attrs={'placeholder': 'Enter industry partner / client name'}),
            'duration': forms.TextInput(attrs={'placeholder': 'e.g. Jan 2024 – Dec 2024'}),
            'amount_received': forms.NumberInput(attrs={'placeholder': 'Enter amount received'}),
            'role': forms.TextInput(attrs={'placeholder': 'Enter your role in the project'}),
            'outcomes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe outcomes or deliverables'}),
            'mou_signed': forms.Select(choices=[('yes', 'Yes'), ('no', 'No')]),
            'no_of_other_authors_from_iilm': forms.NumberInput(attrs={'min': 0}),
        }



class EditorialRolesForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Start Date"
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="End Date"
    )

    class Meta:
        model = EditorialRoles
        fields = [
            'journal_name',
            'publisher',
            'editorial_role',
            'start_date',
            'end_date',
            'pdf_upload',
            'no_of_other_editors_from_iilm',
        ]

        labels = {
            'journal_name': 'Journal Name',
            'publisher': 'Publisher',
            'editorial_role': 'Editorial Board Role',
            'pdf_upload': 'Upload Proof',
            'no_of_other_editors_from_iilm': 'No. of Other Editors from IILM',
        }

        widgets = {
            'journal_name': forms.TextInput(attrs={'class': 'form-control'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control'}),
            'editorial_role': forms.Select(attrs={'class': 'form-control'}),
            'pdf_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'no_of_other_editors_from_iilm': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }


class ReviewerRolesForm(forms.ModelForm):
    class Meta:
        model = ReviewerRoles
        exclude = [
            'user', 'status', 'cluster_head_status', 'cluster_head_remarks',
            'dean_status', 'dean_remarks', 'submitted_at', 'reviewed_at'
        ]
        widgets = {
            'journal_or_conference_name': forms.TextInput(attrs={'placeholder': 'Enter journal or conference name'}),
            'publisher_or_organizer': forms.TextInput(attrs={'placeholder': 'Enter publisher or organizer'}),
            'frequency_of_review': forms.TextInput(attrs={'placeholder': 'Enter frequency of review'}),
            'indexing_of_journal': forms.Select(attrs={'class': 'form-select'}),
        }



class AwardsAchievementsForm(forms.ModelForm):
    class Meta:
        model = AwardsAchievements
        fields = [
            'title_of_award',
            'awarding_body',
            'level',
            'date',
            'nature_of_contribution',
            'pdf_upload',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'title_of_award': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title of award'}),
            'awarding_body': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter awarding body'}),
            'level': forms.Select(attrs={'class': 'form-select'}),
            'nature_of_contribution': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe contribution recognized'}),
            'pdf_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
