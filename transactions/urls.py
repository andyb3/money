from django.conf.urls import url

from . import views

app_name = 'transactions'
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'ofxupload/$', views.ofxupload, name="ofxupload"),
    url(r'ofxupload/(?P<success_code>[1-2]+)/$', views.ofxupload_submission, name="ofxupload_submission"),
    url(r'view/$', views.view_tx, name="view_tx"),
    url(r'select/$', views.select_tx, name="select_tx"),
]
