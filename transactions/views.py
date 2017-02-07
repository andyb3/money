from django.shortcuts import render, redirect
from django.urls import reverse
from transactions.ofxImport import ofxData
from transactions.forms import OFX_Form, TX_History
from transactions.models import Account, OFX_Upload, Transaction, Transaction_Type
from decimal import Decimal

def index(request):
    return render(request, 'transactions/index.html')

def ofxupload(request):
    if request.method == 'POST': #if user has submitted a file
        form = OFX_Form(request.POST, request.FILES) #Pass posted file to form object
        if form.is_valid():
            f = form.save() #Save record in Uploaded_File table in db. Returns the model object for Uploaded File.
            upload_file_pk = f.pk #Get primary key of uploaded file record
            file_path = f.file_location.path #Get full file path of uploaded file
            data = ofxData(file_path) #Create ofxData object
            if data.strip_head() == 'error': #if necessary, trims the header from OFX file (e.g. Natwest file)
                return redirect(reverse('transactions:ofxupload_submission', kwargs={'success_code': 2}))
            statementDetails = data.statementDetails() #returns dictionary of statement level details, or 'error'
            if statementDetails == 'error':
                return redirect(reverse('transactions:ofxupload_submission', kwargs={'success_code': 2}))
            #returns list of account that match the account ID in OFX
            account = Account.objects.filter(ofx_accountID=statementDetails['account'])
            if len(account) != 1: #If more than one account matches, return error message
                return redirect(reverse('transactions:ofxupload_submission', kwargs={'success_code': 2}))
            a = account[0] #Get the account object for matching account
            #Add a new OFX_Upload record for the account
            o = a.ofx_upload_set.create(ofx_file=f,
                                        period_start=statementDetails['period_start'],
                                        period_end=statementDetails['period_end'])
            all_tx = data.transDetails() # Returns list of dictionaries with transaction level details, or 'error'
            if all_tx == 'error':
                return redirect(reverse('transactions:ofxupload_submission', kwargs={'success_code': 2}))
            for tx in all_tx: #loop through transactions in dictionary
                #Check if transaction has already been uploaded previously (e.g in overlapping statement)
                matchTX = Transaction.objects.filter(ofx_txID=tx['ofx_txID'])
                if len(matchTX) == 0: #if transaction not already added...
                    #returns list of matching transaction type objects from Transaction_Type table
                    tx_type = Transaction_Type.objects.filter(ofx_type=tx['tx_type'])
                    if len(tx_type) != 1: #If it matches no or multiple tx types, return error message
                        return redirect(reverse('transactions:ofxupload_submission', kwargs={'success_code': 2}))
                    t = tx_type[0] #Get the Transaction_Type object for matching tx type
                    #Creates a new transaction linked to the OFX_Upload
                    o.transaction_set.create(account=a,
                                             tx_type=t,
                                             date=tx['date'],
                                             ofx_txID=tx['ofx_txID'],
                                             description=tx['description'],
                                             amount=tx['amount'],
                                             balance=tx['balance']
                                             )
            #update account balance: select top 1 when transactions for that account ordered by date then pk
            #To get top 1 result, use slice rather than index to prevent index error if there's no transactions
            latest_tx = Transaction.objects.filter(account=a).order_by('-date', '-pk')[:1]
            if latest_tx: #If query_set contains a result...
                a.balance = latest_tx.balance
                a.save()
            return redirect(reverse('transactions:ofxupload_submission', kwargs={'success_code': 1}))
    else:
        form = OFX_Form()
        return render(request, 'transactions/ofxupload.html', {'form': form,})

def ofxupload_submission(request, success_code):
    if success_code == '1':
        message = "OFX file imported successfully"
    elif success_code == '2':
        message = "WARNING: Error occurred when importing OFX file."
    return render(request, 'transactions/ofxupload_submission.html', {'message': message})

def select_tx(request):
    form = TX_History()
    return render(request, 'transactions/select_tx.html', {'form': form,})

def view_tx(request):
    if request.method == 'POST':
        form = TX_History(request.POST) #Create new instance of form with the posted data
        if form.is_valid():
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            #Creates a list of Account objects from selected accounts.
            accounts = [a for a in Account.objects.all() if form.cleaned_data[str(a.pk)]]
            start_bal = Decimal(0)
            end_bal = Decimal(0)
            for a in accounts:
                t = Transaction.objects.filter(account=a).order_by('-date', '-pk')
                a_start_bal = t.filter(date__lt=start_date)[:1]
                a_end_bal = t.filter(date__lte=end_date)[:1]
                if a_start_bal:
                    start_bal += a_start_bal[0].balance
                if a_end_bal:
                    end_bal += a_end_bal[0].balance
            total_change = end_bal - start_bal
            context = {'start_date': start_date,
                       'end_date': end_date,
                       'start_bal': start_bal,
                       'end_bal': end_bal,
                       'total_change': total_change,
                       }
            return render(request, 'transactions/view_tx.html', context)
    #Change this to return a 404
    return render(request, 'transactions/view_tx.html')
