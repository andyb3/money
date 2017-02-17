from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'transactions'
urlpatterns = [
    url(r'login/$', auth_views.login, {'template_name': 'transactions/login.html'}, name="login",),
    url(r'logout/$', auth_views.logout_then_login, name="logout",),
    url(r'^$', views.index, name="index"),
    url(r'ofxupload/$', views.ofxupload, name="ofxupload"),
    url(r'(?P<message_code>[1-3]+)/$', views.submission, name="submission"),
    url(r'select/view/$', views.view_tx, name="view_tx"),
    url(r'select/$', views.select_tx, name="select_tx"),
    url(r'transaction/$', views.add_tx, name="add_tx"),
]
