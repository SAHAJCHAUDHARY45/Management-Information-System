from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import Announcement, Student, Faculty
from .forms import AnnouncementForm
from django.contrib import messages

@login_required
def announcement_list(request):
    if hasattr(request.user, 'student'):
        student = request.user.student
        announcements = Announcement.objects.filter(to_students=student) | Announcement.objects.filter(to_groups__in=['all', ''])
    elif hasattr(request.user, 'faculty'):
        faculty = request.user.faculty
        announcements = Announcement.objects.filter(created_by=faculty)
    else:
        announcements = Announcement.objects.none()
    return render(request, 'announcements/list.html', {'announcements': announcements})

@login_required
def create_announcement(request):
    if not hasattr(request.user, 'faculty'):
        return redirect('login')
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user.faculty
            announcement.save()
            form.save_m2m()
            messages.success(request, 'Announcement created!')
            return redirect('announcement_list')
    else:
        form = AnnouncementForm()
    return render(request, 'announcements/create.html', {'form': form}) 