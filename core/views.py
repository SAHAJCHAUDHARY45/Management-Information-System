from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Announcement

def home(request):
    announcements = Announcement.objects.all().order_by('-created_at')[:5]
    return render(request, 'home.html', {'announcements': announcements})

@login_required
def dashboard(request):
    if hasattr(request.user, 'student'):
        return redirect('student_dashboard')
    elif hasattr(request.user, 'faculty'):
        return redirect('faculty_dashboard')
    else:
        return redirect('home')
