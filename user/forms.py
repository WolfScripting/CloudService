from django import forms
from allauth.account.forms import *

'''
Disable the forms
'''


class MemberLoginForm(LoginForm):
    def clean(self):
        raise forms.ValidationError('You cannot login via this method.')

class MemberChangePasswordForm(ChangePasswordForm):
    def clean(self):
        raise forms.ValidationError('You cannot change password.')


class MemberSetPasswordForm(SetPasswordForm):
    def clean(self):
        raise forms.ValidationError('You cannot set password.')


class MemberResetPasswordForm(ResetPasswordForm):
    def clean(self):
        raise forms.ValidationError('You cannot reset password.')


class MemberAddEmailForm(AddEmailForm):
    def clean(self):
        raise forms.ValidationError('You cannot add an email.')

class MemberSignupForm(SignupForm):
    def clean(self):
        raise forms.ValidationError('You cannot signup via this method')