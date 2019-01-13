from django.conf.urls import url
from . import views

app_name = 'web'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<kerja_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^create_job/$', views.create_job, name='create_job'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^search/$', views.search, name='search'),
    url(r'^\?q=(?P<query_search>\w+)$', views.search, name='search'),
    url(r'^update/$', views.update_profile, name='update'),
    url(r'^(?P<kerja_id>[0-9]+)/delete_kerja/$', views.delete_kerja, name='delete_kerja'),
]