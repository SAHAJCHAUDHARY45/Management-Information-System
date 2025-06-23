from django.urls import path
from .views import register_faculty, faculty_dashboard

urlpatterns = [
    path('register/', register_faculty, name='register_faculty'),
    path('dashboard/', faculty_dashboard, name='faculty_dashboard'),
] 