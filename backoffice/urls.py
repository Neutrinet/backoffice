from django.contrib import admin
from django.urls import include, re_path
from members.views import ffdn_api

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^admin2/", include("admin2.urls")),
    re_path(r"^", include("ordering.urls")),
    re_path(r"^accounts/", include("accounts.urls")),
    re_path(r"^isp.json$", ffdn_api),
]
