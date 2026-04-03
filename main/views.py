from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
import os
from utils import SimpleOAuth2Client
from main.models import UserProfile, ConfigWeb
from datetime import datetime, timedelta

# Initialize Google OAuth Client
def get_oauth_client():
    """Create and return OAuth client with settings"""
    return SimpleOAuth2Client(
        client_id=os.getenv('GOOGLE_CLIENT_ID', ''),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET', ''),
        auth_url='https://accounts.google.com/o/oauth2/auth',
        token_url='https://oauth2.googleapis.com/token',
        redirect_uri='http://localhost:8000/login/google/callback/',
        scope='openid profile email'
    )


def index(request):
    data_biodata = [
        {
            "nama": "Davin Fauzan", 
            "umur": 19, 
            "npm" : "2406409504",
            "prodi": "Ilmu Komputer", 
            "gambar": "/static/image/davin.png"
        },
        {
            "nama": "Peter Yap", 
            "umur": 19, 
            "npm": "2406432910",
            "prodi": "Ilmu Komputer", 
            "gambar": "/static/image/peter.jpg"
        },
        {
            "nama": "Farrell Bagoes Rahmantyo", 
            "umur": 21, 
            "npm": "2406420596", 
            "prodi": "Ilmu Komputer",
            "gambar": "/static/image/farrell.png"
        },
        {
            "nama": "Andrew Wanarahardja", 
            "umur": 19, 
            "npm": "2406407373",
            "prodi": "Ilmu Komputer", 
            "gambar": "/static/image/andrew.png"
        },
		{
			"nama": "Rousan Chandra Syahbunan", 
			"umur": 19, 
			"npm": "2406435894",
			"prodi": "Ilmu Komputer", 
			"gambar": "/static/image/rousan.png"
		},
    ]
    
    # 1. Ambil atau buat objek konfigurasi web
    config, created = ConfigWeb.objects.get_or_create(id=1)
    
    # 2. Definisikan email Google anggota kelompok yang diizinkan (Ganti dengan email asli)
    # allowed_emails = [
    #     'peteryap0505@gmail.com',
    #     'davin@example.com',
    #     'farrellbagoes04@gmail.com',
    #     'andrew.wanarahardja@gmail.com',
    #     'syahrousan@gmail.com.com'
    # ]
    
    is_member = False
    
    if request.user.is_authenticated:
        # Ngecek apakah role user di database adalah 'editor'
        try:
            if hasattr(request.user, 'oauth_profile'):
                if request.user.oauth_profile.role == 'editor':
                    is_member = True
        except Exception as e:
            pass 
            
        # Handle perubahan tema jika yang submit form adalah editor
        if request.method == 'POST' and is_member:
            bg_color = request.POST.get('background_color')
            font_family = request.POST.get('font_family')
            
            if bg_color:
                config.background_color = bg_color
            if font_family:
                config.font_family = font_family
                
            config.save()
            return redirect('home') 
    
    
    context = {
        "biodata_list": data_biodata,
        "user": request.user if request.user.is_authenticated else None,
        "config": config,          
        "is_member": is_member,
    }
    
    if request.user.is_authenticated:
        try:
            context["oauth_profile"] = request.user.oauth_profile
        except UserProfile.DoesNotExist:
            context["oauth_profile"] = None
    
    return render(request, "main/index.html", context)


def login_google(request):
    """Redirect user to Google OAuth consent screen"""
    oauth_client = get_oauth_client()
    auth_url, state = oauth_client.get_authorization_url()
    
    # Store state in session for verification
    request.session['oauth_state'] = state
    
    return redirect(auth_url)


def login_google_callback(request):
    """Handle Google OAuth callback"""
    # Verify state parameter
    stored_state = request.session.get('oauth_state')
    received_state = request.GET.get('state')
    
    if not stored_state or stored_state != received_state:
        return redirect('home')
    
    # Check for authorization code
    code = request.GET.get('code')
    if not code:
        error = request.GET.get('error', 'Unknown error')
        return redirect('home')
    
    try:
        # Get access token
        oauth_client = get_oauth_client()
        token_response = oauth_client.get_token(code)
        
        # Get user info
        user_info = oauth_client.get_user_info()
        
        # Create or update user
        email = user_info.get('email')
        name = user_info.get('name', email.split('@')[0])
        google_id = user_info.get('id')
        picture = user_info.get('picture')
        
        # Get or create user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email.split('@')[0],
                'first_name': name.split()[0] if name else '',
                'last_name': ' '.join(name.split()[1:]) if len(name.split()) > 1 else '',
            }
        )
        
        # Update user if not just created
        if not created:
            user.first_name = name.split()[0] if name else ''
            user.last_name = ' '.join(name.split()[1:]) if len(name.split()) > 1 else ''
            user.save()
        
        # Create or update OAuth profile
        oauth_profile, _ = UserProfile.objects.get_or_create(user=user)
        oauth_profile.google_id = google_id
        oauth_profile.google_email = email
        oauth_profile.google_name = name
        oauth_profile.google_picture = picture
        oauth_profile.access_token = token_response.get('access_token')
        oauth_profile.refresh_token = token_response.get('refresh_token')
        
        # Calculate token expiration
        expires_in = token_response.get('expires_in', 3600)
        oauth_profile.token_expires = datetime.now() + timedelta(seconds=expires_in)
        oauth_profile.save()
        
        # Log in the user
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        # Save session explicitly
        request.session.save()
        
        # Clean up session
        if 'oauth_state' in request.session:
            del request.session['oauth_state']
        
        request.session.save()
        
        return redirect('home')
    
    except Exception as e:
        print(f"OAuth error: {str(e)}")
        return redirect('home')


def logout_user(request):
    """Log out the current user"""
    logout(request)
    return redirect('home')
