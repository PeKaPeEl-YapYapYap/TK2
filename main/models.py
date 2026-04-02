from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    """Store OAuth user information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='oauth_profile')
    google_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    google_email = models.EmailField(null=True, blank=True)
    google_name = models.CharField(max_length=255, null=True, blank=True)
    google_picture = models.URLField(null=True, blank=True)
    access_token = models.TextField(null=True, blank=True)
    refresh_token = models.TextField(null=True, blank=True)
    token_expires = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - OAuth Profile"

    class Meta:
        verbose_name = "User OAuth Profile"
        verbose_name_plural = "User OAuth Profiles"

    
class ConfigWeb(models.Model):
    background_color = models.CharField(max_length=50, default="#ffffff", help_text="Contoh: #f0f0f0 atau lightblue")
    font_family = models.CharField(max_length=100, default="Arial, sans-serif", help_text="Contoh: 'Courier New', Courier, monospace")

    def __str__(self):
        return "Pengaturan Tampilan Website"