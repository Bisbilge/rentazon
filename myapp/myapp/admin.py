# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'city', 'country', 'rating']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'address', 'city', 'country', 'rating')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number', 'address', 'city', 'country', 'rating')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
