from django.conf import settings
from django.conf.urls import patterns, url
from django.views.generic import TemplateView


urlpatterns = patterns('ordering.views',
    url(r'^$', 'home', name='home'),
    url(r'^order$', 'make_order', name='order'),
    url(r'^success$', TemplateView.as_view(template_name="success.haml"), name='success'),
)

if settings.DEBUG:
    urlpatterns += patterns('ordering.views',
        url(r'^email_debug/(?P<pk>\d+)/$', 'email_debug', name='email_debug'),
        url(r'^admin_email_debug/(?P<pk>\d+)/$', 'admin_email_debug', name='admin_email_debug'),
    )
