from django.conf import settings
from django.urls import re_path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^order$', views.make_order, name='order'),
    re_path(r'^success$', TemplateView.as_view(template_name="success.haml"), name='success'),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^email_debug/(?P<pk>\d+)/$', views.email_debug, name='email_debug'),
        re_path(r'^admin_email_debug/(?P<pk>\d+)/$', views.admin_email_debug, name='admin_email_debug'),
    ]
