from django.contrib import admin
from .models import UserProfile, ConfigWeb

# Daftarin model biar muncul di halaman admin
admin.site.register(UserProfile)
admin.site.register(ConfigWeb)