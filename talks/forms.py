from __future__ import absolute_import

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit
import datetime
from . import models
from django.core.exceptions import ValidationError





class TalkListForm(forms.ModelForm):
    class Meta:
        fields = ('name',)
        model = models.TalkList
    def __init__(self, *args, **kwargs):
        super(TalkListForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            ButtonHolder(
                Submit('create', 'Create', css_class='btn-primary')
            )
        )



class TalkForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'host', 'when', 'room')
        model = models.Talk

    def __init__(self, *args, **kwargs):
        super(TalkForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'host',
            'when',
            'room',
            ButtonHolder(
                Submit('add', 'Add')
            )
        )
    def clean_when(self):
        when = self.cleaned_data.get['when']
        pycon_start = datetime.datetime(2015, 1, 1)
        if when > pycon_start:
            return when

        else:
            raise ValidationError('Date Not Valid')


