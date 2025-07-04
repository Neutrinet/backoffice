# encoding: utf-8

from reversion.admin import VersionAdmin

from django.conf.locale.en import formats as en_formats
from django.contrib import admin

from .models import Movement

en_formats.DATE_FORMAT = "Y-m-d"


class MovementAdmin(VersionAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("date", "amount"),
                    ("title", "kind"),
                    ("comment",),
                    ("bank_id",),
                )
            },
        ),
    )

    list_display = ("date", "title_column", "credit_column", "debit_column")

    def debit_column(self, obj):
        if obj.kind == "debit":
            return obj.amount
        return ""

    debit_column.short_description = "Débit"

    def credit_column(self, obj):
        if obj.kind == "credit":
            return obj.amount
        return ""

    credit_column.short_description = "Crédit"

    def title_column(self, obj):
        if obj.comment:
            return "%s [has comment]" % obj.title
        return obj.title

    title_column.short_description = "Title"

    admin_views = (
        ("Neutrinet Public Accounting Page", "/accounts"),
        ("Upload Record Bank CSV ", "/accounts/upload_record_bank_csv"),
    )


admin.site.register(Movement, MovementAdmin)
