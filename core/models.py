from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)

class Faculty(models.Model):
    user = models.OneToOneField('core.User', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.get_full_name()

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}" if self.code else self.name

class Student(models.Model):
    DEPARTMENT_CHOICES = [
        ('computer_science', 'Computer Science'),
        ('information_technology', 'Information Technology'),
        ('electronics', 'Electronics & Communication'),
        ('mechanical', 'Mechanical Engineering'),
        ('civil', 'Civil Engineering'),
        ('electrical', 'Electrical Engineering'),
        ('business', 'Business Administration'),
        ('arts', 'Arts & Humanities'),
        ('science', 'Science'),
        ('commerce', 'Commerce'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField('core.User', on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, default='computer_science')
    subjects = models.ManyToManyField(Subject, blank=True)

    def __str__(self):
        return self.user.get_full_name()

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.IntegerField()
    grade = models.CharField(max_length=2, blank=True)

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.marks}"

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    to_students = models.ManyToManyField(Student, blank=True)
    to_groups = models.CharField(max_length=100, blank=True)  # For group announcements
    created_by = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title
