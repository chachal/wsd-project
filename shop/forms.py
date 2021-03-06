from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from shop.models import Games

class AddUserForm(ModelForm):
    role_choices = (('user', 'user'), ('developer', 'developer'))
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)
    password = forms.CharField(widget=forms.PasswordInput())
    role = forms.ChoiceField(choices=role_choices)

    class Meta:
        model = User
        fields = ('username', 'password', 'role', 'first_name', 'last_name', 'email')

    def save(self,key, role, commit = True):
        user = super(AddUserForm, self).save(commit = True)
        user_profile = user.profile
        user_profile.confcode = key
        user_profile.role = role
        user_profile.save()
        user.set_password(user.password)
        user.is_active = False
        user.save()

        return user, user_profile

        if commit:
            user.save()
            return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, label="Username")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")

class Addgameform(ModelForm):

    class Meta:
        model = Games
        fields = ('name', 'price', 'url')

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(Addgameform, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(Addgameform, self).save(commit=False)
        inst.dev = self._user
        if commit:
            inst.save()
            self.save_m2m()
        return inst

