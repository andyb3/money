from django import forms
from transactions.models import Uploaded_File

class OFX_Form(forms.ModelForm):
    class Meta:
        model = Uploaded_File
        fields = ('file_location', )
        labels = {'file_location': 'Choose OFX file'}

class TX_History(forms.Form):
    start_date = forms.DateField(label="Period start", widget=forms.TextInput(attrs={'class':'datepicker'}))
    end_date = forms.DateField(label="Period end", widget=forms.TextInput(attrs={'class':'datepicker'}))
    #possibly do the checkboxes in html form instead to put in list
    test_account = forms.BooleanField(label="test_account", required=False)
