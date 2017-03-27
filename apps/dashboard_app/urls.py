from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^register$', views.register),
    url(r'^process_registration', views.process_registration),
    url(r'^dashboard/admin$', views.admin),
    url(r'^dashboard$', views.dashboard),
    url(r'^users/update/admin/(?P<id>\d+)$', views.update_admin),
    url(r'^confirm_delete/(?P<id>\d+)$', views.confirm_delete),
    url(r'^delete_user/(?P<id>\d+)$', views.delete_user),
    url(r'^users/updatepw/admin/(?P<id>\d+)$', views.updatepw_admin),
    url(r'^users/updatepw$', views.updatepw),
    url(r'^users/update$', views.update),
    url(r'^users/new$', views.newuser),
    url(r'^users/edit/(?P<id>\d+)$', views.admin_edit),
    url(r'^users/edit$', views.edit),
    url(r'^users/show/(?P<id>\d+)$', views.show),
    url(r'^submit_message/(?P<id>\d+)$', views.submit_message),
    url(r'^submit_comment/(?P<id>\d+)$', views.submit_comment),
    url(r'^admin$', views.admin),
]
