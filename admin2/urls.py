from django.conf.urls import patterns, url
from django.views.generic import ListView

from ordering.models import GroupOrder

from .utils import user_is_admin
from . import views


urlpatterns = patterns('admin2.views',
    url(r'^$', user_is_admin(ListView.as_view(template_name="admin2/home.haml", queryset=GroupOrder.objects.order_by("-launched_on"))), name='admin2_home'),
    url(r'^group_order/(?P<pk>\d+)/$', user_is_admin(views.group_order_detail), name='admin2_group_order_detail'),
)
