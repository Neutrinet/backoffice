from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .utils import user_is_admin


urlpatterns = patterns('admin2.views',
    url(r'^$', user_is_admin(TemplateView.as_view(template_name="admin2/home.haml")), name='admin2_home'),
)
