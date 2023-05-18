from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Role, ProUser, Donor, BloodRequest,Invitation
from django_select2.forms import Select2Widget

class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ['email']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Отримайте user з параметрів конструктора
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if self.user.role.name != 'Administrator':
            raise forms.ValidationError("You don't have permission to add a donor.")
        return cleaned_data

class ProUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ModelChoiceField(queryset=Role.objects.all())
    invitation_code = forms.CharField(required=True)

    class Meta:
        model = ProUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role', 'invitation_code')

    def save(self, commit=True):
        user = super(ProUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.invitation_code = self.cleaned_data['invitation_code']
        if commit:
            user.save()
        return user

    class Meta:
        model = ProUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role')

    def save(self, commit=True):
        user = super(ProUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    # Додаткові поля, якщо потрібно

    # Приклад зміни мітки поля "username"
    username = forms.CharField(label='Ім\'я користувача')

    # Приклад додаткового поля
   # my_field = forms.CharField(label='Моє поле')
class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = '__all__'
        exclude = ['donation_count']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(DonorForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        print(self.user.role.name)
        if self.user.role.name != 'Administrator':
            raise forms.ValidationError("You don't have permission to add a donor.")
        return cleaned_data


class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = '__all__'
        exclude = []

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['donor'].queryset = Donor.objects.order_by('last_name')
        self.fields['user'].queryset = ProUser.objects.filter(id=self.user.id)  # Обмежуємо вибір користувача на поточного користувача

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user')
        if user != self.user:
            raise forms.ValidationError("You don't have permission to create a blood request.")
        return cleaned_data



class RejectionForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea)
    unavailability_term = forms.DateField(widget=forms.DateInput)
