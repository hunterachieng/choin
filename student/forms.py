from leadership.models import User
from django import forms

from student.models import Student

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name','image')
       

# Edit User Profile form
class UserProfileForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = (
            
            'class_name',
        )
