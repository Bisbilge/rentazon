# myapp/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
# Giriş sayfası
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('welcome')  # Giriş başarılı olursa, 'welcome' sayfasına yönlendir
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Giriş yaptıktan sonra kullanıcıyı karşılayan sayfa
@login_required
def welcome_view(request):
    return render(request, 'welcome.html')

# Çıkış yapma
def logout_view(request):
    logout(request)
    return redirect('login')

def auto_login(request):
    # Admin kullanıcı adı ve şifresi
    admin_username = 'admin'
    admin_password = 'admin_password'  # Gerçek şifreyi buraya yazın

    # Kullanıcıyı doğrulamak
    user = authenticate(request, username=admin_username, password=admin_password)

    # Kullanıcıyı doğruladıktan sonra giriş yap
    if user is not None:
        login(request, user)
        return redirect('admin:index')  # Admin paneline yönlendir
    else:
        return redirect('login')  # Eğer kullanıcı doğrulanmazsa giriş sayfasına yönlendir
