import datetime

from django import forms
from django.forms import ModelForm
from catalog.models import BookInstance
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # is date in past
        if data < datetime.date.today():
            raise ValidationError (_('Invalid date — renewal in past'))

        # is date in allowed range (+4 weeks from today)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError (_('Invalid date — renewal more than 4 weeks ahead'))

        # Return cleaned data
        return data


class ReturnBookModelForm(ModelForm):
    def clean_borrower(self):
        data = self.cleaned_data['borrower']
        return data
        
    def clean_status(self):
        data = self.cleaned_data['status']

        # make sure you remember to return the cleaned data
        return data

    class Meta:
        model = BookInstance
        fields = ['status','borrower']

class CheckOutBookModelForm(ModelForm):
    due_back = forms.DateField(help_text="Default 3 Weeks, max 4. Enter in form YYYY-MM-DD")

    def clean_borrower(self):
        data = self.cleaned_data['borrower']
        return data

    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        # is date in past
        if data < datetime.date.today():
            raise ValidationError (_('Invalid date — due date in past'))

        # is date in allowed range (+4 weeks from today)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError (_('Invalid date — due date more than 4 weeks ahead'))

        # Return cleaned data
        return data
    
    class Meta:
        model = BookInstance
        fields = ['borrower', 'due_back']