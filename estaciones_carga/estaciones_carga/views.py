from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.user_type == 'admin':
        return render(request, 'admin_dashboard.html')
    elif user_profile.user_type == 'client':
        return render(request, 'client_dashboard.html')
    else:
        return redirect('/login/')  # Manejar casos inesperados

