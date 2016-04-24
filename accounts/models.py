# encoding: utf-8

from django.db import models


class Movement(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=500)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    kind = models.CharField(choices=(('credit', 'Crédit'), ('debit', 'Débit')), max_length=6)

    bank_id = models.CharField(max_length=255, unique=True, null=True, blank=True)

    comment = models.TextField(null=True, blank=True)

    added_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]

    def __unicode__(self):
        return "[%s] %s %s%s" % (self.date.strftime("%F"), self.title, "+" if self.kind == "credit" else "-", self.amount)


class ImportReport(models.Model):
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"Import report runned at %s" % (self.created_on.strftime("%F %X"))
