from django.urls import path
from . import views
from django.shortcuts import redirect

def redirect_to_index(request):
    return redirect('index')  # 'index' URL adına yönlendir

urlpatterns = [
    path('', redirect_to_index, name='redirect-to-index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('index/', views.index_view, name='index'),
    path('logout/', views.logout_view, name='logout'),  # Çıkış işlemi için eklendi
    path('home/', views.home_view, name='home'),
]
