from django.urls import path
from .views import register_student, students_home, student_dashboard, student_registration_link

urlpatterns = [
    path('', students_home, name='students_home'),
    path('register/', register_student, name='register_student'),
    path('dashboard/', student_dashboard, name='student_dashboard'),
    path('join/', student_registration_link, name='student_registration_link'),
] 