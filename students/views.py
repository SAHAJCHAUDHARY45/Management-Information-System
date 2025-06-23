from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
    return render(request, 'students/home.html')

@login_required
def student_dashboard(request):
    if not hasattr(request.user, 'student'):
        return redirect('login')
    student = request.user.student
    return render(request, 'students/dashboard.html', {'student': student})
