from django import forms


class CSVUploaderForm(forms.Form):
    csv_file = forms.FileField()
