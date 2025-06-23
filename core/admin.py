from django.contrib import admin
from .models import User, Faculty, Subject, Student, Result, Announcement

admin.site.register(User)
admin.site.register(Faculty)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Result)
admin.site.register(Announcement)
