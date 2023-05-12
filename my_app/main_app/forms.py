from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Role, ProUser



class ProUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ModelChoiceField(queryset=Role.objects.all())

    class Meta:
        model = ProUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role')

    def save(self, commit=True):
        user = super(ProUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


