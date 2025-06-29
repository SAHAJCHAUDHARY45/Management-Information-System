from django import forms
from core.models import Announcement, Student

class AnnouncementForm(forms.ModelForm):
    to_students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all().order_by('user__first_name', 'user__last_name'),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
            'size': '8',
            'style': 'min-height: 200px;'
        }),
        help_text="Hold Ctrl (or Cmd on Mac) to select multiple students. Leave empty to send to all students."
    )
    to_groups = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Group name or "all" for everyone', 
            'class': 'form-control'
        }),
        help_text="Enter 'all' to send to all students, or leave blank for selected students only."
    )
    send_to_all = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text="Check this to send the announcement to all students (overrides individual selections)."
    )

    class Meta:
        model = Announcement
        fields = ['title', 'message', 'to_students', 'to_groups', 'send_to_all']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter announcement title'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter announcement message', 
                'rows': 4
            }),
        } 