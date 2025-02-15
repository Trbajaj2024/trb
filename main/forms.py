from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Student, Teacher

class StudentSignUpForm(UserCreationForm):
    roll_number = forms.CharField(max_length=20)
    grade = forms.CharField(max_length=10)
    section = forms.CharField(max_length=10)
    parent_name = forms.CharField(max_length=100)
    parent_phone = forms.CharField(max_length=15)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'phone', 'address', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        if commit:
            user.save()
            Student.objects.create(
                user=user,
                roll_number=self.cleaned_data.get('roll_number'),
                grade=self.cleaned_data.get('grade'),
                section=self.cleaned_data.get('section'),
                parent_name=self.cleaned_data.get('parent_name'),
                parent_phone=self.cleaned_data.get('parent_phone')
            )
        return user

class TeacherSignUpForm(UserCreationForm):
    employee_id = forms.CharField(max_length=20)
    subject = forms.CharField(max_length=50)
    qualification = forms.CharField(max_length=100)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'phone', 'address', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
            Teacher.objects.create(
                user=user,
                employee_id=self.cleaned_data.get('employee_id'),
                subject=self.cleaned_data.get('subject'),
                qualification=self.cleaned_data.get('qualification')
            )
        return user 