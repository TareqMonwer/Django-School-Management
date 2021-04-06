from django_file_form.forms import FileFormMixin, MultipleUploadedFileField
from django import forms
from .models import NoticeDocument, Notice


class NoticeDocumentForm(FileFormMixin, forms.Form):
    input_file = MultipleUploadedFileField()


class NoticeForm(forms.ModelForm):
    expires_at = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )

    class Meta:
        model = Notice
        fields = (
            'title', 'file',
            'content',
        )
