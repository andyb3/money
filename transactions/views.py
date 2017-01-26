from django.shortcuts import render, redirect

from transactions.ofxImport import ofxData
from transactions.forms import OFX_Form
from transactions.models import Account, OFX_Upload, Transaction, Transaction_Type

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
            statementDetails = data.statementDetails() #returns dictionary of statement level details, or 'error'
            if statementDetails == 'error':
                print('error placeholder 1')
                #return render/redirect reload page with error message
            #returns list of account that match the account ID in OFX
            account = Account.objects.filter(ofx_accountID=statementDetails['account'])
            if len(account) != 1: #If more than one account matches, return error message
                print('error placeholder 2')
                #return render/redirect reload page with error message
            a = account[0] #Get the account object for matching account
            #Add a new OFX_Upload record for the account
            o = a.ofx_upload_set.create(ofx_file=f,
                                        period_start=statementDetails['period_start'],
                                        period_end=statementDetails['period_end'])
            all_tx = data.transDetails() # Returns list of dictionaries with transaction level details, or 'error'
            if all_tx == 'error':
                print('error placeholder 3')
                #return render/redirect reload page with error message
            for tx in all_tx: #loop through transactions in dictionary
                #Check if transaction has already been uploaded previously (e.g in overlapping statement)
                matchTX = Transaction.objects.filter(ofx_txID=tx['ofx_txID'])
                if len(matchTX) == 0: #if transaction not already added...
                    #returns list of matching transaction type objects from Transaction_Type table
                    tx_type = Transaction_Type.objects.filter(ofx_type=tx['tx_type'])
                    if len(tx_type) != 1: #If it matches no or multiple tx types, return error message
                        print('error placeholder 3')
                        #return render/redirect reload page with error message
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
            latest_tx = Transaction.objects.filter(account=a).order_by('-date', 'pk')[0]
            a.balance = latest_tx.balance
            a.save()
            return redirect('transactions:ofxupload')
    else:
        form = OFX_Form()
        return render(request, 'transactions/ofxupload.html', {'form': form})

def ofxupload_submission(request):
    return render(request, 'transactions/ofxupload_submission.html')

def view_tx(request):
    return render(request, 'transactions/view_tx.html')
