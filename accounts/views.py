from django.shortcuts import redirect, render
from django.views.generic import View

from . import banks
from .forms import CSVUploaderForm
from .models import ImportReport


class UploadRecordBankCsv(View):
    def get(self, request):
        return render(
            request,
            "accounts/upload_record_bank_csv.haml",
            {
                "form": CSVUploaderForm(),
            },
        )

    def post(self, request):
        form = CSVUploaderForm(request.POST, request.FILES)

        if not form.is_valid():
            return render(
                request,
                "accounts/upload_record_bank_csv.haml",
                {
                    "form": form,
                },
            )

        report_data = banks.handle_recordbank_csv(form.cleaned_data["csv_file"])

        report = ImportReport.objects.create(
            content=render(
                request,
                "accounts/generate_report.haml",
                {
                    "data": report_data,
                },
            ).content
        )

        return redirect("accounts_importreport_detail", report.id)
