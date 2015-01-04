from bson import ObjectId
from django import forms
from rtuit.models import Trend

class TrendForm(forms.Form):
    name = forms.CharField(max_length=255)
    url = forms.CharField(widget=forms.widgets.Textarea())
    query = forms.CharField(widget=forms.widgets.Textarea())




    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super(TrendForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['name'].initial = self.instance.name
            self.fields['url'].initial = self.instance.url
            self.fields['query'].initial = self.instance.query


    def save(self, commit=True):
        trend = self.instance if self.instance else Trend()
        trend.name = self.cleaned_data['name']
        trend.url = self.cleaned_data['url']
        trend.query = self.cleaned_data['query']
        if commit:
            trend.save()

        return trend

