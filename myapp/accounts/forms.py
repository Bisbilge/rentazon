from django import forms
from .models import User

class RegisterForm(forms.ModelForm):
    # Şifreyi girme alanı (gizli şifre alanı)
    password1 = forms.CharField(
        label="Şifre",  # Kullanıcıya gösterilecek etiket
        widget=forms.PasswordInput,  # Şifreyi gizlemek için
        min_length=8  # Şifre minimum 8 karakter olmalı
    )

    # Şifreyi onaylamak için ikinci alan (gizli şifre alanı)
    password2 = forms.CharField(
        label="Şifreyi Onayla",  # Kullanıcıya gösterilecek etiket
        widget=forms.PasswordInput  # Şifreyi gizlemek için
    )

    class Meta:
        model = User  # Bu form User modeli ile ilişkili
        fields = ['name', 'email', 'phone_number', 'address', 'city', 'country']  # Formda yer alacak alanlar

    # E-posta adresinin benzersiz olduğunu kontrol eden fonksiyon
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():  # Eğer bu e-posta zaten var ise
            raise forms.ValidationError("Bu e-posta adresi zaten kullanılıyor!")  # Hata mesajı
        return email

    # Şifrelerin eşleşip eşleşmediğini kontrol eden fonksiyon
    def clean(self):
        cleaned_data = super().clean()  # Varsayılan temizleme işlemi
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:  # Eğer şifreler eşleşmiyorsa
            raise forms.ValidationError("Şifreler uyuşmuyor!")  # Hata mesajı
        return cleaned_data

    # Telefon numarasının formatını kontrol eden fonksiyon
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and len(phone_number) < 10:  # Eğer telefon numarası 10 haneli değilse
            raise forms.ValidationError("Telefon numarası geçersiz! Lütfen geçerli bir telefon numarası girin.")
        return phone_number
