from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),
    url(r'^dashboard$', views.dashboard),
    url(r'^adddate$', views.adddate, name='adddate'),
    url(r'^process_adddate$', views.process_adddate, name='process_adddate'),
    url(r'^viewdate/(?P<date_id>\d+)$', views.viewdate, name='viewdate'),  #views.html page to look at details of date
    url(r'^cancel/(?P<id>\d+)$', views.cancel, name="cancel"),
    url(r'^delete/(?P<id>\d+)$', views.delete, name='delete'),  # delete the date if owner
    url(r'^joindate/(?P<id>\d+)$', views.joindate, name='joindate'), #ADD
    url(r'^edit/(?P<id>\d+)$', views.edit),
    url(r'^edituser$', views.edituser),
    url(r'^processedituser$', views.processedituser),
    url(r'^process_edit$', views.process_edit, name='process_edit'),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^reg$', views.reg),
]                            # 
