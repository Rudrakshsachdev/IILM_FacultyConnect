from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import FacultyProfile, JournalPublication, ConferencePublication, ResearchProject



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
