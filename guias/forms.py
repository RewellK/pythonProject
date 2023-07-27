from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Address
from django import forms



class CustomUserCreationForm(UserCreationForm):
    street = forms.CharField(max_length=100)
    number = forms.CharField(max_length=20)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=50)
    cep = forms.CharField(max_length=10)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
        'username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'street', 'number', 'city', 'state',
        'cep')

    def save(self, commit=True):
        user = super().save(commit=False)

        address = Address.objects.create(
            street=self.cleaned_data['street'],
            number=self.cleaned_data['number'],
            city=self.cleaned_data['city'],
            state=self.cleaned_data['state'],
            cep=self.cleaned_data['cep']
        )

        user.address = address

        if commit:
            user.save()
        return user
