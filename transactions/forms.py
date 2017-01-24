from django import forms
from transactions.models import Uploaded_File

class OFX_Form(forms.ModelForm):
    class Meta:
        model = Uploaded_File
        fields = ('file_location', )
