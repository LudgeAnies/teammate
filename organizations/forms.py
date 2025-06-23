from django import forms
from .models import Organization


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'description', 'avatar']

class InviteForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['invite_code']