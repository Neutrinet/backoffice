from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .utils import user_is_admin
from . import views


urlpatterns = patterns('admin2.views',
    url(r'^$', user_is_admin(TemplateView.as_view(template_name="admin2/home.haml")), name='admin2_home'),
    url(r'^current_order/$', user_is_admin(views.current_order), name='admin2_current_order'),
)
