from django.db import models

class Bank(models.Model):
    bank_name = models.CharField(max_length=250)
    def __str__(self):
        return self.bank_name

class Account(models.Model):
    ofx_accountID = models.CharField(max_length=250, blank=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    overdraft = models.FloatField()
    balance = models.FloatField()
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.description

class OFX_Upload(models.Model):
    upload_date = models.DateTimeField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    ofx_file = models.FileField(upload_to='ofx_uploads/')
    def __str__(self):
        return self.upload_date

class Transaction_Type(models.Model):
    ofx_type = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    def __str__(self):
        return self.description

class Transaction(models.Model):
    ofx_upload = models.ForeignKey(OFX_Upload, blank=True, null=True, on_delete=models.CASCADE)
    tx_type = models.ForeignKey(Transaction_Type, on_delete=models.CASCADE)
    date = models.DateTimeField()
    ofx_txID = models.CharField(max_length=250, null=True, blank=True)
    description =  models.CharField(max_length=250)
    amount = models.FloatField()
    balance = models.FloatField(default=0, blank=True)
    def __str__(self):
        return self.description
