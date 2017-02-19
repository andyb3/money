from django.db import models

class Bank(models.Model):
    bank_name = models.CharField(max_length=250)
    def __str__(self):
        return self.bank_name

class Account(models.Model):
    ofx_accountID = models.CharField(max_length=250, blank=True, null=True, unique=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    overdraft = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.description

class Uploaded_File(models.Model):
    upload_date = models.DateTimeField(auto_now_add=True)
    file_location = models.FileField(upload_to='uploaded_files/')
    def __str__(self):
        return self.file_location

class OFX_Upload(models.Model):
    ofx_file = models.ForeignKey(Uploaded_File, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    period_start = models.DateField()
    period_end = models.DateField()
    def __str__(self):
        return self.upload_date

class Transaction_Type(models.Model):
    ofx_type = models.CharField(max_length=250, unique=True)
    description = models.CharField(max_length=250)
    def __str__(self):
        return self.description

class Transaction(models.Model):
    ofx_upload = models.ForeignKey(OFX_Upload, blank=True, null=True, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    tx_type = models.ForeignKey(Transaction_Type, on_delete=models.CASCADE)
    date = models.DateField()
    ofx_txID = models.CharField(max_length=250, null=True, blank=True)
    description =  models.CharField(max_length=250)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    def __str__(self):
        return self.description
