from django.shortcuts import render, redirect

from transactions.ofxImport import ofxData
from transactions.forms import OFX_Form
from transactions.models import Account, OFX_Upload

def index(request):
    return render(request, 'transactions/index.html')

def ofxupload(request):
    if request.method == 'POST':
        form = OFX_Form(request.POST, request.FILES)
        if form.is_valid():
            #print("\n!!!!!!!!!!!!!!!!!!!!!!!!")
            #ofx_file = request.FILES['file_location']
            #for line in ofx_file:
            #    print(line)
            #print("!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
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
            a.ofx_upload_set.create(ofx_file = f,
                                    period_start = statementDetails['period_start'],
                                    period_end = statementDetails['period_end'])
            all_tx = data.transDetails()
            if all_tx == 'error':
                print('error placeholder 3')
                #return render/redirect reload page with error message
            for tx in all_tx:
                print(tx['balance'])
            #update account balance
            return redirect('transactions:index')
    else:
        form = OFX_Form()
    return render(request, 'transactions/ofxupload.html', {'form': form})

def ofxupload_submission(request):
    return render(request, 'transactions/ofxupload_submission.html')

def view_tx(request):
    return render(request, 'transactions/view_tx.html')
