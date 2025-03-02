from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm  # Kendi kayıt formumuz

# Ana Sayfa Görünümü (Giriş Yapılmış Kullanıcılar İçin)
@login_required
def home_view(request):
    return render(request, 'accounts/home.html')

# Giriş Görünümü
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Ana sayfaya yönlendir
        else:
            return render(request, 'accounts/login.html', {'error': 'Geçersiz kullanıcı adı veya şifre'})
    return render(request, 'accounts/login.html')

# Kayıt Görünümü
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])  # Şifreyi hashle
            user.save()
            login(request, user)  # Kullanıcıyı giriş yapmış hale getir
            return redirect("home")  # Kayıttan sonra ana sayfaya yönlendir
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})

# Şifremi Unuttum Görünümü
def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = user.id
            # Şifre sıfırlama maili gönderme
            send_mail(
                'Şifre Sıfırlama Linki',
                f'http://localhost:8000/accounts/reset-password/{uid}/{token}/',
                'admin@mywebsite.com',
                [email],
            )
            return render(request, 'accounts/forgot_password.html', {'message': 'Şifre sıfırlama maili gönderildi.'})
        except User.DoesNotExist:
            return render(request, 'accounts/forgot_password.html', {'error': 'Bu e-posta ile kayıtlı bir kullanıcı yok.'})
    return render(request, 'accounts/forgot_password.html')

# Çıkış (Logout) Görünümü
def logout_view(request):
    logout(request)  # Kullanıcıyı çıkış yaptır
    return redirect('index')  # Çıkış yaptıktan sonra index sayfasına yönlendir

# Kullanıcı Ana Sayfa mı, Giriş Sayfası mı Göreceğini Belirleyen Sayfa
def index_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Kullanıcı giriş yaptıysa ana sayfaya yönlendir
    return render(request, 'accounts/index.html')  # Kullanıcı giriş yapmadıysa giriş/kayıt sayfasını göster
