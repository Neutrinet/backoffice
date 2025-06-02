from django.conf.urls import url
from django.views.generic import ListView

from ordering.models import GroupOrder

from .utils import user_is_admin
from . import views


urlpatterns = [
    url(r'^$', user_is_admin(views.dashboard), name='admin2_home'),
    url(r'^group_order/(?P<pk>\d+)/$', user_is_admin(views.group_order_detail), name='admin2_group_order_detail'),
]
