from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import Announcement, Student, Faculty
from .forms import AnnouncementForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

def debug_announcements(request):
    """Debug view to check announcement-related issues"""
    try:
        data = {
            'total_announcements': Announcement.objects.count(),
            'user_authenticated': request.user.is_authenticated,
            'user_username': request.user.username if request.user.is_authenticated else None,
            'user_is_student': hasattr(request.user, 'student') if request.user.is_authenticated else False,
            'user_is_faculty': hasattr(request.user, 'faculty') if request.user.is_authenticated else False,
            'student_exists': request.user.student is not None if hasattr(request.user, 'student') else False,
            'faculty_exists': request.user.faculty is not None if hasattr(request.user, 'faculty') else False,
        }
        
        if request.user.is_authenticated and hasattr(request.user, 'student') and request.user.student:
            student = request.user.student
            data['student_announcements'] = Announcement.objects.filter(to_students=student).count()
            data['all_announcements'] = Announcement.objects.filter(to_groups__in=['all', '']).count()
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)})

@login_required
def announcement_list(request):
    try:
        if hasattr(request.user, 'student') and request.user.student:
            # User is a student - show announcements targeted to them
            student = request.user.student
            announcements = Announcement.objects.filter(
                Q(to_students=student) | 
                Q(to_groups__in=['all', '']) |
                Q(to_students__isnull=True, to_groups__isnull=True)
            ).distinct().order_by('-created_at')
        elif hasattr(request.user, 'faculty') and request.user.faculty:
            # User is faculty - show announcements they created
            faculty = request.user.faculty
            announcements = Announcement.objects.filter(created_by=faculty).order_by('-created_at')
        else:
            # User is authenticated but not student or faculty - show all announcements
            announcements = Announcement.objects.all().order_by('-created_at')
    except Exception as e:
        # If there's any error, show all announcements
        announcements = Announcement.objects.all().order_by('-created_at')
        messages.warning(request, f'There was an issue loading your specific announcements. Showing all announcements.')
    
    return render(request, 'announcements/list.html', {'announcements': announcements})

@login_required
def create_announcement(request):
    if not hasattr(request.user, 'faculty') or not request.user.faculty:
        messages.error(request, 'Only faculty members can create announcements.')
        return redirect('announcement_list')
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            try:
                announcement = form.save(commit=False)
                announcement.created_by = request.user.faculty
                department = form.cleaned_data.get('department')
                send_to_all = form.cleaned_data.get('send_to_all')
                # If send_to_all is checked, send to all students
                if send_to_all:
                    announcement.save()
                # If department is selected, send to all students in that department
                elif department:
                    announcement.save()
                    students_in_dept = Student.objects.filter(department=department)
                    announcement.to_students.set(students_in_dept)
                else:
                    announcement.save()
                    form.save_m2m()
                # Set groups field appropriately
                if send_to_all:
                    announcement.to_groups = 'all'
                    announcement.save()
                # Send email notification to all users
                User = get_user_model()
                emails = list(User.objects.values_list('email', flat=True))
                send_mail(
                    subject='New Announcement',
                    message=f'New announcement: {announcement.title}\n\n{announcement.content}',
                    from_email=None,
                    recipient_list=emails,
                    fail_silently=True,
                )
                messages.success(request, 'Announcement created successfully!')
                return redirect('announcement_list')
            except Exception as e:
                messages.error(request, f'Failed to create announcement: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below and try again.')
    else:
        form = AnnouncementForm()
    
    return render(request, 'announcements/create.html', {'form': form}) 