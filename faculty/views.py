from django.shortcuts import render, redirect
from .forms import FacultyRegistrationForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from core.models import Faculty, Subject

# Create your views here.

@staff_member_required
def register_faculty(request):
    if request.method == 'POST':
        form = FacultyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Faculty registered successfully!')
            return redirect('register_faculty')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FacultyRegistrationForm()
    return render(request, 'faculty/register.html', {'form': form})

@login_required
def faculty_dashboard(request):
    if not hasattr(request.user, 'faculty'):
        return redirect('login')
    faculty = request.user.faculty
    subjects = Subject.objects.filter(faculty=faculty)
    return render(request, 'faculty/dashboard.html', {'faculty': faculty, 'subjects': subjects})
