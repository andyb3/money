from django.conf.urls import url

from . import views

app_name = 'transactions'
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'ofxupload/$', views.ofxupload, name="ofxupload"),
    url(r'ofxupload/submission/$', views.ofxupload_submission, name="ofxupload_submission"),
    url(r'view/$', views.view_tx, name="view_tx"),
]
