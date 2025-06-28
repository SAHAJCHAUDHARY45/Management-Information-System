from django.shortcuts import render, redirect, get_object_or_404
from .forms import FacultyRegistrationForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from core.models import Faculty, Subject, Student, User
from students.forms import StudentRegistrationForm
from django import forms

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

@login_required
def manage_students(request):
    if not hasattr(request.user, 'faculty'):
        return redirect('login')
    students = Student.objects.all()
    return render(request, 'faculty/manage_students.html', {'students': students})

@login_required
def add_student(request):
    if not hasattr(request.user, 'faculty'):
        return redirect('login')
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully!')
            return redirect('manage_students')
    else:
        form = StudentRegistrationForm()
    return render(request, 'faculty/add_student.html', {'form': form})

@login_required
def edit_student(request, student_id):
    if not hasattr(request.user, 'faculty'):
        return redirect('login')
    student = get_object_or_404(Student, id=student_id)
    class EditStudentForm(StudentRegistrationForm):
        username = forms.CharField(initial=student.user.username)
        password = forms.CharField(widget=forms.PasswordInput, required=False)
        name = forms.CharField(label='Full Name', initial=student.user.first_name)
        email = forms.EmailField(initial=student.user.email)
        phone_number = forms.CharField(label='Phone Number', initial=student.phone_number)
    if request.method == 'POST':
        form = EditStudentForm(request.POST, instance=student)
        if form.is_valid():
            user = student.user
            user.username = form.cleaned_data['username']
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
            user.first_name = form.cleaned_data['name']
            user.email = form.cleaned_data['email']
            user.save()
            student.phone_number = form.cleaned_data['phone_number']
            student.roll_number = form.cleaned_data['roll_number']
            student.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('manage_students')
    else:
        form = EditStudentForm(instance=student)
    return render(request, 'faculty/edit_student.html', {'form': form, 'student': student})

@login_required
def delete_student(request, student_id):
    if not hasattr(request.user, 'faculty'):
        return redirect('login')
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        user = student.user
        student.delete()
        user.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('manage_students')
    return render(request, 'faculty/delete_student.html', {'student': student})

@login_required
def assign_subjects(request, student_id):
    if not hasattr(request.user, 'faculty'):
        return redirect('login')
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        subject_ids = request.POST.getlist('subjects')
        student.subjects.set(subject_ids)
        student.save()
        messages.success(request, 'Subjects assigned successfully!')
        return redirect('manage_students')
    subjects = Subject.objects.all()
    return render(request, 'faculty/assign_subjects.html', {'student': student, 'subjects': subjects})
