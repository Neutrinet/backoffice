import csv
from datetime import datetime
from StringIO import StringIO

from django.db import transaction

from .models import Movement

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
            movement.bank_id = entry["Valutadatum"]
            movement.date = datetime.strptime(entry["Datum v. verrichting"], "%d-%m-%Y").date()
            movement.amount = float(entry["Bedrag v/d verrichting"].replace(".", "").replace(",", ".")) + (int(entry["Munt"]) * 0.01)

            if movement.amount < 0:
                movement.kind = "debit"

                # XXX could we have float errors here?
                # I might want to do string parsing to remove the "-"
                # but that sucks
                movement.amount = -1 * movement.amount
            else:
                movement.kind = "credit"

            movement.comment = "From: %s\nCommunication: '%s'" % (entry["Naam v/d tegenpartij :"], entry["Mededeling 1 :"])

            movement.title = "FIXME"

            # I've already imported this movement, don't do anything
            if Movement.objects.filter(bank_id=entry["Ref. v/d verrichting"]).exists():
                for_report["skip_because_already_imported"].append(Movement.objects.get(bank_id=entry["Ref. v/d verrichting"]))
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
                for_report["guessed_title"].append((movement, entry["Mededeling 1 :"], entry["Naam v/d tegenpartij :"]))

            movement.save()

    return for_report


def guess_title(movement, entry):
    if movement.kind == "debit" and entry["Rekening tegenpartij"] == "BE52 6528 3497 8409":
        return "Frais Bancaires"

    if movement.kind == "debit" and entry["Rekening tegenpartij"] == "GB24 MIDL 4005 1570 5243 70":
        return "Commande Olimex UK"

    if movement.kind == "debit":
        return None

    # everything is a credit starting from here

    title = entry["Mededeling 1 :"]

    if movement.amount in (6, 8, 10):
        return "Redevance VPN"

    if "cotisation" in title.lower() and movement.amount < 70:
        return "Cotisation"

    if "cube order" in title.lower() or "order" in title.lower() or "brique" in title.lower():
        return "Commande de Brique Internet"

    if 60 <= movement.amount <= 80:
        return "Commande de Brique Internet"

    return None
