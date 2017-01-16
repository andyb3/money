from django.contrib import admin

from .models import Bank, Account, Transaction_Type

admin.site.register(Bank)
admin.site.register(Account)
admin.site.register(Transaction_Type)
