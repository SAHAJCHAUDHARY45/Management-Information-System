from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import Result, Announcement

# Create your views here.

def student_registration_link(request):
    """Landing page for student registration link"""
    return render(request, 'students/registration_link.html')

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            try:
                student = form.save()
                messages.success(
                    request, 
                    f'Registration successful! Welcome {student.user.get_full_name()}. You can now login with your username and password.'
                )
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Registration failed. Please try again. Error: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below and try again.')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'students/register.html', {'form': form})

def students_home(request):
    try:
        announcements = Announcement.objects.all().order_by('-created_at')[:5]
    except Exception as e:
        announcements = []
        messages.warning(request, f'Could not load announcements: {str(e)}')
    return render(request, 'students/home.html', {'announcements': announcements})

@login_required
def student_dashboard(request):
    try:
        if not hasattr(request.user, 'student') or not request.user.student:
            messages.error(request, 'You do not have a student profile. Please contact the administrator.')
            return redirect('home')
        
        student = request.user.student
        subjects = student.subjects.all()
        results = Result.objects.filter(student=student)
        
        return render(request, 'students/dashboard.html', {
            'student': student,
            'subjects': subjects,
            'results': results
        })
    except Exception as e:
        messages.error(request, f'Error loading dashboard: {str(e)}')
        return redirect('home')
