from django.urls import re_path
from django.views.generic import ListView
from ordering.models import GroupOrder

from . import views
from .utils import user_is_admin

urlpatterns = [
    re_path(r"^$", user_is_admin(views.dashboard), name="admin2_home"),
    re_path(
        r"^group_order/(?P<pk>\d+)/$",
        user_is_admin(views.group_order_detail),
        name="admin2_group_order_detail",
    ),
]
