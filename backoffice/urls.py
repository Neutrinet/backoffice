from members.views import ffdn_api

from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin2/', include('admin2.urls')),
    url(r'^', include('ordering.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^isp.json$', ffdn_api),
]
