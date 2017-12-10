import csv
from datetime import datetime
from StringIO import StringIO

from django.db import transaction

from .models import Movement

nl_to_fr = {
    "Ref. v/d verrichting": "R\xe9f\xe9rence de l'op\xe9ration",
    "Datum v. verrichting": "Date d'op\xe9ration",
    "Bedrag v/d verrichting": "Montant de l'op\xe9ration",
    "Naam v/d tegenpartij :": 'Nom de la contrepartie :',
    "Mededeling 1 :": 'Communication 1 :',
    "Rekening tegenpartij": 'Compte de contrepartie',
}

def fr_or_nl(entry, key):
    if key in entry:
        return entry[key]

    return entry[nl_to_fr[key]]


def handle_recordbank_csv(csv_file):
    for_report = {
        "movement_that_might_be_the_same": [],
        "need_title": [],
        "guessed_title": [],
        "skip_because_already_imported": [],
    }

    with transaction.atomic():
        for entry in csv.DictReader(StringIO("\r\n".join(csv_file.read().split("\n")[1:]) + "\r\n"), delimiter=";"):
            movement = Movement()
            movement.bank_id = fr_or_nl(entry, "Ref. v/d verrichting")[:-1]
            movement.date = datetime.strptime(fr_or_nl(entry, "Datum v. verrichting"), "%d-%m-%Y").date()
            movement.amount = float(fr_or_nl(entry, "Bedrag v/d verrichting").replace(".", "").replace(",", "."))

            if movement.amount < 0:
                movement.kind = "debit"

                # XXX could we have float errors here?
                # I might want to do string parsing to remove the "-"
                # but that sucks
                movement.amount = -1 * movement.amount
            else:
                movement.kind = "credit"

            movement.comment = "From: %s\nCommunication: '%s'" % (fr_or_nl(entry, "Naam v/d tegenpartij :"), fr_or_nl(entry, "Mededeling 1 :"))

            movement.title = "FIXME"

            # I've already imported this movement, don't do anything
            if Movement.objects.filter(bank_id=fr_or_nl(entry, "Ref. v/d verrichting")).exists():
                movement = Movement.objects.get(bank_id=fr_or_nl(entry, "Ref. v/d verrichting"))
                if movement.title == "FIXME":
                    title = guess_title(movement, entry)
                    if title:
                        movement.title = title
                        movement.save()
                        for_report["guessed_title"].append((movement, fr_or_nl(entry, "Mededeling 1 :"), fr_or_nl(entry, "Naam v/d tegenpartij :")))

                for_report["skip_because_already_imported"].append(movement)
                continue

            movement_that_might_be_the_same = Movement.objects.filter(date=movement.date, amount=movement.amount, kind=movement.kind, bank_id__isnull=True)

            if movement_that_might_be_the_same.exists():
                for_report["movement_that_might_be_the_same"].append((movement, movement_that_might_be_the_same[0]))
                continue

            title = guess_title(movement, entry)

            if title is None:
                for_report["need_title"].append(movement)
            else:
                movement.title = title
                for_report["guessed_title"].append((movement, fr_or_nl(entry, "Mededeling 1 :"), fr_or_nl(entry, "Naam v/d tegenpartij :")))

            movement.save()

    return for_report


def guess_title(movement, entry):
    if movement.kind == "debit" and fr_or_nl(entry, "Rekening tegenpartij") == "BE52 6528 3497 8409":
        return "Frais Bancaires"

    if movement.kind == "debit" and fr_or_nl(entry, "Rekening tegenpartij").strip() == "":
        return "Frais Bancaires"

    if movement.kind == "debit" and fr_or_nl(entry, "Rekening tegenpartij") == "GB24 MIDL 4005 1570 5243 70":
        return "Commande Olimex UK"

    if movement.kind == "debit" and fr_or_nl(entry, "Rekening tegenpartij") == "LU96 0030 8787 9307 0000":
        return "Facture GANDI"

    if movement.kind == "debit" and fr_or_nl(entry, "Rekening tegenpartij") == "NL51 INGB 0004 4900 08":
        return "Frais serveur i3D"

    if movement.kind == "debit" and fr_or_nl(entry, "Rekening tegenpartij") == "BE48 6792 0055 0227":
        return "Frais status moniteur"

    if movement.kind == "debit" and fr_or_nl(entry, "Rekening tegenpartij") == "FR76 1027 8060 3100 0204 5230 163":
        return "Facture Gitoyen"

    if movement.kind == "debit":
        return None

    # everything is a credit starting from here

    title = fr_or_nl(entry, "Mededeling 1 :")

    if movement.amount in (6, 8, 10):
        return "Redevance VPN"

    if "cotisation" in title.lower() and movement.amount < 70:
        return "Cotisation"

    if title == "Abonnement Ivan":
        return "Redevance VPN"

    if movement.amount == 25:
        return "Cotisation"

    if "cube order" in title.lower() or "order" in title.lower() or "brique" in title.lower():
        return "Commande de Brique Internet"

    if 60 <= movement.amount <= 80:
        return "Commande de Brique Internet"

    return None
