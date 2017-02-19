from django import forms
from transactions.models import Uploaded_File, Transaction, Account

class OFX_Form(forms.ModelForm):
    class Meta:
        model = Uploaded_File
        fields = ('file_location', ) #Uses file_location field from the Uploaded_File model
        labels = {'file_location': 'Choose OFX file'}
    def clean_file_location(self):
        data = self.cleaned_data['file_location']
        if data.name[-4:] != ".ofx":
            raise forms.ValidationError("Only OFX files (.ofx) can be imported")
        return data

class TX_Add(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('account', 'tx_type', 'date', 'description', 'amount')
        labels = {'tx_type': 'Type'}
        widgets = {'date': forms.TextInput(attrs={'class':'datepicker','autocomplete':'off'}),
                   'account': forms.Select(attrs={'class':'form-control'}),
                   'tx_type': forms.Select(attrs={'class':'form-control'})}

class TX_History(forms.Form):
    start_date = forms.DateField(label="Period start", widget=forms.TextInput(attrs={'class':'datepicker','autocomplete':'off'}))
    end_date = forms.DateField(label="Period end", widget=forms.TextInput(attrs={'class':'datepicker','autocomplete':'off'}))
    #Number of account fields varies, so have to loop and directly add to parent's self.fields attribute
    def __init__(self, *args, **kwargs):
        super(TX_History, self).__init__(*args, **kwargs)
        for account in Account.objects.all().order_by('bank'):
            #Have to convert primary key to string to use as field name, otherwise field always returns 'false'
            self.fields['acct'+str(account.pk)] = forms.BooleanField(label=account.bank.bank_name + ": " + account.description, required=False, initial=True)
    def clean(self):
        cleaned_data = super(TX_History, self).clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if not end_date >= start_date:
            raise forms.ValidationError({'end_date':"End date cannot be before start date"})
