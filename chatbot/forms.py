
from django import forms
 
class PDFUploadForm(forms.Form):
    pdf_file = forms.FileField(label="ASK")
    question = forms.CharField(label='Ask a question',max_length=500, required=False)
