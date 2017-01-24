from django.shortcuts import render, redirect

from transactions.ofxImport import ofxData
from transactions.forms import OFX_Form
from transactions.models import Account, OFX_Upload, Transaction_Type

def index(request):
    return render(request, 'transactions/index.html')

def ofxupload(request):
    if request.method == 'POST':
        form = OFX_Form(request.POST, request.FILES)
        if form.is_valid():
            f = form.save()
            upload_file_pk = f.pk
            file_path = f.file_location.path
            data = ofxData(file_path)
            statementDetails = data.statementDetails()
            if statementDetails == 'error':
                print('error placeholder 1')
                #return render/redirect reload page with error message
            account = Account.objects.filter(ofx_accountID=statementDetails['account'])
            if len(account) != 1:
                print('error placeholder 2')
                #return render/redirect reload page with error message
            a = account[0]
            o = a.ofx_upload_set.create(ofx_file=f,
                                        period_start=statementDetails['period_start'],
                                        period_end=statementDetails['period_end'])
            all_tx = data.transDetails()
            if all_tx == 'error':
                print('error placeholder 3')
                #return render/redirect reload page with error message
            for tx in all_tx:
                #add in check that txID not already in table
                tx_type = Transaction_Type.objects.filter(ofx_type=tx['tx_type'])
                if len(tx_type) != 1:
                    print('error placeholder 3')
                    #return render/redirect reload page with error message
                t = tx_type[0]
                o.transaction_set.create(account=a,
                                         tx_type=t,
                                         date=tx['date'],
                                         ofx_txID=tx['ofx_txID'],
                                         description=tx['description'],
                                         amount=tx['amount'],
                                         balance=tx['balance']
                                         )

            #update account balance: select top 1 when transactions for that account ordered by date then pk
            return redirect('transactions:index')
    else:
        form = OFX_Form()
    return render(request, 'transactions/ofxupload.html', {'form': form})

def ofxupload_submission(request):
    return render(request, 'transactions/ofxupload_submission.html')

def view_tx(request):
    return render(request, 'transactions/view_tx.html')
