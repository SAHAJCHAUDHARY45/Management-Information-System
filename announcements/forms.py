from django import forms
from core.models import Announcement, Student

class AnnouncementForm(forms.ModelForm):
    to_students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})
    )
    to_groups = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Group name or "all" for everyone', 'class': 'form-control'})
    )

    class Meta:
        model = Announcement
        fields = ['title', 'message', 'to_students', 'to_groups']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message', 'rows': 4}),
        } 