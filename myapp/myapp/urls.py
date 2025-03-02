from django.contrib import admin
from django.urls import path, include
from .views import auto_login
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # accounts/ uygulamasının URL'lerini dahil et
    path('', include('accounts.urls')),
    path('auto_login/', auto_login, name='auto_login'),# Ana sayfa için yönlendirme
    path('logout/', auth_views.LogoutView.as_view(next_page='/index/'), name='logout'),

    #şifre sıfırlama
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
