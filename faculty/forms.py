from django import forms
from core.models import User, Faculty

class FacultyRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    name = forms.CharField(label='Full Name', widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone_number = forms.CharField(label='Phone Number', widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))
    department = forms.CharField(label='Department', widget=forms.TextInput(attrs={'placeholder': 'Department'}))

    class Meta:
        model = Faculty
        fields = ['phone_number', 'department']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['name'],
            is_faculty=True
        )
        faculty = super().save(commit=False)
        faculty.user = user
        faculty.phone_number = self.cleaned_data['phone_number']
        faculty.department = self.cleaned_data['department']
        if commit:
            faculty.save()
        return faculty 