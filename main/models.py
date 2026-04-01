from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# class CustomUser(AbstractUser):
#     # npm, prodi, phtoroute
#     prodiChoices = ['Ilmu Komputer', 'Sistem Informasi', 'Kecerdasaan Artifisial']

#     npm = models.CharField(max_length=10)
#     prodi = models.CharField(choices=prodiChoices, default='Ilmu Komputer')
#     photoRoute = models.TextField()
    

class ConfigWeb(models.Model):
    background_color = models.CharField(max_length=50, default="#ffffff", help_text="Contoh: #f0f0f0 atau lightblue")
    font_family = models.CharField(max_length=100, default="Arial, sans-serif", help_text="Contoh: 'Courier New', Courier, monospace")

    def __str__(self):
        return "Pengaturan Tampilan Website"