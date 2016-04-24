# encoding: utf-8

from datetime import datetime
from django.db import models

juridical_form_choices = (
    ('pp', 'Personne physique'),
    ('pm', 'Personne morale'),
)

class Member(models.Model):
    first_name = models.CharField(max_length=255, verbose_name="Prénom")
    last_name = models.CharField(max_length=255, verbose_name="Nom")
    last_paid_date = models.DateField(null=True, blank=True, verbose_name="Dernière date de versement de la costisation")
    juridical_form = models.CharField(choices=juridical_form_choices, default="pp", max_length=3, verbose_name="Forme juridique", help_text="99% du du temps ce sera 'personne physique' (un individu)")
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name="Lieu d'envoie du courrier")
    email = models.EmailField(null=True, blank=True)
    member_since = models.DateField(default=datetime.today, verbose_name="Membre depuis le", null=True, blank=True)
    member_end = models.DateField(null=True, blank=True, verbose_name="N'est plus membre depuis")
    why_member_end = models.TextField(null=True, blank=True, verbose_name="Pourquoi il n'est plus membre")
    ca_member = models.BooleanField(default=False, verbose_name="Membre du conseil d'administration ?")
    ca_function = models.CharField(max_length=255, null=True, blank=True, verbose_name="Rôle dans le conseil d'administration")
    billing_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="Identifiant de domiciliation", help_text="Identifiant donné à l'usagé qu'il doit mettre sur ses virements (pour le VPN pour l'instant)")

    is_not_a_member_yet = models.BooleanField(default=False, help_text="Cette personne a commandé une brique avec un access VPN mais n'a pas envoyé commencé à payer son abonnement VPN mais doit le faire. Elle sera considéré comme membre quand ça sera fait.")

    comments = models.TextField(blank=True, null=True, help_text="Random comments regarding the current situation of this member like 'paying vpn by cash' or sometehing like that.")

    vpn = models.BooleanField(default=False, verbose_name="a un abonnement vpn")
    cube = models.BooleanField(default=False, verbose_name="possède une brique")

    added_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        ordering = ['last_name', 'first_name']
