from django import forms
from transactions.models import Uploaded_File, Transaction, Account

class OFX_Form(forms.ModelForm):
    class Meta:
        model = Uploaded_File
        fields = ('file_location', ) #Uses file_location field from the Uploaded_File model
        labels = {'file_location': 'Choose OFX file'}


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
        for account in Account.objects.all():
            #Have to convert primary key to string to use as field name, otherwise field always returns 'false'
            self.fields['acct'+str(account.pk)] = forms.BooleanField(label=account.description, required=False, initial=True)
