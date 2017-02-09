from django.conf.urls import url

from . import views

app_name = 'transactions'
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'ofxupload/$', views.ofxupload, name="ofxupload"),
    url(r'(?P<message_code>[1-3]+)/$', views.submission, name="submission"),
    url(r'view/$', views.view_tx, name="view_tx"),
    url(r'select/$', views.select_tx, name="select_tx"),
    url(r'transaction/$', views.add_tx, name="add_tx"),
]
