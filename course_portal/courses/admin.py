from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import *
from .models import *


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('full_name','email', 'user_type', 'is_staff', 'is_active',)
    list_filter = ('full_name','email', 'user_type','is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name','user_type', 'email', 'password', 'phone_number','is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

class CourseAdmin(admin.ModelAdmin):
    form = CourseForm
    list_display = ('course_name', 'course_type','total_hours')
    fieldsets = ((
        None, {
            'fields': ('course_name', 'course_type','total_hours')
        }), 
    )
    
    def save_model(self, request, obj):
        obj.user = request.user.id
        print(obj.user)
        obj.save()


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Course)
admin.site.register(Comment)
admin.site.register(Enrollment)
