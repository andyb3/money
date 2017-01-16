from django.shortcuts import render

def index(request):
    return render(request, 'transactions/index.html')

def ofxupload(request):
    return render(request, 'transactions/ofxupload.html')

def ofxupload_submission(request):
    return render(request, 'transactions/ofxupload_submission.html')

def view_tx(request):
    return render(request, 'transactions/view_tx.html')
