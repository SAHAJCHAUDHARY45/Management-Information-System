from django.urls import path
from .views import (
    faculty_home, register_faculty, faculty_dashboard, manage_students, add_student, edit_student, delete_student, assign_subjects,
    manage_subjects, add_subject, edit_subject, delete_subject,
    manage_results, add_result, edit_result, delete_result, students_by_department
)
from django.shortcuts import redirect

def faculty_root(request):
    return redirect('faculty_home')

urlpatterns = [
    path('', faculty_root, name='faculty_root'),  # Handles /faculty/
    path('home/', faculty_home, name='faculty_home'),
    path('register/', register_faculty, name='register_faculty'),
    path('dashboard/', faculty_dashboard, name='faculty_dashboard'),
    path('students/', manage_students, name='manage_students'),
    path('students/add/', add_student, name='add_student'),
    path('students/<int:student_id>/edit/', edit_student, name='edit_student'),
    path('students/<int:student_id>/delete/', delete_student, name='delete_student'),
    path('students/<int:student_id>/assign_subjects/', assign_subjects, name='assign_subjects'),
    path('students/department/<str:department>/', students_by_department, name='students_by_department'),
    # Subject Management URLs
    path('subjects/', manage_subjects, name='manage_subjects'),
    path('subjects/add/', add_subject, name='add_subject'),
    path('subjects/<int:subject_id>/edit/', edit_subject, name='edit_subject'),
    path('subjects/<int:subject_id>/delete/', delete_subject, name='delete_subject'),
    # Result Management URLs
    path('results/', manage_results, name='manage_results'),
    path('results/add/', add_result, name='add_result'),
    path('results/<int:result_id>/edit/', edit_result, name='edit_result'),
    path('results/<int:result_id>/delete/', delete_result, name='delete_result'),
] 