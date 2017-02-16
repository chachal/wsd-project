from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

class AddUserForm(ModelForm):
    role_choices = (('user', 'user'), ('publisher', 'publisher'), ('admin', 'admin'))
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)
    role = forms.ChoiceField(choices=role_choices)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'role')

    def save(self,commit = True):
        user = super(AddUserForm, self).save(commit = True)
        user_profile = user.profile
        user_profile.role = self.cleaned_data['role']
        user_profile.save()
        return user, user_profile

        if commit:
            user.save()
            return user


