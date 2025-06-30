from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Announcement
from django.contrib.auth import logout

def home(request):
    try:
        announcements = Announcement.objects.all().order_by('-created_at')[:5]
    except Exception as e:
        announcements = []
        messages.warning(request, f'Could not load announcements: {str(e)}')
    return render(request, 'home.html', {'announcements': announcements})

@login_required
def dashboard(request):
    try:
        if hasattr(request.user, 'student') and request.user.student:
            return redirect('student_dashboard')
        elif hasattr(request.user, 'faculty') and request.user.faculty:
            return redirect('faculty_dashboard')
        else:
            messages.warning(request, 'Your account type is not recognized. Please contact the administrator.')
            return redirect('home')
    except Exception as e:
        messages.error(request, f'Error accessing dashboard: {str(e)}')
        return redirect('home')

def custom_logout(request):
    logout(request)
    return redirect('home')
