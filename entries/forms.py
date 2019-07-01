from django.forms import ModelForm
from django import forms
from entries.models import Entry


class EntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        fields = (
            'title',
            'event',
        )
