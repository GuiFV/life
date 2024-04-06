from allauth.account.forms import SignupForm, ResetPasswordForm
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Invisible
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Goal, GoogleAgenda, Notes


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ('my_notes',)
        widgets = {
            "my_notes": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"},
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["my_notes"].required = False


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        exclude = ('user', 'matrix')

        widgets = {'start_date': forms.DateInput(attrs={'id': 'flatpickr-date1',
                                                        'class': 'flatpickr'}),
                   'end_date': forms.DateInput(attrs={'id': 'flatpickr-date2',
                                                      'class': 'flatpickr'})
                   }

    def clean(self):
        """Validates that start date must be smaller than end date"""
        super(GoalForm, self).clean()
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        if start_date and end_date and start_date >= end_date:
            raise ValidationError("Start date must be earlier than end date")


class GoogleAgendaForm(forms.ModelForm):

    agenda_id = forms.CharField(
        label='Google agenda url',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 12})
    )

    class Meta:
        model = GoogleAgenda
        fields = ('agenda_id',)


class UserUpdateForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control custom-name-width'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control custom-name-width'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control custom-name-width'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class CustomSignupForm(SignupForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)


class CustomResetPasswordForm(ResetPasswordForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)
