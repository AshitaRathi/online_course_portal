from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import FileExtensionValidator

USER_CHOICES =(
    ("Student", "Student"),
    ("Teacher", "Teacher"),
)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=100,null=True)
    email = models.EmailField(_('email address'), unique=True,null=True)
    user_type = models.CharField(max_length = 20,choices = USER_CHOICES,null=True)
    phone_number = PhoneNumberField(unique = True, null = True)
    is_staff = models.BooleanField(default=False,null=True)
    is_active = models.BooleanField(default=True,null=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # modified_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

COURSE_CHOICES = (
    ('Design' , 'Design'),
    ('Development','Development'),
    ('Marketing', 'Marketing'),
    ('IT and Software','IT and Software'),
    ('Personal Development','Personal Development'),
    ('Photography','Photography'),
    ('Music','Music')
)

class Course(models.Model):
    course_name = models.CharField(max_length=200,null=True)
    course_image = models.ImageField(upload_to='course_images/',null=True)
    course_type = models.CharField(max_length=100,choices = COURSE_CHOICES,null=True)
    total_hours = models.FloatField(null=True)
    description = models.CharField(max_length=500,null=True)
    reading_content = models.FileField(upload_to='course_reading_content_uploaded',null=True)
    video = models.FileField(upload_to='course_videos_uploaded',null=True, 
            validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

class Comment(models.Model):
    username = models.CharField(max_length=100,null=True)
    description = models.CharField(max_length=100,null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)

class Enrollment(models.Model):
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE, null=True)
    course = models.ForeignKey("Course", on_delete=models.CASCADE, null=True)
    is_enrolled = models.BooleanField(null=True,default=False)
    

