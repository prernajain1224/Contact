from django import forms
from .models import Content

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['name', 'phone_number', 'alternate_phone_number', 'profile_image']
