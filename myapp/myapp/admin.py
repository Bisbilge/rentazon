# your_app/admin.py
from django.contrib import admin
from accounts.models import User

admin.site.register(User)
