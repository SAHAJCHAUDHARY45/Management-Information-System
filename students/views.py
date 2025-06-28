from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import Result, Announcement

# Create your views here.

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect('register_student')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentRegistrationForm()
    return render(request, 'students/register.html', {'form': form})

def students_home(request):
    announcements = Announcement.objects.all().order_by('-created_at')[:5]
    return render(request, 'students/home.html', {'announcements': announcements})

@login_required
def student_dashboard(request):
    if not hasattr(request.user, 'student'):
        return redirect('login')
    student = request.user.student
    subjects = student.subjects.all()
    results = Result.objects.filter(student=student)
    return render(request, 'students/dashboard.html', {
        'student': student,
        'subjects': subjects,
        'results': results
    })
