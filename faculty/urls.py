from django.urls import path
from .views import register_faculty, faculty_dashboard, manage_students, add_student, edit_student, delete_student, assign_subjects
from django.shortcuts import redirect

def faculty_root(request):
    return redirect('faculty_dashboard')

urlpatterns = [
    path('', faculty_root, name='faculty_root'),  # Handles /faculty/
    path('register/', register_faculty, name='register_faculty'),
    path('dashboard/', faculty_dashboard, name='faculty_dashboard'),
    path('students/', manage_students, name='manage_students'),
    path('students/add/', add_student, name='add_student'),
    path('students/<int:student_id>/edit/', edit_student, name='edit_student'),
    path('students/<int:student_id>/delete/', delete_student, name='delete_student'),
    path('students/<int:student_id>/assign_subjects/', assign_subjects, name='assign_subjects'),
] 