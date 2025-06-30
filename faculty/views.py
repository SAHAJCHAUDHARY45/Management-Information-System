from django.shortcuts import render, redirect, get_object_or_404
from .forms import FacultyRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import Faculty, Subject, Student, User, Result, Announcement
from students.forms import StudentRegistrationForm
from django import forms

# Create your views here.

def faculty_home(request):
    announcements = Announcement.objects.all().order_by('-created_at')[:5]
    return render(request, 'faculty/home.html', {'announcements': announcements})

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
    students = Student.objects.all()
    return render(request, 'faculty/dashboard.html', {'faculty': faculty, 'subjects': subjects, 'students': students})

@login_required
def students_by_department(request, department):
    if not hasattr(request.user, 'faculty'):
        return redirect('login')
    students = Student.objects.filter(department=department)
    department_label = dict(Student.DEPARTMENT_CHOICES).get(department, department)
    return render(request, 'faculty/manage_students.html', {
        'students': students,
        'selected_department': department,
        'department_label': department_label,
        'departments': Student.DEPARTMENT_CHOICES,
    })

@login_required
def manage_students(request):
    if not hasattr(request.user, 'faculty'):
        return redirect('login')
    department = request.GET.get('department')
    if department:
        students = Student.objects.filter(department=department)
    else:
        students = Student.objects.all()
    return render(request, 'faculty/manage_students.html', {
        'students': students,
        'selected_department': department,
        'departments': Student.DEPARTMENT_CHOICES,
    })

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

# Subject Management
@login_required
def manage_subjects(request):
    if not hasattr(request.user, 'faculty'):
        return redirect('login')
    subjects = Subject.objects.all()
    return render(request, 'faculty/manage_subjects.html', {'subjects': subjects})

@login_required
def add_subject(request):
    if not hasattr(request.user, 'faculty'):
        return redirect('login')
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        if name and code:
            Subject.objects.create(name=name, code=code, faculty=request.user.faculty)
            messages.success(request, 'Subject added successfully!')
            return redirect('manage_subjects')
    return render(request, 'faculty/add_subject.html')

@login_required
def edit_subject(request, subject_id):
    if not hasattr(request.user, 'faculty'):
        return redirect('login')
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        subject.name = request.POST.get('name')
        subject.code = request.POST.get('code')
        subject.save()
        messages.success(request, 'Subject updated successfully!')
        return redirect('manage_subjects')
    return render(request, 'faculty/edit_subject.html', {'subject': subject})

@login_required
def delete_subject(request, subject_id):
    if not hasattr(request.user, 'faculty'):
        return redirect('login')
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted successfully!')
        return redirect('manage_subjects')
    return render(request, 'faculty/delete_subject.html', {'subject': subject})

# Result Management
@login_required
def manage_results(request):
    if not hasattr(request.user, 'faculty'):
        return redirect('login')
    results = Result.objects.all()
    return render(request, 'faculty/manage_results.html', {'results': results})

@login_required
def add_result(request):
    if not hasattr(request.user, 'faculty'):
        return redirect('login')
    if request.method == 'POST':
        student_id = request.POST.get('student')
        subject_id = request.POST.get('subject')
        marks = request.POST.get('marks')
        if student_id and subject_id and marks:
            student = get_object_or_404(Student, id=student_id)
            subject = get_object_or_404(Subject, id=subject_id)
            Result.objects.create(student=student, subject=subject, marks=marks)
            messages.success(request, 'Result added successfully!')
            return redirect('manage_results')
    students = Student.objects.all()
    subjects = Subject.objects.all()
    return render(request, 'faculty/add_result.html', {'students': students, 'subjects': subjects})

@login_required
def edit_result(request, result_id):
    if not hasattr(request.user, 'faculty'):
        return redirect('login')
    result = get_object_or_404(Result, id=result_id)
    if request.method == 'POST':
        result.marks = request.POST.get('marks')
        result.save()
        messages.success(request, 'Result updated successfully!')
        return redirect('manage_results')
    return render(request, 'faculty/edit_result.html', {'result': result})

@login_required
def delete_result(request, result_id):
    if not hasattr(request.user, 'faculty'):
        return redirect('login')
    result = get_object_or_404(Result, id=result_id)
    if request.method == 'POST':
        result.delete()
        messages.success(request, 'Result deleted successfully!')
        return redirect('manage_results')
    return render(request, 'faculty/delete_result.html', {'result': result})
