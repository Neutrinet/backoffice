from django.conf.urls import patterns, url
from django.views.generic import ListView, DetailView

from .models import Movement, ImportReport
from .utils import user_is_admin

from . import views


urlpatterns = patterns('',
    url(r'^$', user_is_admin(ListView.as_view(model=Movement, template_name="accounts/home.haml")), name='accounts_home'),
    url(r'^import_report/$', user_is_admin(ListView.as_view(model=ImportReport, template_name="accounts/importreport_list.haml")), name='accounts_importreport_list'),
    url(r'^import_report/(?P<pk>\d+)/$', user_is_admin(DetailView.as_view(model=ImportReport, template_name="accounts/importreport_detail.haml")), name='accounts_importreport_detail'),
    url(r'^upload_record_bank_csv/$', user_is_admin(views.UploadRecordBankCsv.as_view()), name='accounts_upload_record_bank_csv'),
)
