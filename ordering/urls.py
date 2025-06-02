from django.conf import settings
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^order$', views.make_order, name='order'),
    url(r'^success$', TemplateView.as_view(template_name="success.haml"), name='success'),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^email_debug/(?P<pk>\d+)/$', views.email_debug, name='email_debug'),
        url(r'^admin_email_debug/(?P<pk>\d+)/$', views.admin_email_debug, name='admin_email_debug'),
    ]
