from django.urls import re_path
from django.views.generic import DetailView, ListView

from . import views
from .models import ImportReport, Movement
from .utils import user_is_admin

urlpatterns = [
    re_path(
        r"^$",
        ListView.as_view(model=Movement, template_name="accounts/home.haml"),
        name="accounts_home",
    ),
    re_path(
        r"^import_report/$",
        user_is_admin(
            ListView.as_view(
                model=ImportReport, template_name="accounts/importreport_list.haml"
            )
        ),
        name="accounts_importreport_list",
    ),
    re_path(
        r"^import_report/(?P<pk>\d+)/$",
        user_is_admin(
            DetailView.as_view(
                model=ImportReport, template_name="accounts/importreport_detail.haml"
            )
        ),
        name="accounts_importreport_detail",
    ),
    re_path(
        r"^upload_record_bank_csv/$",
        user_is_admin(views.UploadRecordBankCsv.as_view()),
        name="accounts_upload_record_bank_csv",
    ),
]
