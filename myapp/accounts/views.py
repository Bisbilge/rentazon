from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.conf import settings  # settings'i ekledim
from .models import CustomUser
from .forms import RegisterForm

# Ana Sayfa (Giriş Yapılmış Kullanıcılar İçin)
@login_required
def home_view(request):
    return render(request, 'accounts/home.html')

# Giriş Sayfası
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Zaten giriş yapılmışsa anasayfaya yönlendir
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Başarıyla giriş yaptınız!")
            return redirect('home')
        else:
            messages.error(request, "Geçersiz e-posta veya şifre!")
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

# Kayıt Sayfası
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Kayıt başarılı! Hoş geldiniz!")
            return redirect('home')
        else:
            messages.error(request, "Kayıt başarısız! Lütfen bilgileri doğru giriniz.")
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})

# Şifremi Unuttum
def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            token = get_random_string(length=32)
            reset_link = request.build_absolute_uri(
                reverse('reset_password', kwargs={'token': token})
            )
            
            subject = 'RENTAZON - Şifre Sıfırlama Talebi'
            message = f'Merhaba {user.username},\n\nŞifrenizi sıfırlamak için aşağıdaki bağlantıya tıklayın:\n{reset_link}\n\nBu bağlantı 24 saat geçerlidir.\n\nRENTAZON Ekibi'
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'Şifre sıfırlama bağlantısı e-posta adresinize gönderildi.')
            return redirect('login')
        
        except CustomUser.DoesNotExist:
            messages.error(request, 'Bu e-posta adresiyle kayıtlı bir kullanıcı bulunamadı.')
        except Exception as e:
            print(f"E-posta gönderim hatası: {str(e)}")
            messages.error(request, f'Bir hata oluştu: {str(e)}. Lütfen tekrar deneyin.')
    
    return render(request, 'accounts/forgot_password.html')

# Şifre Sıfırlama (Yeni Eklenen)
def reset_password_view(request, token):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Şifreniz başarıyla güncellendi! Giriş yapabilirsiniz.')
            return redirect('login')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Geçersiz kullanıcı veya token.')
        except Exception as e:
            messages.error(request, f'Bir hata oluştu: {str(e)}')
    
    return render(request, 'accounts/reset_password.html', {'token': token})

# Çıkış (Logout)
def logout_view(request):
    logout(request)
    messages.success(request, "Başarıyla çıkış yaptınız!")
    return redirect('login')

# Kullanıcı Ana Sayfa mı, Giriş Sayfası mı Göreceğini Belirleyen Sayfa
def index_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    return redirect('login')