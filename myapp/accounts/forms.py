from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="E-posta")
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        label="Telefon Numarası"
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2}),
        required=False,
        label="Adres"
    )
    city = forms.CharField(max_length=100, required=False, label="Şehir")
    country = forms.CharField(max_length=100, required=False, label="Ülke")

    class Meta:
        model = CustomUser  # Güncellenmiş model
        fields = ['username', 'email', 'phone_number', 'address', 'city', 'country']

    # E-posta benzersizliği kontrolü
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu e-posta adresi zaten kullanılıyor!")
        return email

    # Telefon numarası kontrolü
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and len(phone_number) < 10:
            raise forms.ValidationError("Telefon numarası geçersiz! En az 10 karakter olmalıdır.")
        return phone_number
