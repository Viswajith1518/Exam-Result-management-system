from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Student, Subject, Department, Result


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_active']
    list_filter = ['role', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['register_number', 'full_name', 'department', 'semester', 'batch_year']
    list_filter = ['department', 'semester', 'batch_year']
    search_fields = ['register_number', 'full_name']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'department', 'credits', 'semester']
    list_filter = ['department', 'semester']


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'semester', 'internal_marks', 'external_marks', 'grade', 'is_pass']
    list_filter = ['semester', 'is_pass', 'grade']
    search_fields = ['student__register_number', 'student__full_name']
