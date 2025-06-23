from django import forms
from core.models import User, Student

class StudentRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    name = forms.CharField(label='Full Name', widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone_number = forms.CharField(label='Phone Number', widget=forms.TextInput(attrs={'placeholder': '10-digit Phone Number'}))

    class Meta:
        model = Student
        fields = ['roll_number', 'phone_number']
        widgets = {
            'roll_number': forms.TextInput(attrs={'placeholder': 'Roll Number'}),
        }

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError('Enter a valid 10-digit phone number.')
        return phone

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean_roll_number(self):
        roll_number = self.cleaned_data['roll_number']
        if Student.objects.filter(roll_number=roll_number).exists():
            raise forms.ValidationError('This roll number is already registered.')
        return roll_number

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['name'],
            is_student=True
        )
        student = super().save(commit=False)
        student.user = user
        student.phone_number = self.cleaned_data['phone_number']
        if commit:
            student.save()
            self.save_m2m()
        return student 