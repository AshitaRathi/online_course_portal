from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from django import forms
from django.forms import ClearableFileInput

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('full_name','email','user_type','phone_number',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('course_name', 'course_image', 'course_type','total_hours','total_hours','description','video','reading_content')
        
class CommentForm(forms.ModelForm):
    description = forms.CharField(label ="", widget = forms.Textarea(
    attrs ={
        'class':'form-control',
        'placeholder':'Comment here !',
        'rows':4,
        'cols':50
    }))
    class Meta:
        model = Comment
        fields =['username','description']