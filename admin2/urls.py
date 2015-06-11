from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .utils import user_is_admin
from . import views


urlpatterns = patterns('admin2.views',
    url(r'^$', user_is_admin(TemplateView.as_view(template_name="admin2/home.haml")), name='admin2_home'),
    url(r'^current_order/$', user_is_admin(views.current_order), name='admin2_current_order'),
    url(r'^current_order/calculate$', user_is_admin(views.calculate_final_price_for_current_order), name='admin2_calculate_final_price_for_current_order'),
)
